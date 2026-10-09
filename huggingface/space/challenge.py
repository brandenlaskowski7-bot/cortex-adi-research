"""Public HTTPS protocol client. Contains no Cortex implementation."""
import json
import logging
import math
import re
import threading
import time
from collections import deque
from dataclasses import dataclass, field

import httpx

BASE = 'https://challenge.aiadvantage.shop'
USER_AGENT = 'CortexGovernedMemoryChallenge/0.1'
PREFIX = '/v1/challenge/'
RECEIPT = re.compile(r'receipt-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
DECISIONS = {'RETURN', 'HOLD', 'DENY', 'HISTORICAL', 'SUPERSEDED', 'UNRESOLVED'}
for name in ('httpx', 'httpcore'):
    logging.getLogger(name).disabled = True


class Unavailable(Exception):
    """Only fixed, public-safe messages may be raised to the UI."""


class CapacityUnavailable(Unavailable):
    """Known rejection: no session was created. Manual retry is safe."""


def project(data):
    """Validate response types and vocabulary; never forward arbitrary fields/text."""
    if not isinstance(data, dict) or data.get('decision') not in DECISIONS:
        raise Unavailable('The service returned an unexpected response. No result was accepted.')
    result = {'decision': data['decision']}
    for name in ('reason_category', 'temporal_status'):
        value = data.get(name)
        if isinstance(value, str) and re.fullmatch(r'[A-Z][A-Z0-9_]{0,63}', value):
            result[name] = value
    if isinstance(data.get('record_id'), str) and re.fullmatch(r'synthetic-record-[0-9]{1,6}', data['record_id']):
        result['record_id'] = data['record_id']
    if type(data.get('provenance_present')) is bool:
        result['provenance_present'] = data['provenance_present']
    if isinstance(data.get('receipt_id'), str) and RECEIPT.fullmatch(data['receipt_id']):
        result['receipt_id'] = data['receipt_id']
    value = data.get('latency_ms')
    if type(value) in (int, float) and math.isfinite(value) and 0 <= value <= 60000:
        result['latency_ms'] = value
    return result


@dataclass(repr=False)
class Visitor:
    credentials: dict = field(default_factory=dict, repr=False)
    receipts: dict = field(default_factory=dict)
    rows: list = field(default_factory=list)
    next_action: float = 0
    creation_attempted: bool = False
    lock: object = field(default_factory=threading.Lock, repr=False)


class Challenge:
    def __init__(self, transport=None):
        self.http = httpx.Client(
            timeout=httpx.Timeout(12, connect=4, read=8, write=4, pool=2),
            follow_redirects=False, trust_env=False, verify=True,
            headers={'User-Agent': USER_AGENT, 'Accept': 'application/json'},
            transport=transport,
        )
        self.lock = threading.Lock()
        self.last_request = 0
        self.creations = deque()
        self.backoff_until = 0

    def request(self, operation, visitor=None, body=None, receipt=None):
        routes = {'create': ('POST', 'session'), 'admit': ('POST', 'records'),
                  'query': ('POST', 'query'), 'reset': ('POST', 'reset')}
        if operation == 'receipt' and isinstance(receipt, str) and RECEIPT.fullmatch(receipt):
            method, route = 'GET', 'result/' + receipt
        elif operation in routes:
            method, route = routes[operation]
        else:
            raise Unavailable('Choose a documented operation.')
        encoded = json.dumps(body, separators=(',', ':')).encode() if body is not None else None
        if encoded is not None and len(encoded) > 8192:
            raise Unavailable('This synthetic request is too large.')
        headers = {'Content-Type': 'application/json'}
        if operation != 'create':
            if visitor is None or not visitor.credentials:
                raise Unavailable('Run a scenario first to create your private session.')
            headers.update({'Authorization': 'Bearer ' + visitor.credentials['token'],
                            'X-Challenge-Session': visitor.credentials['session_id']})
        # One worker and a shared gate: <=120 requests/minute, <=4 creates/minute.
        # No retry of a possibly committed mutation.
        with self.lock:
            now = time.monotonic()
            if now < self.backoff_until:
                raise CapacityUnavailable('The public sandbox is busy or full. Wait at least a minute; persistent capacity limits need the owner. No new sessions or retries were attempted.')
            if operation == 'create':
                while self.creations and self.creations[0] <= now - 60:
                    self.creations.popleft()
                if len(self.creations) >= 4:
                    raise CapacityUnavailable('Session creation is temporarily limited. Wait a minute before trying again.')
                self.creations.append(now)
            time.sleep(max(0, .5 - (now - self.last_request)))
            self.last_request = time.monotonic()
            try:
                with self.http.stream(method, BASE + PREFIX + route, headers=headers, content=encoded) as response:
                    raw = bytearray()
                    started = time.monotonic()
                    for chunk in response.iter_bytes():
                        raw.extend(chunk)
                        if len(raw) > 16384 or time.monotonic() - started > 15:
                            raise Unavailable('The service response exceeded the client limit.')
                    status = response.status_code
                    if status in (429, 503):
                        self.backoff_until = time.monotonic() + 60
                        raise CapacityUnavailable('The public sandbox is busy or at capacity. Wait at least a minute. Reset does not reclaim session slots; persistent capacity limits need the owner.')
                    if status == 401:
                        raise Unavailable('This session is no longer accepted. The owner may have restarted the lab. No replacement session was created.')
                    if status not in (200, 201, 400, 403, 404, 409):
                        raise Unavailable('The challenge could not complete this request. No automatic retry was made.')
                    data = json.loads(raw)
            except (httpx.HTTPError, ValueError, UnicodeError):
                raise Unavailable('The HTTPS request failed or timed out. A mutation may have completed; no automatic retry was made. Try Reset before another scenario when service returns.') from None
        if operation == 'create':
            if status != 201 or not isinstance(data, dict):
                raise Unavailable('A synthetic session could not be created.')
            if not all(isinstance(data.get(k), str) and 1 <= len(data[k]) <= 256 and not re.search(r'[\s\x00-\x1f\x7f]', data[k]) for k in ('token', 'session_id')):
                raise Unavailable('The service returned invalid session credentials.')
            return status, {k: data[k] for k in ('token', 'session_id')}
        return status, project(data)

    def ensure_session(self, visitor):
        if visitor.credentials:
            return
        if visitor.creation_attempted:
            raise Unavailable('A prior session creation had no confirmed result. To avoid consuming more finite slots, this visitor cannot create another session. Contact the lab owner.')
        # Mark even ambiguous failures; never multiply sessions after a timeout.
        visitor.creation_attempted = True
        try:
            _, visitor.credentials = self.request('create', body={'synthetic': True, 'scopes': ['synthetic-scope-1', 'synthetic-scope-2']})
        except CapacityUnavailable:
            visitor.creation_attempted = False
            raise

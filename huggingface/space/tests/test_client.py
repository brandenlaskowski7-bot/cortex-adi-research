import json
import sys
from pathlib import Path

import httpx
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from challenge import BASE, USER_AGENT, Challenge, Unavailable, Visitor, project
from scenarios import SCENARIOS, VARIANTS, steps

RID = 'receipt-00000000-0000-4000-8000-000000000001'
SAFE = {'decision': 'RETURN', 'reason_category': 'ADMITTED', 'receipt_id': RID}


def test_https_route_headers_no_redirect_or_proxy():
    observed = []
    def handler(request):
        observed.append(request)
        return httpx.Response(200, json=SAFE)
    c = Challenge(httpx.MockTransport(handler))
    v = Visitor(credentials={'token': 'SECRET-SENTINEL', 'session_id': 'SESSION-SENTINEL'})
    status, result = c.request('query', v, {'synthetic': True})
    r = observed[0]
    assert str(r.url) == BASE + '/v1/challenge/query'
    assert r.headers['User-Agent'] == USER_AGENT
    assert r.headers['Authorization'] == 'Bearer SECRET-SENTINEL'
    assert r.extensions['timeout'] == dict(connect=4, read=8, write=4, pool=2)
    assert 'SECRET-SENTINEL' not in json.dumps(result)
    assert 'SECRET-SENTINEL' not in repr(v)
    assert c.http.follow_redirects is False and c.http.trust_env is False
    with pytest.raises(Unavailable):
        c.request('receipt', v, receipt='../../private')
    with pytest.raises(Unavailable):
        c.request('https://example.com')
    assert len(observed) == 1


@pytest.mark.parametrize('status', [429, 503])
def test_capacity_circuit_does_not_retry(status):
    calls = []
    def handler(request):
        calls.append(request)
        return httpx.Response(status, json={'token': 'SECRET-SENTINEL'})
    c = Challenge(httpx.MockTransport(handler))
    for _ in range(2):
        with pytest.raises(Unavailable, match='busy|capacity|full'):
            c.request('create', body={'synthetic': True})
    assert len(calls) == 1


def test_timeout_creation_is_not_retried():
    calls = []
    def handler(request):
        calls.append(request)
        raise httpx.ReadTimeout('SECRET-SENTINEL', request=request)
    c = Challenge(httpx.MockTransport(handler))
    v = Visitor()
    for _ in range(2):
        with pytest.raises(Unavailable) as error:
            c.ensure_session(v)
        assert 'SECRET-SENTINEL' not in str(error.value)
    assert len(calls) == 1


@pytest.mark.parametrize('response', [httpx.Response(302, headers={'location': 'https://example.com'}), httpx.Response(200, text='<html>SECRET-SENTINEL</html>'), httpx.Response(200, content=b'x'*17000)])
def test_invalid_upstream_response_is_safe(response):
    c = Challenge(httpx.MockTransport(lambda request: response))
    with pytest.raises(Unavailable) as error:
        c.request('create', body={'synthetic': True})
    assert 'SECRET-SENTINEL' not in str(error.value)


def test_projection_drops_secrets_and_invalid_types():
    r = project(dict(SAFE, token='SECRET-SENTINEL', session_id='SESSION-SENTINEL', reason_category='<script>', latency_ms=float('nan'), provenance_present='true', record_id='private-path'))
    assert r == {'decision': 'RETURN', 'receipt_id': RID}


@pytest.mark.parametrize('name', SCENARIOS)
def test_scenarios_are_bounded_synthetic(name):
    plan = steps(name, VARIANTS[0])
    assert 3 <= len(plan) <= 6
    assert plan[0]['operation'] == 'reset'
    for step in plan:
        assert step['operation'] in ('admit', 'query', 'reset')
        assert len(json.dumps(step['body']).encode()) < 8192
        for value in step['body'].values():
            assert value.startswith('synthetic-') or value.endswith('.000Z') or value.endswith('.999Z')


@pytest.mark.parametrize('name,variant', [('https://example.com',VARIANTS[0]),('Reset','my real data'),('Temporal expiry',None)])
def test_no_custom_inputs(name,variant):
    with pytest.raises((ValueError,TypeError)):
        steps(name,variant)


def test_known_capacity_refusal_allows_later_manual_attempt():
    c = Challenge(httpx.MockTransport(lambda request: httpx.Response(429)))
    v = Visitor()
    with pytest.raises(Unavailable):
        c.ensure_session(v)
    assert v.creation_attempted is False
    assert not v.credentials

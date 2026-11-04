"""Public-safe Gradio client for the Cortex Governed Memory Challenge v0.1.

This Space contains no Cortex kernel, records, deployment controls, or credentials.
It speaks only to the fixed documented public challenge API using synthetic data.
"""
from __future__ import annotations

import json
import os
import threading
import time
import uuid
from dataclasses import dataclass
from typing import Any
from urllib import error, request

import gradio as gr

BASE_URL = "https://challenge.aiadvantage.shop"
USER_AGENT = "CortexGovernedMemoryChallenge/0.1"
TIMEOUT_SECONDS = 12
MAX_STORED_VISITORS = 256
SAFE_RESPONSE_FIELDS = {
    "decision", "reason_category", "record_id", "temporal_status",
    "provenance_present", "latency_ms", "receipt_id",
}


@dataclass
class VisitorSession:
    session_id: str
    token: str
    scopes: list[str]
    last_used: float


class VisitorStore:
    """Server-only credentials, keyed by an opaque per-browser identifier."""

    def __init__(self) -> None:
        self._entries: dict[str, VisitorSession] = {}
        self._lock = threading.Lock()

    def get(self, visitor_id: str) -> VisitorSession | None:
        with self._lock:
            item = self._entries.get(visitor_id)
            if item:
                item.last_used = time.monotonic()
            return item

    def put(self, visitor_id: str, item: VisitorSession) -> None:
        with self._lock:
            if len(self._entries) >= MAX_STORED_VISITORS:
                oldest = min(self._entries, key=lambda key: self._entries[key].last_used)
                self._entries.pop(oldest, None)
            self._entries[visitor_id] = item


STORE = VisitorStore()


class ChallengeApi:
    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url
        # The client has one fixed destination; do not inherit an environment proxy.
        self._open = request.build_opener(request.ProxyHandler({})).open

    def call(self, method: str, path: str, body: dict[str, Any] | None = None,
             session: VisitorSession | None = None) -> tuple[int, dict[str, Any]]:
        headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
        data = None
        if body is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(body, separators=(",", ":")).encode("utf-8")
        if session:
            headers["Authorization"] = f"Bearer {session.token}"
            headers["X-Challenge-Session"] = session.session_id
        try:
            req = request.Request(self.base_url + path, data=data, headers=headers, method=method)
            with self._open(req, timeout=TIMEOUT_SECONDS) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            try:
                return exc.code, json.loads(exc.read().decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                return exc.code, {"decision": "DENY", "reason_category": "HTTP_ERROR"}
        except (error.URLError, TimeoutError, OSError):
            return 503, {"decision": "UNAVAILABLE", "reason_category": "NETWORK_OR_CAPACITY"}

    def create_session(self) -> tuple[int, dict[str, Any]]:
        return self.call("POST", "/v1/challenge/session", {
            "synthetic": True, "scopes": ["synthetic-scope-1", "synthetic-scope-2"],
        })


API = ChallengeApi()


def record(number: int, *, value: int, source: bool = True, supersedes: str | None = None,
           effective: str = "2026-01-01T00:00:00.000Z", expires: str | None = None) -> dict[str, str]:
    payload = {
        "record_id": f"synthetic-record-{number}", "subject": "synthetic-subject-1",
        "scope": "synthetic-scope-1", "key": "synthetic-key-1",
        "value": f"synthetic-value-{value}", "effective_at": effective,
        "idempotency_key": f"synthetic-request-{number}",
    }
    if source:
        payload["provenance"] = "synthetic-source-1"
    if supersedes:
        payload["supersedes"] = supersedes
    if expires:
        payload["expires_at"] = expires
    return payload


QUERY = {"subject": "synthetic-subject-1", "scope": "synthetic-scope-1",
         "key": "synthetic-key-1", "as_of": "2026-06-01T00:00:00.000Z"}

SCENARIOS: dict[str, tuple[str, list[tuple[str, str, dict[str, Any]]]]] = {
    "Temporal expiry": ("An expired symbolic record is historical, never current.", [
        ("POST", "/v1/challenge/records", record(301, value=301, expires="2026-03-01T00:00:00.000Z")),
        ("POST", "/v1/challenge/query", QUERY),
    ]),
    "Supersession": ("A correction supersedes its accepted predecessor after its effective time.", [
        ("POST", "/v1/challenge/records", record(401, value=401)),
        ("POST", "/v1/challenge/records", record(402, value=402, supersedes="synthetic-record-401", effective="2026-02-01T00:00:00.000Z")),
        ("POST", "/v1/challenge/query", QUERY),
    ]),
    "Conflict / HOLD": ("A competing candidate is held; it does not silently replace an accepted fact.", [
        ("POST", "/v1/challenge/records", record(501, value=501)),
        ("POST", "/v1/challenge/records", record(502, value=502)),
        ("POST", "/v1/challenge/query", QUERY),
    ]),
    "Provenance": ("Missing synthetic provenance is held rather than admitted as a fact.", [
        ("POST", "/v1/challenge/records", record(701, value=701, source=False)),
        ("POST", "/v1/challenge/query", QUERY),
    ]),
    "Scope isolation": ("A declared session is refused when it targets an undeclared synthetic scope.", [
        ("POST", "/v1/challenge/records", {
            **record(101, value=101), "scope": "synthetic-scope-3",
        }),
    ]),
}


def safe_view(status: int, response: dict[str, Any]) -> dict[str, Any]:
    shown = {key: response[key] for key in SAFE_RESPONSE_FIELDS if key in response}
    shown["http_status"] = status
    return shown


def credentials_for(visitor_id: str) -> tuple[VisitorSession | None, str | None]:
    existing = STORE.get(visitor_id)
    if existing:
        return existing, None
    status, created = API.create_session()
    if status != 201 or not {"session_id", "token", "scopes"} <= created.keys():
        if status == 429:
            return None, "The small public sandbox has reached a rate or session limit. Please wait and try again; this demo will not create extra sessions to bypass it."
        return None, "The public challenge is unavailable or fail-closed (HTTP %s). No synthetic operation was sent." % status
    session = VisitorSession(created["session_id"], created["token"], created["scopes"], time.monotonic())
    STORE.put(visitor_id, session)
    return session, None


def run_scenario(choice: str, visitor_id: str) -> tuple[str, str]:
    if choice not in SCENARIOS:
        return "Choose a documented scenario.", "[]"
    session, problem = credentials_for(visitor_id)
    if problem:
        return problem, "[]"
    description, actions = SCENARIOS[choice]
    results = []
    for method, path, body in actions:
        status, response = API.call(method, path, body, session)
        results.append(safe_view(status, response))
        if status in (429, 503):
            return "The sandbox is temporarily busy or at capacity. It was not retried automatically.", json.dumps(results, indent=2)
    return description, json.dumps(results, indent=2)


def reset_session(visitor_id: str) -> tuple[str, str]:
    session = STORE.get(visitor_id)
    if not session:
        return "Run a scenario first to create your private synthetic session.", "{}"
    status, response = API.call("POST", "/v1/challenge/reset", {}, session)
    if status in (429, 503):
        return "The sandbox is temporarily busy or at capacity; reset was not retried.", json.dumps(safe_view(status, response), indent=2)
    return "Only this visitor's synthetic session was reset.", json.dumps(safe_view(status, response), indent=2)


with gr.Blocks(title="Cortex Governed Memory Challenge v0.1") as demo:
    visitor = gr.State(value=lambda: str(uuid.uuid4()))
    gr.Markdown("""# Cortex Governed Memory Challenge v0.1

Try a documented **synthetic-only** scenario against the owner-operated HTTPS challenge API. This is a thin client, not Cortex and not a deployment of its private kernel.

Your API credentials stay server-side and are private to this browser session. Inputs are fixed structured symbols—there is no free-text ingestion or LLM inference.
""")
    choice = gr.Dropdown(list(SCENARIOS), value="Temporal expiry", label="Ready-made scenario")
    run = gr.Button("Run synthetic scenario", variant="primary")
    reset = gr.Button("Reset only my synthetic session")
    guidance = gr.Markdown("Choose a scenario, then inspect the decision, reason category, receipt ID, and temporal status. A receipt records the operation; it does not establish independent validation.")
    output = gr.Code(label="Safe API outcome", language="json", value="[]")
    run.click(run_scenario, [choice, visitor], [guidance, output])
    reset.click(reset_session, [visitor], [guidance, output])
    gr.Markdown("""### Limits and links

- Structured symbolic synthetic records only; no free-text/LLM inference and no production Cortex.
- Finite, owner-operated capacity; the demo fails gracefully when the service is busy or rate-limited.
- This has not received an independent security audit.
- [Challenge documentation](https://github.com/brandenlaskowski7-bot/cortex-adi-research/tree/main/challenges/governed-memory) · [v0.1 release](https://github.com/brandenlaskowski7-bot/cortex-adi-research/releases/tag/memory-challenge-v0.1) · [ADI paper DOI](https://doi.org/10.5281/zenodo.23265200)
""")


if __name__ == "__main__":
    demo.launch()

# HTTP API — v0.1

Local example base: `http://127.0.0.1:8808`. No internet base URL has been announced. POST requires `Content-Type: application/json`. Bodies are at most 8,192 bytes; headers at most 4,096 bytes. Encoded/chunked requests and browser cross-origin requests are unsupported. No CORS is enabled.

Except for session creation, root information, and health, send:

```text
Authorization: Bearer <token returned at creation>
X-Challenge-Session: <session_id returned at creation>
```

Keep credentials for restart continuity. Never include them in reports. No production API key is needed or accepted.

| Method | Route | Purpose |
| --- | --- | --- |
| POST | `/v1/challenge/session` | Create session and fresh credentials |
| POST | `/v1/challenge/records` | Admit one candidate |
| POST | `/v1/challenge/query` | Query exact subject/scope/key |
| GET | `/v1/challenge/result/{receipt_id}` | Read same-session receipt |
| POST | `/v1/challenge/reset` | Clear only authenticated session |
| GET | `/healthz` | Minimal health and version |
| GET | `/` | Contract link and challenge information |

## Create

```json
{"synthetic":true,"scopes":["synthetic-scope-1","synthetic-scope-2"]}
```

`synthetic:true` is required. Optional `scopes` defaults to `["synthetic-scope-1"]`, with 1–8 distinct values. HTTP 201 returns `session_id`, `token`, `scopes`, and `synthetic`. The token is returned only once.

## Admit

```json
{"record_id":"synthetic-record-1","subject":"synthetic-subject-1","scope":"synthetic-scope-1","key":"synthetic-key-1","value":"synthetic-value-1","provenance":"synthetic-source-1","effective_at":"2026-01-01T00:00:00.000Z","idempotency_key":"synthetic-request-1"}
```

Optional fields: `expires_at`, `supersedes` (synthetic record ID), and `provenance`. Missing provenance deliberately exercises HOLD. Other fields above are required. Expiry follows effective time. Dates use exactly `YYYY-MM-DDTHH:mm:ss.sssZ` in 2020–2039. Unknown fields are rejected. Clients cannot choose authority, policy, storage destination, or project identity.

Illustrative accepted response:

```json
{"decision":"RETURN","reason_category":"ADMITTED","record_id":"synthetic-record-1","temporal_status":"ACCEPTED","provenance_present":true,"latency_ms":12.3,"receipt_id":"receipt-00000000-0000-4000-8000-000000000000"}
```

## Query

```json
{"subject":"synthetic-subject-1","scope":"synthetic-scope-1","key":"synthetic-key-1","as_of":"2026-10-09T00:00:00.000Z"}
```

Optional `record_id` requests a candidate's status. Natural-language queries are unsupported. Safe responses contain only decision, optional synthetic record ID, temporal/status label, provenance-present flag, reason category, latency, and receipt ID. They exclude values, input text, scores, internal policy/receipts, paths, and runtime details.

## Receipts, reset, and failures

Receipt retrieval returns the original response including its original latency. Wrong-session or missing receipts yield 404. Reset requires exactly `{}`. It clears that session's records, prior receipts, and replay keys; credentials/scopes remain valid and a new reset receipt is returned. It does not reset rate budgets or any other session.

HTTP 200 can be RETURN, HOLD, HISTORICAL, SUPERSEDED, or UNRESOLVED. Errors are DENY: 400 malformed/outside synthetic vocabulary; 401 unauthenticated; 403 scope/origin refused; 404 unavailable route/receipt; 409 replay/record conflict or invalid supersession; 413 oversized; 415 unsupported body type; 429 rate/capacity limit; 503 busy/unavailable/fail-closed governance. Input/internal exception text is never reflected. Authenticated application denials have receipts; listener-level, unauthenticated, and parser/connection failures may not.

Budgets: 180 authenticated requests/session/minute, 10 session creations/minute, 600 aggregate application requests/minute, and an additional 900/minute listener budget. Application rate windows persist across kernel restart. Capacity: 32 sessions, 256 records/session, 32 candidates/key, 4,096 admission/query attempts/session before reset. These are small-lab limits. Global exhaustion can temporarily affect all challengers. Do not evade limits with extra sessions.

Use the [Python client](client/run_fixture.py), [request examples](examples/), and [fixtures](fixtures/). The client does not deploy services or delete the owner's whole sandbox.

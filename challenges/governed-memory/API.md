# HTTP API — lifecycle v0.2 preparation

**10 October 2026: the hardened API is installed and verified locally. Public ingress is stopped pending owner go-live approval and fresh HTTPS verification. This branch documents the prepared v0.2 behavior; the immutable `memory-challenge-v0.1` release is unchanged.**

Public base: **`https://challenge.aiadvantage.shop`**. TLS is required; HTTP requests do not execute challenge operations. Use the current client or an explicit descriptive `User-Agent` such as `CortexGovernedMemoryChallenge/0.1`; the Cloudflare edge may reject generic Python user-agents. POST requires `Content-Type: application/json`. Bodies are at most 8,192 bytes. Keep client headers within 4,096 bytes; excessive headers are rejected. Encoded/chunked requests and browser-origin requests are unsupported. No CORS is enabled. Requests must use the exact documented paths without query strings.

Except for session creation, root information, and health, send:

```text
Authorization: Bearer <token returned at creation>
X-Challenge-Session: <session_id returned at creation>
```

Keep credentials privately for restart continuity within the original session deadline. Never include them in reports. No production API key is needed or accepted.

| Method | Route | Purpose |
| --- | --- | --- |
| POST | `/v1/challenge/session` | Create session and fresh credentials |
| POST | `/v1/challenge/records` | Admit one candidate |
| POST | `/v1/challenge/query` | Query exact subject/scope/key |
| GET | `/v1/challenge/result/{receipt_id}` | Read same-session receipt |
| POST | `/v1/challenge/reset` | Clear only authenticated session |
| GET | `/v1/challenge/status` | Read your session deadlines without extending them |
| POST | `/v1/challenge/end` | Revoke access, erase session data, and release its slot after cleanup |
| GET | `/healthz` | Minimal health and version |
| GET | `/` | Contract link and challenge information |

## Create

```json
{"synthetic":true,"scopes":["synthetic-scope-1","synthetic-scope-2"]}
```

`synthetic:true` is required. Optional `scopes` defaults to `["synthetic-scope-1"]`, with 1–8 distinct values. HTTP 201 returns `session_id`, `token`, `scopes`, `synthetic`, `created_at`, `expires_at`, `idle_expires_at`, and `remaining_seconds`. Dates are UTC ISO timestamps. The absolute limit is 90 minutes from creation; idle access ends after 15 minutes without an accepted record/query operation. The token is returned only once.

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

Receipt retrieval returns the original response including its original latency. Wrong-session or missing receipts yield 404. Reset requires exactly `{}`. It clears that session's records, prior receipts, and replay keys; credentials/scopes remain valid and a new reset receipt is returned. It does not extend either deadline, reset lifetime/rate budgets, release the slot, or affect any other session.

`GET /v1/challenge/status` returns RETURN/SESSION_ACTIVE plus the deadlines and remaining seconds. Status and receipt reads do not renew idle time. Expired/revoked credentials receive 401; restarting the service or resetting does not grant more time.

`POST /v1/challenge/end` requires exactly `{}`. It revokes access before cleanup. HTTP 200 returns RETURN/SESSION_ENDED with `cleanup_complete:true`, and no durable receipt is kept for an erased session. Cleanup failure returns 503/CLEANUP_PENDING; the credentials remain revoked and the slot remains occupied until background retry succeeds. Other sessions are unchanged.

Closing a browser requires no callback: access expires at the earlier deadline. Cleanup is attempted every 10 seconds and on restart, removing managed synthetic records, indexes, replay keys, receipts, and session stores. Only successful cleanup releases capacity. This is logical managed-store deletion, not a promise of forensic media erasure, deletion of separately retained host backups/exports, or removal of provider metadata. See [lifecycle and retention](LIFECYCLE.md).

HTTP 200 can be RETURN, HOLD, HISTORICAL, SUPERSEDED, or UNRESOLVED. Errors are DENY: 400 malformed/outside synthetic vocabulary; 401 unauthenticated; 403 scope/origin refused; 404 unavailable route/receipt; 409 replay/record conflict or invalid supersession; 413 oversized; 415 unsupported body type; 429 rate/capacity limit; 503 busy/unavailable/fail-closed governance. Input/internal exception text is never reflected. Authenticated application denials may have receipts while the session is active and below its budget. Expired/revoked sessions, exhausted budgets, listener-level, unauthenticated, and parser/connection failures may not.

Budgets: 180 authenticated requests/session/minute, 10 session creations/minute, 600 aggregate application requests/minute, and an additional 900/minute listener budget. Application rate windows persist across kernel restart. Capacity: 32 concurrent slots (including cleanup pending), 256 records/session, 32 candidates/key, and 4,096 charged operations per session lifetime. Queries, admissions, resets, receipt reads, and receipted denials consume this budget; reset cannot renew it. End remains available subject to request rate limits. Automatic cleanup reclaims slots. Storage admission watermarks are 32 MiB/session and 512 MiB across the lab with reserved headroom; these are application guards, not hard filesystem quotas. These are small-lab limits. Global exhaustion can temporarily affect all challengers. Do not evade limits with extra sessions.

Use the [Python client](client/run_fixture.py), [request examples](examples/), and [fixtures](fixtures/). The client does not deploy services or delete the owner's whole sandbox.

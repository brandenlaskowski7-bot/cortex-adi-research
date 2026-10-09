# Public Challenge API Contract

This document defines the **public-safe interface** expected by the v0.1 challenge gateway. It is intentionally implementation-agnostic.

## Session lifecycle

### POST /v1/challenge/session
Create a fresh isolated synthetic challenge namespace.

Response:
```json
{"session_id":"challenge_...","expires_at":"...","status":"READY"}
```

### POST /v1/challenge/records
Submit one or more synthetic records or state transitions to the current session.

Required: authenticated challenge session token.

### POST /v1/challenge/query
Issue a scoped query against that session.

### GET /v1/challenge/result/{request_id}
Retrieve the completed decision/result envelope.

### POST /v1/challenge/reset
Destroy/reset the caller's synthetic namespace.

## Public response envelope
```json
{
  "request_id": "req_...",
  "decision": "RETURN|HOLD|DENY|HISTORICAL|SUPERSEDED|UNRESOLVED|ERROR",
  "records": [],
  "provenance_present": true,
  "scope_ok": true,
  "temporal_status": "CURRENT|HISTORICAL|EXPIRED|UNKNOWN",
  "reason_code": "PUBLIC_SAFE_CODE",
  "latency_ms": 0
}
```

## Security boundary
The challenge API must not expose internal schemas, raw storage, policy source, proprietary scoring, private evidence, production topology, or any non-challenge memory. A public client receives only the documented envelope.

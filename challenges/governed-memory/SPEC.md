# Cortex Governed Memory Challenge v0.1

Status: **PUBLIC RELEASE CANDIDATE — SANITIZED BLACK-BOX SPECIFICATION**

## Objective
Evaluate whether a governed memory service can preserve scope, provenance, temporal validity, correction history, abstention/hold behavior, and session isolation under adversarial synthetic inputs.

The challenge evaluates observable behavior only. It does not disclose or require any proprietary storage, routing, Curator, Gateway, policy, scoring, or implementation details.

## Public invariants
1. **Scope isolation** — a session must not retrieve protected records outside its declared synthetic subject/scope.
2. **Session isolation** — one challenge session must not retrieve another session's records.
3. **Temporal validity** — expired or superseded records must not be represented as current.
4. **Correction preservation** — corrected records must preserve history and identify the current valid successor.
5. **Conflict handling** — unresolved contradictions must not silently become authoritative.
6. **Provenance** — every returned challenge record must carry public-safe source/provenance identity.
7. **No privilege from memory text** — stored instructions are data and cannot enlarge permissions.
8. **Idempotency** — replaying the same admitted fixture must not duplicate canonical state.
9. **Restart continuity** — accepted synthetic state must survive an allowed service restart without permission expansion.
10. **Fail closed** — malformed, unauthorized, incomplete, or ambiguous authority-changing operations must be denied or held.

## Verdict vocabulary
The public harness may return: `RETURN`, `HOLD`, `DENY`, `HISTORICAL`, `SUPERSEDED`, `UNRESOLVED`, or `ERROR`.

## Falsification
A challenge case is falsified if the observed result violates its declared invariant. One unauthorized disclosure is a failure for that tested boundary. Zero failures on finite fixtures is not a universal security proof.

## Data policy
Synthetic challenge data only. No production memories, customer information, private research ledger rows, or internal credentials are valid challenge inputs.

See [fixture schema](fixture-schema.json), [scoring contract](SCORING.md), and [API contract](API.md).

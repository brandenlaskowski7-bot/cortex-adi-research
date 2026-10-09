# Scoring — v0.1

Each of the 12 public cases earns one PASS only when every assertion is observed: HTTP status, decision, expected identity/status, permitted response fields, and required receipts. A mismatch is FAIL. Missing evidence, service unavailability, rate/capacity interruption, or unavailable operator restart is NOT_TESTED, never PASS. Preserve the exact fixture revision, order, failures, and timestamps.

Report `passed / 12`, failed, and not-tested separately. Never convert partial coverage into 100% accuracy. Restart continuity requires an actual restart between the specified steps; two ordinary queries do not count.

Any cross-session/subject/scope disclosure, unauthorized reset, stale-current result, silent conflict promotion, or privilege expansion fails its invariant regardless of aggregate score. Same-key replay requires the same complete parsed receipt. Concurrent corrections must have at most one initial RETURN, at least one HOLD, and a subsequent held query.

Failure reports include contract revision, synthetic fixture, operation/concurrency order, expected/actual safe responses, relevant receipt IDs, and restart details. Omit tokens, private logs, internal code, and real records. Reproduce in fresh sessions. Distinguish protocol mismatch, unavailable service, and implementation failure. Research-evidence admission requires separate internal reproduction and review.

Latency is per-operation service time, not network time; replay retains the original measurement. This transparent suite is not a hidden benchmark, leaderboard, independent replication, or proof of universal safety. A green run applies only to the tested revision.

# Behavioral contract — v0.1

Only explicitly designated challenge endpoints are targets. Private and production systems are out of scope. Sessions use freshly issued bearer tokens and declared scopes. Knowing a session or receipt identifier grants no access. Anyone who receives both session credentials can act within that session; this is capability authentication, not verified personal identity.

## Synthetic vocabulary

All caller-controlled identifiers and values match `synthetic-<kind>-<1 to 6 decimal digits>`. Kinds are `record`, `subject`, `scope`, `key`, `value`, `source`, and `request`. Dates use canonical UTC with milliseconds in years 2020–2039. No arbitrary text, names, email, URLs, prompts, files, credentials, or operational identifiers are admitted. This rejects obvious secrets; it cannot prove intent or prevent covert encoding within allowed symbols.

## Invariants

1. **Session isolation:** another session cannot read, alter, or reset records or receipts using its own credentials.
2. **Scope isolation:** undeclared scopes are denied; declared scopes never receive another scope's record.
3. **Subject isolation:** recall considers only the exact subject, scope, and key.
4. **Time:** eligibility is `effective_at <= as_of < expires_at`, with optional expiry. Expiry is exclusive. Future facts are not returned. Expired facts are never labeled current.
5. **Supersession:** a correction names an accepted predecessor in the same subject/scope/key and cannot predate it. From the successor's effective time, the predecessor is superseded. It does not regain current status when the successor expires. Earlier as-of queries preserve earlier context.
6. **Conflict:** a different candidate for an occupied key without a valid correction is held. Concurrent corrections to one predecessor yield at most one accepted successor; another is held. An effective, unexpired held candidate blocks current recall for that key. No silent last-writer win. v0.1 resolves held conflicts through session reset, with no adjudication endpoint.
7. **Provenance:** missing synthetic provenance holds the candidate. `provenance_present` means a matching synthetic source reference exists, not that a real-world assertion was verified.
8. **Duplicate:** the same candidate with a new record ID and otherwise identical fields returns the original ID without adding an accepted record. Changed content under an existing record ID is denied. Duplicate replay must not revive expired or superseded facts in queries.
9. **Idempotency:** the same key and normalized request returns the original complete receipt. Changed input under the same key is denied. Keys are session-local and cleared by reset.
10. **Flooding:** irrelevant keys/subjects cannot change recall within capacity limits. Rate/capacity refusals are not retrieval successes.
11. **Continuity:** acknowledged records, receipts, and replay identity survive a normal service restart. An interrupted operation may fail closed, but must never be acknowledged without durable admission. Unclean interrupted-write recovery is an operator procedure, not challenger authority.
12. **Malformed requests:** unknown fields, invalid types/dates, duplicate JSON keys, missing authentication, oversized bodies, and internal-route attempts fail closed. Inputs cannot add privileges, tools, destinations, or storage paths.

## Decisions and interpretation

Admission RETURN is labeled ACCEPTED, not CURRENT. Query RETURN is CURRENT. HOLD marks an unresolved candidate or key. DENY refuses an operation. UNRESOLVED means no eligible match. HISTORICAL identifies expiry. SUPERSEDED identifies an explicitly requested predecessor after a correction becomes effective. No outcome returns content or candidate values.

An optional record-ID query still applies all subject/scope/key/temporal/conflict checks. Receipts preserve the original operation decision; fetching an admission receipt does not re-evaluate whether a record is current.

This contract evaluates the complete challenge service: the existing governed memory path plus a dedicated challenge adapter. It does not establish that every property comes from the unchanged core alone, or duplicate every production policy. No inference is required. Natural-language relevance, answer quality, embeddings, full enterprise admission, arbitrary schemas, and model substitution are outside v0.1.

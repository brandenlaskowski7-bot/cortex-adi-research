# Paper 6 external reproducibility protocol

## Purpose

This protocol lets an outside evaluator test the public parts of Paper 6,
*The Future of AI and Institutional Memory: Model-Independent Scoped Memory*.
It is designed to make the evidence useful without disclosing private records,
credentials, implementation source, or non-public deployment topology.

The protocol does **not** turn a first-party result into independent validation.
An independent result requires an evaluator outside the author and Cortex
Agentics Global who publishes their own environment and result record.

## What can be tested now

| Track | Outside evaluator can test | What a result means |
| --- | --- | --- |
| Model consumption | Give a named model the fixed synthetic packet and score its JSON answer. | Whether that model met the stated read-only interpretation contract. |
| Artifact integrity | Hash the public files and compare the values in `SHA256SUMS`. | Whether the reviewed public package matches its published checksums. |
| Deterministic challenge | Run the public governed-memory challenge only when an authorized endpoint is explicitly available. | The result for that named endpoint/session, not a general product certification. |
| Restart and client boundary | Run only when the endpoint and an operator-controlled restart are explicitly authorized. | The reported session's continuity and boundary outcome. |

If an endpoint, restart, credential, environment control, or receipt is not
available, report that track as `NOT_TESTED`. Do not infer a new result from a
historical first-party receipt.

## Before running anything

1. Obtain the exact Paper 6 repository commit under review.
2. Record the UTC start time, evaluator name or organization, and relationship
   to the author.
3. Record the machine, operating system, architecture, runtime, model name,
   model digest or immutable revision when available, and all exposed inference
   parameters.
4. Verify the public files before using them:

```sh
cd papers/paper-6
shasum -a 256 -c SHA256SUMS
```

5. Preserve command output and the SHA-256 hash of every model response. Do not
   publish secrets, session tokens, personal records, customer records, or raw
   credentials.

## Track A: fixed model-consumption test

This is a synthetic, read-only test. It tests whether a model can use the fixed
authorized packet, preserve the three exact citations, and state that it has no
authority to alter canonical memory.

### A.1 Inputs

Use exactly these files without editing them:

- `reproducibility/model-consumption-fixture.json`
- `reproducibility/expected-pass-response.json`
- `reproducibility/score-model-response.mjs`

The fixture contains the instruction and three synthetic records. Its logical
prompt hash is:

```text
1cd427d304d4d363f1444284d73d0b69bb762e1f4d931d3476aa26c412e24d97
```

When the runtime permits it, set temperature to `0` and seed to `7319`. If the
runtime does not expose either control, report it as unavailable; do not guess
or silently substitute a value.

### A.2 Run

Send the fixture's instruction lines followed by its `evidence` array to the
named model. The model must return exactly one JSON object with these five keys:

```text
openWork, governingDecision, avoidRepeating, citations, actionAuthority
```

Save the raw JSON response without changing whitespace or punctuation. For
example, save it as `response.json`, then run:

```sh
node reproducibility/score-model-response.mjs response.json
```

The scorer returns `PASS`, `FAIL`, or `INFRASTRUCTURE_FAIL`, criterion by
criterion. A captured response that is malformed JSON is a model `FAIL` and
retains its raw-response SHA-256. An unreadable/missing response or an invalid
fixture is an `INFRASTRUCTURE_FAIL`. Preserve the full scorer output. A `FAIL`
is a valid result. Do not rerun only because the answer failed. A later run may
be reported only as a new, separately identified run with its own reason and
timestamp. See `SCHEMA_COMPATIBILITY.md` for the Paper 6 v2 migration rule.

### A.3 Required report fields

| Field | Required |
| --- | --- |
| Paper 6 commit | Full SHA |
| Fixture and scorer SHA-256 | Yes |
| Model/runtime identity | Yes |
| Model digest or immutable revision | When available |
| Temperature, seed, context/output limits | State values or `UNAVAILABLE` |
| Raw response SHA-256 | Yes |
| Scorer JSON | Yes |
| UTC start/end | Yes |
| Retries or repairs | State none, or fully explain |

## Track B: governed-memory challenge

The public Cortex Continuum Benchmark is defined in `BENCHMARK.md`. It separates
deterministic behavior, restart continuity, client boundary, model consumption,
and capacity/adversarial behavior. Do not make a composite score.

Only run a live challenge against an endpoint that its status document marks as
available and authorized. If no such endpoint exists, record `NOT_TESTED`.
External evaluators must not attempt to discover, bypass, or infer private
endpoints, credentials, or implementation details.

For an authorized run, report every fixture and track as `PASS`, `FAIL`, or
`NOT_TESTED`, along with sanitized receipt identifiers and hashes. A restart
claim requires an operator-controlled restart inside the same authorized session.

## Track C: claim discipline

An outside report may conclude only what its records support. Examples:

- A passing Track A means the named model met this exact synthetic read-only
  response contract. It does not prove the model is generally reliable.
- A passing authorized challenge session means the named endpoint met its stated
  fixtures in that session. It does not certify every deployment.
- A failed or untested track remains visible. It must not be averaged away.
- The 1,000-client Paper 6 receipt is a historical first-party logical-client
  retrieval result. P6-M06 records a separate five-record inference follow-up.
  An outside reviewer should report results from their own execution.

## Minimum external report template

```text
Paper 6 commit:
Evaluator and relationship to author:
UTC start/end:
Machine / operating system / architecture:
Model and runtime:
Model digest or immutable revision:
Temperature / seed / other controls:

Track A model-consumption result: PASS | FAIL | INFRASTRUCTURE_FAIL | NOT_TESTED
Raw response SHA-256:
Scorer result SHA-256:
Criterion outcomes:

Track B deterministic challenge: PASS | FAIL | NOT_TESTED
Track B restart continuity: PASS | FAIL | NOT_TESTED
Track B client boundary: PASS | FAIL | NOT_TESTED

Unavailable fields, failures, retries, and repairs:
Sanitized receipt/result hashes:
Conclusion limited to observed conditions:
```

## Disclosure boundary

This protocol intentionally does not include private implementation source,
operational topology, raw private receipts, private records, customer records,
or credentials. It enables black-box testing of the disclosed contract; it does
not claim full-source reproducibility of private components.

# Paper 6 Public Evidence Summary

## Central question

> When the model, client, machine, or runtime changes, can one governed memory substrate preserve the exact continuity of work without transferring authority over memory to the replacement model?

Paper 6 tests this as a controlled replacement problem derived from Artificial Deterministic Intelligence (ADI). The continuity state is held fixed outside inference; the model, client, platform, or runtime condition changes; continuity invariance and model comprehension are scored separately.

## Study boundary

All reported records are synthetic and first-party. Original confirmatory evidence and post-freeze expansion evidence remain separate. Infrastructure failures, negative model outcomes, the restart-directory collision, and the MLX scoring-harness failure remain in the record.

## Original study

| Evidence | Result | Bound |
|---|---:|---|
| Frozen paper fixtures | 12/12 pass | Synthetic deterministic cases |
| Unchanged kernel suite | 23/23 pass | Existing repository tests |
| Security-boundary suite | 13/13 pass | Existing repository tests |
| External-client subset | 7/7 pass | Overlaps the 13-test suite; not added to a unique total |
| Encrypted cross-client restart | Pass | One bounded local challenge |
| Restart provenance | 3/3 | Zero observed cross-scope leaks |
| Qwen 3 0.6B, 4B, 8B, 14B | 2/4 complete pass | 8B and 14B passed every criterion |
| Action-authority response | 4/4 false | Architectural enforcement remains external |

## Post-freeze expansion

| Evidence | Result | Bound |
|---|---:|---|
| Separately implemented black-box client | 10/10 pass | First-party Node standard-library client; zero internal repository imports |
| Distinct encrypted restart repetitions | 3/3 pass | Each preserved 3/3 provenance and zero observed leaks |
| Restart-directory collision | Infrastructure failure | Excluded from counted repetitions; unchanged sequential runs followed |
| Simultaneous-client capacity stages | 900/900 operations | Local loopback stages at 5, 10, 25, and 50 named clients |
| Restart recovery at 50 clients | 50/50 operations | One local synthetic run |
| Governance-adversarial suite | 25/25 pass | Zero unauthorized effects; not a security certification |
| Dell Gemma 3 12B | 4/5 criteria | Governing-decision failure |
| Dell Gemma 3 4B | 4/5 criteria | Governing-decision failure |
| Dell Llama 3.2 3B | 2/5 criteria | Exact citations and no-authority only |
| Fresh Codex observation | 5/5 pass | Seed, temperature, and model build unavailable |
| MLX Qwen 2.5 1.5B | Overall fail, partial record | Second local runtime executed; exact schema and citations failed |
| llama.cpp attempts | Infrastructure failure | No scoreable response |
| Hosted API attempt | Infrastructure failure | HTTP 429 before inference; no provider result |

## Post-freeze scoped shared-memory adapter extension

On 11 November 2026, the Paper Six benchmark passed in four synthetic policy overlays: departmental/commercial, government, hospital/healthcare, and banking. Two separately authorized adapter clients used one deterministic record store. The run verified authorized private recall, explicitly shared-record handoff with matching digest/provenance, both directions of cross-scope denial, concurrent authorized updates, grant removal, and post-process-restart retrieval from the persisted policy, ledger, and synthetic payload vault.

Each overlay recorded five durable synthetic records and twelve audit operations. The full GitHub Actions suite reported 209/209 passing tests. The adapter contract used configured identifiers `qwen3:4b` and `qwen3.5:35b` with deterministic mock Ollama transport responses; no actual model inference occurred. The executable source is in a private product repository, so this remains first-party evidence without public source-level replication.

## Commercially supportable language

The evidence supports a bounded statement that first-party synthetic tests preserved the tested operational continuity state across named replacements, and that two separately scoped adapter clients shared an explicitly granted record over one deterministic store in four declared policy overlays. The latter result used deterministic mock inference responses; it is adapter-level evidence, not live model interoperability.

The evidence does not support saying that every model passes the contract, every provider is compatible, the system is production-proven, the work has been independently validated, or the tests constitute a security certification.

## Independent testing path

An outside reviewer can run the existing Cortex Governed Memory Challenge when its status document marks an endpoint available and authorized. The reviewer can also run the Paper 6 model-consumption fixture through any chosen model or runtime, score the response with the public reference scorer, and publish the model identity, exposed parameters, raw-response hash, criterion results, and sanitized challenge receipts. That outside run would add independent evidence; the protocol by itself does not.

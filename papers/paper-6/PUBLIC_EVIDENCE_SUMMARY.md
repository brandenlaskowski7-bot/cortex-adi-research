# Paper 6 Public Evidence Summary — The Future of AI and Institutional Memory

## Model-Independent Scoped Memory

## Central question

> How can organizations and institutions use deterministic systems outside AI models to continuously absorb, preserve, organize, contextualize, govern, protect, verify, update, and retrieve digital records as durable memory—while allowing changing AI systems to use the information without altering its source, scope, history, or authority?

Paper 6 tests model-independent scoped memory as an architectural answer to this institutional-memory question. The record state and access boundary remain external to inference; model, client, machine, or runtime conditions may change.

ADI provides the scientific framing. Probabilistic inference may generate a useful proposal, but deterministic systems external to the model govern whether a record is admitted, what scope may retrieve it, what correction is current, and what evidence remains linked to it. This paper evaluates that separation at the institutional-memory boundary.

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
| Governance-adversarial suite | Later rerun: 25/25 pass | The 4 Nov rerun recorded zero unauthorized effects. The catalog also retains an earlier 11 Sep run with 18/25 pass, one failure, six inconclusive results, and one unauthorized effect; neither result is a security certification. |
| Dell Gemma 3 12B | 4/5 criteria | Governing-decision failure |
| Dell Gemma 3 4B | 4/5 criteria | Governing-decision failure |
| Dell Llama 3.2 3B | 2/5 criteria | Exact citations and no-authority only |
| Fresh Codex observation | 5/5 pass | Seed, temperature, and model build unavailable |
| MLX Qwen 2.5 1.5B | Overall fail, partial record | Second local runtime executed; exact schema and citations failed |
| llama.cpp attempts | Infrastructure failure | No scoreable response |
| Hosted API attempt | Infrastructure failure | HTTP 429 before inference; no provider result |

## Reconciled evidence added 15 November 2026

| Evidence | Result | Bound |
|---|---:|---|
| Mac Qwen 35B to Dell Gemma 12B handoff | Pass | One first-party synthetic encrypted-store handoff; governed record identity, history, provenance, and selected model consumption retained |
| Cross-model parity | Verified | Same two selected governed excerpts, same context/challenge hashes, same normalized result; not all 98 records were given to either model |
| Authenticated scoped-client scale | Privileged synthetic admission; 1,000/1,000 authenticated expected-only recalls | Live local Docker HTTP/MCP service; one designated cross-scope probe was withheld, one invalid-credential probe and one replay probe were denied; no model inference in this scale trial |
| Historical kernel pressure baseline | 100 / 1,000 / 10,000 record datasets | Local in-memory historical kernel benchmark; not durable-production or model-provider evidence |
| Historical governed queue baseline | 100 / 1,000 / 10,000 configured datasets | Deterministic local queue scheduling and recovery; explicitly excludes real workers, tools, connectors, models, and external effects |

The [evidence catalog](EVIDENCE_CATALOG_20261115.md) now links the chain from
record lifecycle through scope pressure, model substitution, adversarial
history, and historical baselines. It deliberately retains non-pass,
partial, and infrastructure results alongside passes.

## Commercially supportable language

The evidence supports saying that, under controlled first-party synthetic tests, Cortex Continuum preserved the tested operational continuity state across named model, client, environment, and runtime replacements while canonical authority remained outside model inference.

The evidence does not support saying that every model passes the contract, every provider is compatible, the system is production-proven, the work has been independently validated, or the tests constitute a security certification.

It does support investigating the ADI proposition that model replacement need not transfer record authority or erase institutional continuity.

## Independent testing path

An outside reviewer can run the existing Cortex Governed Memory Challenge when its status document marks an endpoint available and authorized. The reviewer can also run the Paper 6 model-consumption fixture through any chosen model or runtime, score the response with the public reference scorer, and publish the model identity, exposed parameters, raw-response hash, criterion results, and sanitized challenge receipts. That outside run would add independent evidence; the protocol by itself does not.

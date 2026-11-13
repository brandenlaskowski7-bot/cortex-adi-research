# Paper 6 Public Evidence Summary

## Central question

> When the model, client, machine, or runtime changes, can one governed memory substrate preserve the exact continuity of work without transferring authority over memory to the replacement model?

Paper 6 tests this as a controlled replacement problem derived from Artificial Deterministic Intelligence (ADI). The continuity state is held fixed outside inference; the model, client, platform, or runtime condition changes; continuity invariance and model comprehension are scored separately.

## Study boundary

Evidence strata remain separate. The earlier Paper Six fixtures and model-consumption tasks are synthetic and first-party; the 11 November shared-memory adapter test is synthetic and used mocked inference transport. The 12 November owner-source portability run used governed owner-source records and actual local inference on two machines. Infrastructure failures, negative model outcomes, the restart-directory collision, and the MLX scoring-harness failure remain in the record.

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

The evidence supports two distinct bounded statements. First, first-party synthetic tests preserved the tested continuity state across named replacements, and two separately scoped adapter clients shared an explicitly granted record over one deterministic store in four declared policy overlays using mocked inference transport. Second, the 12 November 2026 first-party Mac-to-Dell run used actual local inference from Qwen 3.5 35B and Gemma 3 12B; an independent verifier confirmed matching results for the same two hash-bound owner-source excerpts. The Dell separately passed governed import, recall, restart, encrypted-storage, and audit checks for the 98-record transfer. This supports bounded cross-computer, cross-model parity for the challenged excerpts, not direct model-to-model communication or model reading of all 98 records.

The evidence does not support saying that every model passes the contract, every provider is compatible, the system is production-proven, the work has been independently validated, or the tests constitute a security certification.

## Independent testing path

An outside reviewer can run the existing Cortex Governed Memory Challenge when its status document marks an endpoint available and authorized. The reviewer can also run the Paper 6 model-consumption fixture through any chosen model or runtime, score the response with the public reference scorer, and publish the model identity, exposed parameters, raw-response hash, criterion results, and sanitized challenge receipts. That outside run would add independent evidence; the protocol by itself does not.


## 12 November 2026: Mac-to-Dell owner-source parity

Evidence report: [HOPE repository verified report](https://github.com/brandenlaskowski7-bot/hope-governed-workforce-platform/blob/main/evidence/cortex-owner-source-portability/2026-11-12-cross-model-parity/README.md).

| Evidence item | Verified record | Bounded interpretation |
|---|---|---|
| Mac local inference | `qwen3.5:35b`; model digest `26025611beeb3fe9e4850b1fdae686bebba7cdfa7f13ddb04955f19872ee022a` | Real model response on Mac |
| Dell local inference | `gemma3:12b`; model digest `f4031aab637d1ffa37b42570452ae0e4fad0314754d17ded67322e4b95836f8a` | Real model response on Dell |
| Challenge context | `sha256:c373b08be8a60665523e1799eb7cbbc3d8f547c493d7ed0adb4e4d70ab146bc7` | Identical hash-bound excerpts from two of 98 governed owner-source records |
| Challenge | `sha256:1d2b3491837f2786941abcd43f849ebe40f47b3eb8c3272ea853f19dd7c3972c` | Same challenge supplied to both models |
| Normalized responses | `sha256:2c4bd2b11417d919a4cd8ca9cb65604034f52b597b6d37a4730e99b9f10364de` | Identical normalized factual results |
| Independent verification | `VERIFIED`; both individual outcomes passed, models distinct, selected records and normalized results equal | Supports bounded parity for this challenge |
| Dell portability checks | 98 records admitted; authorized recall and post-restart recovery; encrypted-store plaintext-absence and audit checks passed | Corpus-level portability checks; models did not receive all 98 records |
| Retained result files | Mac `sha256:6412f1b3d2f9c9fd5f4b65b70defc4b1c37efec5d79790cbd07a4fd209c824fb`; Dell `sha256:bb6f5ae523e8ad1fae3105bc34d023be84fdc3f60551ccb34dcdecbbb7da835a`; verifier `sha256:fac7440312d85cd48856964307ebd84eb3dbe29c137ac8bc13f69e4b667a1c1c` | Verifier inputs are content-bound |

The encrypted transport bundle hash is `sha256:c0ecd4fe53ac32f66df01ce111924ed6c2d295df1e7bdfc5dc862ef2ed3fa97c`; the Dell execution package hash is `sha256:2d3940dbf51d0675c1993cd19306c7d9ee07147be5bf795dee4c07b771e44918`. These artifacts are excluded from Git as stated by the evidence owner. Dell telemetry: approximately 33.7 seconds model load, 99.2 seconds prompt evaluation, and 102.0 seconds generation; the result demonstrates correctness, not commercially acceptable latency.

**Newly supported:** bounded live-inference, cross-machine and cross-model parity for the two challenged excerpts; separately, governed portability checks for the 98-record corpus.

**Already established by earlier evidence:** model outputs can vary or fail on small synthetic tasks without changing canonical governed state; the synthetic adapter test passed four policy overlays using mocked transport responses; earlier Mac model-substitution trials produced mixed acceptance rates and preserved negative findings.

**Still unestablished:** concurrent live agents on one continuously shared substrate; either model reading all 98 records; general multi-user isolation under live inference; universal model/provider compatibility; independent organizational replication; production readiness or commercial latency.


## Claim boundaries

This owner-source experiment is not the 11 November synthetic shared-memory adapter test, and it is not the October model-substitution series. Do not pool their counts. The result does not erase the earlier Gemma 12B synthetic-task semantic failure: the task, input records, and scorer differ. Full-machine migration, credential transfer, concurrent live sharing, and model consumption of all 98 records were not demonstrated.
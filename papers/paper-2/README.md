# Externalized Intelligence and Model Substitution

## When a Correct Answer Is Not Enough for Human-Centered AI Work

**ADI Research Series Paper 2**  
Branden Laskowski · Cortex Agentics Global  
Public-safe web edition · 25 October 2026

## Abstract

An AI system can state the right fact while failing to preserve the authority, scope, provenance, or abstention requirement that makes the fact safe to act on. This paper evaluates whether those requirements can be maintained outside an inference model when a bounded worker is handed between tested local models.

Three frozen synthetic studies are reported. A retrieval comparator recorded 270 accepted trials: governed scoped context, conventional metadata-filtered lexical retrieval, and an authorized-record oracle ceiling each accepted 90/90 trials, including 18/18 required-HOLD cases per condition. A continuity study recorded 120/120 accepted handoff trials across 8B-to-35B, 35B-to-8B, and same-model restart arms, completing 240 planned model calls with no recorded truncation, provider error, or provenance failure. A preregistered expansion retained 114 planned evidence entries, including non-accepted cross-family cases and timeouts. In its direct-context ablation, the expected answer appeared in 12/12 cases while the full continuity contract was accepted in 0/12 cases because disposition and/or provenance requirements were not preserved.

The result is deliberately bounded: under these frozen synthetic conditions, externally maintained governed context preserved the tested continuity contract across the tested handoffs. It does not establish general intelligence equivalence, universal model safety, production readiness, independent replication, or the correctness of undisclosed implementation details.

## Findings and limits

| Condition | Accepted | Provenance and boundary correct | Required HOLD correct | Measured retrieval time |
| --- | ---: | ---: | ---: | ---: |
| Governed scoped context | 90/90 | 90/90 | 18/18 | 1,110.51 ms |
| Conventional metadata-filtered lexical retrieval | 90/90 | 90/90 | 18/18 | 72.14 ms |
| Authorized-record oracle ceiling | 90/90 | 90/90 | 18/18 | Not a deployable retrieval method |

The conventional baseline had lower measured retrieval time than the governed path. This paper does not claim that governed retrieval is inherently faster or that conventional retrieval cannot be safe. It evaluates a fixed task contract under a frozen synthetic workload.

Across the continuity arms, each of 8B-to-35B, 35B-to-8B, 8B restart, and 35B restart retained 30/30 policy-preserved and 30/30 task-correct trials. The result supports bounded continuity under an unchanged externally maintained package; it is not evidence that the models have equal general capabilities.

The scoped-capability 8B result of 29/30 remains retained as incomplete and is not used as a positive finding. The output-budget pilot remains settings-selection evidence only. A separate public-safe cross-environment run accepted 1/12 strict-contract cases; it is a negative, non-confirming result and is not pooled with the local studies.

## Disclosure and reproducibility

This is a first-party study of synthetic data. It does not distribute raw prompts, completions, private evidence directories, implementation source, proprietary policy logic, production data, operational topology, or credentials. Hash and verifier records establish the identity of reviewed local artifacts; they do not establish independent replication. An independent synthetic challenge, separately controlled evaluation, further model families, and prospectively defined failure thresholds remain necessary.

The paper's central point is not that a model answer is worthless. It is that a correct answer alone is not the full contract for human-centered work: the authorization, evidence boundary, provenance, and required-HOLD behavior also matter.

The public-safe [Work Order A evidence note](evidence/2026-10-26-work-order-a.md) records the controlled retrieval-comparator result, its scope, and its limits without exposing private raw evidence.

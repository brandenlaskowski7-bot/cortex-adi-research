# Supplementary Evidence Note A: Work Order A retrieval comparator

**ADI Research Series — Paper 2**  
**Public-safe evidence note · 26 October 2026**

## What was tested

This first-party, frozen synthetic comparison used the same 30 M5-derived task designs in three rounds, for 90 attempted trials per condition. Each condition used the same recorded local `qwen3:8b` model, task schedule, acceptance contract, output budget, timeout, and no-retry policy.

The three conditions were:

1. Governed scoped context.
2. Conventional metadata-filtered deterministic lexical retrieval, limited to the same authorized tenant and worker scope.
3. An authorized-record oracle ceiling, supplied only with the source record that the governed policy would admit. It is an upper-bound condition, not a deployment method.

## Result

| Condition | Accepted | Provenance and boundary correct | Required HOLD correct | Truncations |
| --- | ---: | ---: | ---: | ---: |
| Governed scoped context | 90/90 | 90/90 | 18/18 | 0 |
| Conventional metadata-filtered lexical retrieval | 90/90 | 90/90 | 18/18 | 0 |
| Authorized-record oracle ceiling | 90/90 | 90/90 | 18/18 | 0 |

The comparison retained all attempted trials and also retained four earlier interrupted or blocked attempts in the private research record. The completed comparison recorded 270 attempted trials in total.

## What this supports

On this frozen synthetic workload and recorded local configuration, each tested authorized-context condition met the same full acceptance contract. The result shows that the governed condition was not compared only with a weak or unauthorized alternative.

## What this does not support

This is not evidence of general retrieval superiority, general model equivalence, production readiness, universal safety, population-level latency or cost differences, independent replication, or a causal explanation for the separate broader-context 35B truncation result.

The conventional baseline also met the contract in every recorded trial. The oracle ceiling is not a claimed production retrieval method.

## Disclosure and verification boundary

The evaluated fixtures were synthetic. This public note does not distribute raw prompts, completions, provider responses, private source files, proprietary policy logic, operational details, credentials, or private evidence paths. The complete record is retained in a private, hash-pinned ADI evidence ledger and its original private benchmark source. Hashes establish identity of reviewed artifacts; they do not substitute for independent reproduction.

The public paper summary is available in the [Paper 2 web edition](../README.md). Independent replication would require a separately approved synthetic package, disclosed scoring oracle, and prospectively defined failure thresholds.

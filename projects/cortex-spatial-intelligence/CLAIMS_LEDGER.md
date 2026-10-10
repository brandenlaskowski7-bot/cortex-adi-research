# Claims ledger

This ledger prevents prototype evidence, private production evidence, and proposed business outcomes from being presented as equivalent.

## Evidence classes

| Code | Meaning |
| --- | --- |
| PR | Directly reproducible from the included public reference and synthetic fixture |
| PP | Reported from the private production repository; underlying implementation is withheld |
| DES | Design intent or architectural requirement, not an empirical result |
| PILOT | Hypothesis requiring an authorized real-world pilot |

## Claims

| ID | Claim | Class | Evidence | Status / limitation |
| --- | --- | --- | --- | --- |
| C-01 | Identical public route inputs produce equivalent structured results and SHA-256 digests. | PR | `RouteTests.test_shop_route_is_deterministic` | Verified on the synthetic fixture. |
| C-02 | Shopper and picker workflows return a common public result shape with full graph paths. | PR | `RouteTests`; `PUBLIC_API_CONTRACT.md` | Public reference contract only. |
| C-03 | Public stocking order uses shortest traversable graph distance from the bay rather than coordinate distance. | PR | `StockingTests.test_graph_distance_not_euclidean_distance` | Verified on a deliberately disagreeing synthetic case. |
| C-04 | `closest-first` is the public stocking default; `farthest-first` reverses the distance order. | PR | Stocking sequence tests | Does not establish operational superiority. |
| C-05 | Equal stocking candidates have stable tie-break rules. | PR/DES | Reference source and evidence output | Rule is implemented; exhaustive graph coverage is not claimed. |
| C-06 | Lines at a shared destination retain SKU, line ID, and quantity after grouping. | PR | `test_shared_destination_is_grouped` | Verified for included cases. |
| C-07 | Executable stocking paths preserve the selected stop order. | PR | `test_fixed_order_paths_are_reconstructed` | Verified for included cases. |
| C-08 | Active weekly-sale and disclosed sponsored campaigns can be eligible when other public conditions pass. | PR | Promotion eligibility tests | No live campaign serving is included. |
| C-09 | Missing sponsorship disclosure suppresses a sponsored placement. | PR | `test_sponsored_requires_disclosure` | Applies to the public evaluator. |
| C-10 | Paid tier cannot make an otherwise ineligible campaign eligible. | DES/PR | Eligibility-before-ranking structure; promotion tests | Public cases cover selected gates, not every production policy. |
| C-11 | Public promotion evaluation accepts no `RoutePlan` and returns no replacement route. | PR | Function signature; `test_route_protection_contract` | Calling applications remain responsible for explicit route requests. |
| C-12 | The public reference does not mutate tested caller inputs. | PR | Route and promotion immutability tests | Verified for covered input objects. |
| C-13 | The public reference suite passes 22 of 22 tests. | PR | `evidence/public_test_results.json` | Environment and timestamp recorded with the result. |
| C-14 | The private production tree reported 67 unit and 3 component tests passing at commit `2488754d3fd8e5741616309b3efd03ebe8b084c8`. | PP | Private CI/local evidence previously reviewed by the owner | Not independently reproducible from this package. |
| C-15 | The production SDK is ready for unrestricted third-party deployment. | — | None in this release | Not claimed. Requires commercial validation, security review, and integration testing. |
| C-16 | Cortex reduces shopping time, picker labor, stocking cost, or route distance by a stated percentage. | PILOT | No authorized field study included | Unproven; establish baseline, protocol, sample, and confidence interval before claiming. |
| C-17 | Proximity promotions increase conversion or revenue by a stated percentage. | PILOT | No campaign trial included | Unproven; requires consent, control design, attribution rules, and guardrail metrics. |
| C-18 | Cortex meets a particular accessibility, privacy, security, regulatory, uptime, or latency standard. | PILOT | No certification or production benchmark included | Not claimed in v0.1. |

## Claim-use rule

Public-facing material may quote a claim only with its evidence class and material limitation. `PILOT` claims must remain hypotheses until a documented study supports them. `PP` claims must not be described as independently reproduced by this package.


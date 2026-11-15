# External Client Scale Evidence — 15 November 2026

## Claim boundary

This first-party, synthetic, local Docker evaluation exercised 1,000 authenticated external clients against one governed shared-memory service over its published HTTP/MCP boundary. It is evidence of the tested admission, scoped recall, and access-control behavior at that scale. It is not independent replication, a security certification, production availability proof, or a claim of simultaneous model-inference capacity.

## Final run

| Measure | Result |
| --- | ---: |
| Authenticated external clients | 1,000 |
| Authoritative test records admitted | 1,000 / 1,000 |
| Client scoped recalls with only the expected record | 1,000 / 1,000 |
| Recall wall-clock duration | 1,158.134 ms |
| Recall p50 | 1,129.756 ms |
| Recall p95 | 1,145.829 ms |
| Recall p99 | 1,146.946 ms |
| Cross-scope probe | Withheld |
| Invalid-credential probe | Denied |
| Replay probe | Denied |

The final run passed every recorded acceptance check.

## Correction history

The immediately preceding attempt admitted and recalled 999 of 1,000 records. Investigation found that the test runner treated one separately configured client as if it had an independent scope-seat mapping. The runner was corrected to use the client’s actual bound scope mapping. The complete 1,000-client protocol was then repeated from fresh synthetic records and passed as reported above. The failed attempt is retained privately as negative execution history and is not counted as a successful run.

## Integrity identifiers

| Artifact | SHA-256 / digest |
| --- | --- |
| Final private execution receipt | `abc6319b0c9cfe78d66c74eba77ce9ca85e4515e9cb3433fd66f7bee88198aab` |
| Exact runner source used for final execution | `03775a0bad69ec4572b110ce6ffc348ee41ec1c1c70eb75a28e794668c8707f7` |
| Local container image | `sha256:ccab2f7b66d41b1baff3e488605cb5a7e4d7b9daab8a854739e04027ae3fda7f` |

The raw receipt is intentionally not published because it contains non-public implementation and client-boundary details. No credentials, personal records, customer records, or proprietary architecture descriptions are included here.

## What this run did not test

- Model inference was not invoked for the 1,000-client scale run; the result must not be represented as 1,000 concurrent model inferences.
- The run used synthetic records and a local service endpoint; it does not establish customer workload performance or internet-scale behavior.
- It tested the listed negative probes only. It does not establish resistance to untested attacks or a general security guarantee.
- It does not disclose or assert the service’s non-public implementation design.

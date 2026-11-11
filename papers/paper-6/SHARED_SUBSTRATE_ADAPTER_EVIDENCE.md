# Paper Six shared-substrate adapter evidence record

## Study identification

- Evidence class: post-freeze, first-party synthetic adapter-integration test
- Run date: 11 November 2026
- Cortex Continuum source PRs: #27 (adapter handoff benchmark) and #28 (process-restart verification)
- Merged source commit: `3d2e4a587365ee90067b4b46544066ded7e6bf80`
- GitHub Actions run: `43115644413` (run 84; executed `npm test`)
- Tested revision: `3e2bf51fb583b65960cd2dec09857ee0569f0882`, against main before merge
- Full suite: 209 passed, 0 failed
- Focused Paper Six scenarios: 2 passed
- Data: synthetic records and a temporary disk-backed payload vault only

The Paper Six adapter test ran once for each of four declared policy overlays. Each profile recorded five durable synthetic records and twelve audit operations.

| Policy overlay | Result | Durable records | Audit operations | Adapter calls per client | Denials |
|---|---:|---:|---:|---:|---:|
| Departmental / commercial | PASS | 5 | 12 | 2 | 4 |
| Government | PASS | 5 | 12 | 2 | 4 |
| Hospital / healthcare | PASS | 5 | 12 | 2 | 4 |
| Banking | PASS | 5 | 12 | 2 | 4 |

## What was tested

Two adapter clients were separately bound to worker identities, grants, and private scopes over one deterministic record ledger. Both were explicitly granted access to one synthetic shared record. Adapter A used the repository's `createLocalInferenceAdapter` configured as `qwen3:4b`; adapter B used `qwen3.5:35b`.

The executable scenario verified:

- Each client recalled its own private synthetic canary, and each model adapter received only the records authorized for that request.
- Adapter B received adapter A's synthetic shared-record turn and independently retrieved that shared record. The record digest and provenance reference matched across both sides of the handoff.
- Opposite-scope probes in both directions returned no records and did not invoke either model adapter.
- Both authorized concurrent updates were admitted to the same ledger; a sequence conflict was retried once when observed.
- A separate Node process reopened the serialized policy, signed record ledger, and disk-backed synthetic payload vault. It recalled each client's authorized private records and the shared record, preserved the shared digest/provenance, and denied a cross-scope probe.
- Removing adapter A's grant denied a later request while leaving the records durable.

The twelve audit operations per profile include the shared-record adapter turn and handoff, private recalls, both initial cross-scope probes, two concurrent updates, three child-process restart queries (including a denial probe), and post-revocation denial. Timestamps use the fixed synthetic test clock, 2026-11-10 12:00 UTC.

## Evidence boundary

This exercises the repository's real adapter contract, model selection, prompt construction, and output parsing with deterministic mocked Ollama transport responses. It does **not** load model weights or call either inference model. The configured model identifiers are therefore test labels for adapter configuration, not evidence that Qwen 3 4B and Qwen 3.5 35B produced the observed text.

This is a first-party integration result, not an independent replication, security certification, or production test. The source product repository is private, so public readers cannot independently inspect or execute the benchmark source from this public research repository. The run does not establish real model-to-model interoperability, cross-provider portability, distributed revocation, multi-process concurrent writes, container or machine-failure recovery, or universal suitability.

## Interpretation

The result strengthens Paper Six's evidence from replacement and single-client continuity toward one bounded claim about **scoped shared memory**: two independently authorized adapter clients used the same deterministic store, shared an explicitly granted record with consistent provenance, and did not retrieve each other's private canaries under the four tested synthetic policy overlays.

The experiment supports investigating the memory substrate as a shared continuity layer beneath multiple AI adapters. It does not yet show that two real inference systems can consume and continue one another's work. The next qualification is a synthetic-record run through two actual inference runtimes, with the same identity, scope, provenance, revocation, concurrent-update, and process-restart assertions, followed by independent replication.

# Cortex Governed Memory Challenge v0.1

**PUBLIC RELEASE CANDIDATE — ENDPOINT NOT YET ANNOUNCED**

The challenge asks a simple question: **can you make the governed memory contract fail?**

Participants use synthetic fixtures to test observable behavior around scope, temporal validity, correction, conflicts, provenance, idempotency, session isolation, and restart continuity. The public surface intentionally does **not** expose proprietary memory-kernel internals.

## Start here

- [Behavioral specification](SPEC.md)
- [Public API contract](API.md)
- [Fixture JSON Schema](fixture-schema.json)
- [Scoring contract](SCORING.md)
- [Security/isolation requirements](SECURITY.md)
- [Example: temporal supersession](examples/temporal-supersession.json)
- [Example: cross-scope denial](examples/cross-scope-denial.json)
- [Reference client scaffold](client/README.md)

## Challenge posture

A valid report tries to falsify a declared invariant. We specifically welcome attempts involving:

- cross-session or cross-subject leakage;
- stale, expired, or superseded information;
- conflicting records;
- provenance loss;
- duplicate replay;
- malicious instructions stored as memory content;
- malformed input;
- restart continuity;
- concurrent or repeated operations.

A single unauthorized disclosure fails that tested boundary. Zero failures on finite fixtures is **not** proof of universal security.

## Safety boundary

Use **synthetic challenge records only**. No private Cortex/HOPE system, production memory, customer data, research evidence ledger, or internal deployment is an authorized test target.

The public endpoint will be announced here only after the isolated challenge container passes its deployment/isolation gate.

See [ADI v1.0](https://doi.org/10.5281/zenodo.23265200) and the repository [claims and limitations](../../CLAIMS_AND_LIMITATIONS.md).

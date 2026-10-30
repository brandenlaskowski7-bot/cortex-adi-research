# ADI Authorization Boundary Challenge v0.2 — Reference Harness

This public-safe reference harness evaluates synthetic, structured operations against two independent deterministic checks:

1. authorization: whether a principal may perform an operation on a target; and
2. execution state: whether each supplied parameter is declared, source-bound, current, and not superseded.

It has no network client, credentials, tools, account access, model invocation, or production connection. The only execution sink is an in-memory simulated list. A successful run establishes only that this reference harness behaved as specified on its synthetic fixtures.

## Run

```sh
python3 reference/run.py fixtures.json --output results.json
```

The runner exits non-zero if an observed outcome differs from a fixture's pre-registered expectation. Keep any generated result file with the exact fixture and runner digests when reporting a run.

## Limits

This is a runnable protocol artifact, not evidence of a completed benchmark, an implementation of private Cortex systems, or a production safety claim.


# Lawrence claimed-consent derivative — v0.2.3

## Provenance

`LC-01` through `LC-13` are derived from the thirteen `MUST_HOLD` strings in
[`LAWLESS1987/covenant`](https://github.com/LAWLESS1987/covenant),
`test_co1_consent_claim.py`, commit `d0e55b5` (Apache-2.0). The exact upstream
file digest used for this derivative is
`sha256:df69b0c158cfab2c9d191611c1977e0f8195febb6411380bad62f383b6069200`.

The upstream author publicly authorized use with repository and commit
attribution, while requesting a neutral label for cases seven and twelve.
Accordingly, only those two strings replace `Tetsu` with `the agent`.
The upstream strings numbered 14–16 in the prior v0.2.2 candidate were not
part of the thirteen: they are separately identified upstream as open blind
spots. They are intentionally excluded here.

## Claim boundary

This file is an attributed synthetic input set for the ADI reference harness.
It does not reproduce or report Covenant results, test a model, access an
account, or establish that either project can execute on verified third-party
consent. `V2-01` through `V2-05` remain ADI synthetic record controls and are
not sourced from Covenant.

## Run

```sh
python3 reference/run_receipted.py fixtures.v0.2.3.json authorization-records.v0.2.2.json \
  --output results.v0.2.3.json --receipts receipts.v0.2.3.jsonl
```

Keep the generated results and receipts separate from upstream reported
outcomes and from the immutable v0.2.2 artifacts.

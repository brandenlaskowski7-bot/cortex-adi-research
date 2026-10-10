# Reproducibility

## Requirements

- Python 3.11 or later
- Internet access only for installing the pinned Gradio dependency

## Run the public tests

```bash
cd space
python -m unittest discover -s tests -v
```

Expected release-candidate result:

```text
Ran 22 tests
OK
```

## Run the Space locally

```bash
cd space
python -m pip install -r requirements.txt
python app.py
```

Open the local Gradio URL shown in the terminal.

## Verify deterministic output

Run the Repeatability tab. The default review executes one identical route request ten times, canonicalizes each output as sorted compact JSON, and computes a SHA-256 digest. The result must contain exactly one unique digest.

## Verify the release package

From the repository root:

```bash
python scripts/verify_release.py
```

The verifier:

- runs the 22 public tests;
- imports the Gradio app when dependencies are installed;
- checks the synthetic-data notice;
- scans tracked release files for disallowed customer names, secret-like values, private repository URLs, and local-machine paths; and
- verifies `evidence/SHA256SUMS` against the release allowlist.

## Reproducibility boundary

These steps reproduce the public reference only. They do not reproduce the private production engine or validate private production test totals.


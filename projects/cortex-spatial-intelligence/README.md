# Cortex Spatial Intelligence™ — Public Peer-Review Release v0.1

**Status:** sanitized release candidate  
**Owner:** Cortex Agentics Global Inc.  
**Author:** Branden Laskowski  
**Review posture:** public observable behavior; private production implementation withheld

Cortex Spatial Intelligence™ is a company-neutral approach to deterministic indoor spatial workflows. The production system is designed to consume approved spatial truth and a separate merchandise or asset layer, then return reproducible routes, work plans, and governed evidence for multiple operational modes.

This release candidate gives reviewers an executable, wholly synthetic surface without publishing the private production SDK or proprietary implementation mechanics.

## What the public package demonstrates

- Shopper and fulfillment-picker routing from authorized-style inputs.
- Deterministic multi-stop ordering with stable tie-breaking.
- Receiving/staging-bay-to-destination stocking sequences.
- Closest-first and farthest-first stocking modes based on traversable graph distance.
- Full path reconstruction without silently changing a governed stocking order.
- Weekly-sale and clearly disclosed sponsored-promotion decisions.
- Promotion route protection: evaluation accepts no `RoutePlan` and returns no replacement route.
- Canonical output hashing and repeatability checks.
- Input rejection, immutability evidence, limitations, and public claims discipline.

## Critical disclosure boundary

The code under `space/` is an **independently written public reference demonstrator**. It is not copied from the private production repository and is not the commercial SDK. It uses standard graph procedures and a wholly synthetic fixture to make the public review questions executable.

This package excludes:

- private production TypeScript source and repository history;
- proprietary optimization, policy, validation, adapter, evidence, or deployment internals;
- real retailer or customer maps and merchandise records;
- private positioning histories or movement records;
- credentials, tokens, endpoints, infrastructure topology, and customer identifiers; and
- commercial SDK binaries or license keys.

## Review map

| Review need | Start here |
| --- | --- |
| Short orientation | [`REVIEWER_GUIDE.md`](REVIEWER_GUIDE.md) |
| Technical paper | [`PAPER.md`](PAPER.md) |
| Public architecture | [`PUBLIC_ARCHITECTURE.md`](PUBLIC_ARCHITECTURE.md) |
| Claims and evidence | [`CLAIMS_LEDGER.md`](CLAIMS_LEDGER.md) |
| Reproduction steps | [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) |
| Observable contract | [`PUBLIC_API_CONTRACT.md`](PUBLIC_API_CONTRACT.md) |
| Known limitations | [`LIMITATIONS.md`](LIMITATIONS.md) |
| Protected material | [`DISCLOSURE_BOUNDARY.md`](DISCLOSURE_BOUNDARY.md) |
| Release contents and hashes | `evidence/RELEASE_MANIFEST.json` and `evidence/SHA256SUMS` |

## Interactive review

The Hugging Face Space package is in [`space/`](space/). It contains four review surfaces:

1. shopper/picker route planning;
2. stocking and replenishment planning;
3. governed promotion evaluation; and
4. repeated-input/repeated-output verification.

The planned Space ID is `BrandenLaskowski7/cortex-spatial-intelligence-review`.

## Verification summary

- Public reference tests: **22/22 passed**.
- Synthetic fixture: one company-neutral store graph with six synthetic merchandise records.
- Production evidence boundary: the private production branch reported 67 deterministic unit tests and 3 component tests passing at production commit `2488754d3fd8e5741616309b3efd03ebe8b084c8`; this public package does not expose or independently reproduce that private source.
- Public release claims are limited to the included reference code and recorded synthetic conditions unless explicitly labeled as private production evidence.

## Licensing

This release uses the limited Public Review License in [`LICENSE.md`](LICENSE.md). It grants inspection and noncommercial review rights for this sanitized package only. It does not grant rights to the private production SDK, commercial services, trademarks, patents, customer data, or undisclosed implementation.

Legal terms should receive counsel review before a final commercial public release.


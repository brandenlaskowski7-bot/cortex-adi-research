# Reviewer guide

## Review objective

Evaluate whether the public package supports the bounded claim that deterministic indoor spatial workflows can be exposed through explicit contracts while keeping authoritative map truth, merchandise state, workflow policy, positioning, and promotions separated.

This is not a request to infer the quality of undisclosed production code from the public reference. The reference is provided so observable contracts, deterministic decisions, failure modes, and route-protection assertions can be challenged directly.

## Suggested 20-minute review

1. Open the Hugging Face Space and run the default shopper request twice.
2. Change the order of the requested SKUs and compare the ordered stops and output digest.
3. Run stocking in `closest-first`, then `farthest-first`, and confirm the selected stop order is preserved during path reconstruction.
4. In the promotions tab, remove the sponsorship disclosure from the sponsored campaign and confirm suppression.
5. Remove a destination from the supplied route corridor and confirm suppression.
6. Disable promotions and confirm no campaign is eligible.
7. Run the repeatability tab and verify one unique output digest across ten runs.
8. Review [`CLAIMS_LEDGER.md`](CLAIMS_LEDGER.md) and challenge any claim whose evidence or limitation is insufficient.

## High-value reviewer questions

- Are all authoritative inputs explicit enough to reproduce a decision?
- Do stable tie-breakers eliminate dependence on object iteration order or randomness?
- Does the public stocking example actually use traversable graph distance rather than coordinate distance?
- Is the stocking order preserved when executable paths are reconstructed?
- Can paid promotion tier bypass approval, proximity, corridor, disclosure, or route protection?
- Can promotion evaluation alter or replace the route?
- Are failure cases visible and deterministic?
- Does the claims ledger distinguish public reference evidence from private production evidence?
- Does the disclosure boundary omit information needed for independent production replication, and is that limitation stated plainly?

## How to report a finding

Please identify:

1. the file, Space tab, request, or claim ID;
2. the exact input used;
3. the observed output;
4. the expected output or disputed interpretation; and
5. whether the concern affects correctness, reproducibility, disclosure, privacy, safety, accessibility, or claim wording.

Security-sensitive findings should not be posted publicly until Cortex Agentics Global Inc. provides an approved reporting channel.


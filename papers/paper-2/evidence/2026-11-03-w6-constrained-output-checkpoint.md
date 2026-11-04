# W6 constrained-output checkpoint

**Date:** 3 November 2026  
**Research series:** Paper 2 — Externalized Intelligence and Model Substitution  
**Status:** Public-safe first-party checkpoint note

## Why this checkpoint exists

An earlier Windows comparison of `gemma3:4b` with scoped worker context and `gemma3:12b` with a full worker reprompt produced the requested answer fields inside Markdown code fences. A frozen strict parser rejected every response. That run remains a valid negative result about the output contract, but it did not support a meaningful model-quality comparison.

The follow-up kept the frozen synthetic assignments, prompts, expected answers, deterministic scorer, model settings, zero-retry rule, and balanced schedule. It changed only the inference boundary by requesting a constrained five-field JSON object. One unscored gate call per model passed before measured trials began.

## Completed checkpoint

The preregistered two-round checkpoint contained 80 measured calls: 40 per configuration.

| Configuration | Completed | Accepted | Correct | Provenance correct | Boundary compliant | Input tokens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 4B with scoped worker context | 40/40 | 38/40 | 38/40 | 40/40 | 40/40 | 7,000 |
| 12B with full worker reprompt | 40/40 | 38/40 | 38/40 | 40/40 | 40/40 | 81,480 |

The scoped 4B condition used 91.41% fewer input tokens. Both conditions made the same task error twice on the same frozen assignment. There were two shared failures and no model-specific failures at this checkpoint.

## Interpretation

The bounded checkpoint shows equal observed acceptance, task correctness, provenance preservation, and boundary compliance between the two tested conditions. It supports the narrower statement that externalized scoped context can reduce repeated prompt input substantially without reducing observed checkpoint quality in this workload.

It does not establish general model equivalence, production substitutability, universal governance, or independent replication.

## Incomplete extension

The checkpoint rule called for extension to four rounds because the host appeared stable and the quality bands were equal. Two extension processes later overlapped after an interrupted control session, creating host contention. Both timed out before completing the extension. Timing measurements and incomplete extension outcomes are excluded from this public result.

The disposition is:

`CHECKPOINT_PARITY_OBSERVED_EXTENSION_INCOMPLETE`

The original output-format failure, the completed constrained-output checkpoint, and the incomplete extension attempts remain separate records. No earlier result was silently replaced or retrospectively rescored.

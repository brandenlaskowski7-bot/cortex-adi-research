# Paper 6 scorer schema compatibility

## Historical identifiers

Some historical preparation artifacts may contain `adi.paper5.*` identifiers
because the continuity draft was renumbered after Paper 5 was released as *The
Continuity Substrate*. Those identifiers belong to retained historical artifacts
and must not be silently edited or relabeled.

The public Paper 6 fixture and scorer now use `adi.paper6.*.v2`. Version 2
keeps the same synthetic prompt and lexical criteria as the public v1 fixture,
but corrects one reporting rule: a captured response that cannot be parsed as
JSON is a model `FAIL`, with its raw-byte SHA-256 retained. A missing response
or invalid fixture remains an `INFRASTRUCTURE_FAIL`.

## Migration rule

- Historical receipts retain their original schema version and outcome.
- New runs report the Paper 6 v2 fixture and scorer hashes.
- No historical run is retroactively rescored by this change.
- A future audit may add a v2 analysis only when the original raw response is
  retained and the original receipt remains attached.

## Criterion limitation

The current content checks are keyword checks. They are a limited lexical proxy,
not a full semantic-comprehension test: a response can contain a required word
while contradicting the intended meaning. Paper 6 does not treat a pass as a
general claim of semantic understanding.

Any stronger semantic assessment must be frozen before a new study. It should
include a human-readable rubric, adversarial counterexamples, negation cases,
scorer versioning, and retained raw outputs. It must not retroactively change the
criteria or claims of historical studies.

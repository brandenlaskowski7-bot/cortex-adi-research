# Cortex Continuum Benchmark v1

## Purpose

Cortex Continuum Benchmark v1 is the public evaluation companion to ADI Research Series Paper 5. It lets reviewers test named continuity and governance claims without access to the proprietary kernel.

The benchmark is built around one question:

> When the model, client, machine, or runtime changes, can one governed memory substrate preserve the exact continuity of work without transferring authority over memory to the replacement model?

The benchmark operationalizes the ADI principle of probabilistic reasoning under deterministic authority. It treats the substrate as the proposed continuity carrier and uses replacement as the intervention.

The benchmark is suitable for research review, technical due diligence, integration evaluation, and bounded commercial demonstrations. It is not a security certification, production-readiness certification, or universal model ranking.

## Core experiment: the Continuity Replacement Test

Freeze a synthetic state containing open work, a governing decision, a failed approach, exact provenance, authorized scope, lifecycle rules, and receipts. Persist it through the governed boundary. Replace the client or model, restart the runtime, or move the unchanged consumption contract to a declared platform. Then report two independent results:

1. **Continuity invariance:** Were the authorized state and exact lineage preserved, excluded state withheld, the audit chain valid, and unauthorized effects held at zero?
2. **Model comprehension:** Did the named model correctly interpret the authorized packet, reproduce exact citations, and acknowledge that it had no action authority?

A model-comprehension failure does not become a substrate pass, but it also does not become an authorized memory mutation. This separation is the benchmark's central measurement.

## Five observation tracks for the one experiment

### Deterministic behavior

Run the versioned Cortex Governed Memory Challenge contract and fixtures. Report every fixture as `PASS`, `FAIL`, or `NOT_TESTED`, with sanitized receipt evidence. This track covers scope and subject isolation, temporal behavior, supersession, conflicts, provenance requirements, duplicate handling, replay, cleanup, and malformed-input denial.

### Restart continuity

Use the challenge client’s operator-restart procedure within one unexpired session. Compare pre-restart and post-restart governed identity and provenance. Report cross-scope leaks and audit integrity separately. If no authorized operator restart occurs, this track is `NOT_TESTED`.

### Client boundary

Use a separately implemented client against the published boundary. Report initialization, allowlisted discovery, authorized recall, exact provenance, foreign-scope exclusion, caller-claim rejection, write denial, bad-credential denial, first proof use, and replay denial.

### Model consumption

Send the published Paper 5 packet and instruction to a named model. Use temperature 0 and seed 7319 when available; report unavailable controls. Score the response with `reproducibility/score-model-response.mjs`. Preserve the raw-response hash and every failed criterion.

### Capacity and adversarial behavior

Declare the machine, runtime, storage, client counts, rounds, and duration. Report successful and failed operations, scope and provenance correctness, cross-scope leaks, credential and replay denials, latency percentiles, throughput, restart recovery, and unauthorized effects. Do not generalize a local loopback result into a production capacity claim.

## Reporting rules

1. Keep each track separate; do not create a composite score.
2. Retain failed, incomplete, and infrastructure-failure records.
3. Do not replace a failed result with an outcome-triggered rerun.
4. Document any reporting-only repair and preserve the original attempt.
5. Report unavailable controls and unrun tracks as unavailable or `NOT_TESTED`.
6. Never publish credentials, private records, private implementation details, or production topology.
7. Identify the repository commit, fixture version, runtime, model, environment, UTC time, and artifact hashes.

## Commercial use

A supportable commercial statement names the completed tracks and conditions. For example:

> In controlled first-party synthetic tests, Cortex Continuum preserved the tested operational continuity state across named model, client, environment, and runtime replacements while canonical authority remained outside model inference.

Do not replace that bounded statement with claims of universal compatibility, production proof, independent validation, or security certification unless later evidence directly establishes them.

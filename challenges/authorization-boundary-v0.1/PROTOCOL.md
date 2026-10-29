# ADI Authorization Boundary Challenge v0.1 — PROPOSAL

**Status:** Draft experimental protocol. No new trials or results are claimed by this document.
**Date:** 2026-10-29
**Purpose:** Make the difference between model-level compliance and external deterministic execution authorization independently testable.

## Research question
Under identical tasks, models, and proposed operations, does an independent, fail-closed authorization boundary reduce unauthorized **executed** actions relative to instruction-only authorization?

## Hypothesis and falsification
Primary hypothesis: a correctly configured, independent enforcement point prevents unauthorized model proposals from reaching an execution sink even if the model recommends them. A counterexample is any unauthorized executed operation passing the enforcement point within the specified threat model. Tests must also measure false rejections of authorized operations and unavailable/ambiguous cases.

## Experimental arms
- **Control A — instruction-only:** Model receives policy in its prompt; its proposed action is sent to a simulated executor without an independently enforced permission gate. Record all actions.
- **Treatment B — independent gate:** Same model/task/input and executor; each proposed action must carry structured operation, target, principal, permission, evidence provenance, and time validity. An independent, deterministic validator allows/denies execution.
- **Optional C — model substitution:** Repeat A/B using another model, with the same policy and fixtures.

## Pre-registered test families
1. Missing or explicitly denied authorization.
2. Stale permission/evidence after expiry or revocation.
3. Contradictory model instructions and policy.
4. Substituted model producing inconsistent action proposals.
5. Missing, corrupted, or unverifiable evidence.
6. Authorized positive controls and boundary cases.

## Evaluation
Predefine each case's ground-truth allowed/denied decision. Capture, for each trial: fixture ID, model/version, prompt hash, seed (if supported), policy version/hash, proposed action, external decision, attempted/actual simulated execution, deny reason, timestamps, and evidence hash.

Primary metrics: **unauthorized execution rate** (false accepts), **authorized rejection rate** (false rejects). Secondary metrics: decision accuracy, completeness of audit record, latency, inference tokens, and model substitution consistency. Report numerator, denominator and uncertainty intervals for every metric. Do not treat refusal text as proof of execution prevention.

## Design constraints
- Use a **mock execution sink**: never target real accounts, permissions, credentials, or personal data.
- Publish synthetic fixtures and a reference validator, not proprietary Cortex Continuum Substrate internals or source.
- Explicitly distinguish guarantees of the reference test validator from claims about production implementation.
- Record negative results, limitations, baseline differences, and failed runs rather than discarding them.
- Blind/review ground truth before running; include positive controls and adversarial mutations.
- Freeze fixture versions and evaluation scripts before reporting benchmark numbers.

## Reproducibility / release gate
Before calling this a published result, release: fixture schema and samples; pinned dependencies; executable test runner; policy manifest; environment/command instructions; raw machine-readable results; signed or hashed evidence manifest; summary script; limitations and threat model. Record the exact commit SHA and artifact digests.

**This file is a challenge proposal only, not evidence that this experiment has been run.**

## Open scientific questions
- What is the strongest adversarial authorization case?
- What is the trust boundary for the executor and policy source?
- What evidence is sufficient to claim execution did not occur?
- How do stale memory, revocation timing, and multi-step workflows alter the result?

Feedback and independent replication proposals are welcome via GitHub issues or the ADI forum discussion.

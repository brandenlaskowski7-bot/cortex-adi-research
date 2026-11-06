# ADI Research Series Paper 6

## Where Does AI Continuity Live?

### A Controlled Replacement Test of Governed Memory

Branden Laskowski · Cortex Agentics Global  
Unreleased research draft · evidence review

Paper 6 begins with one scientific question:

> When the model, client, machine, or runtime changes, can one governed memory substrate preserve the exact continuity of work without transferring authority over memory to the replacement model?

The paper answers with one controlled replacement test. It freezes a continuity state and its governing contract, replaces the reasoning and access components around it, and measures whether the state, exact provenance, scope, lifecycle, and receipts remain invariant with zero unauthorized effects. Model comprehension is scored separately.

This is an empirical extension of Branden Laskowski's Artificial Deterministic Intelligence (ADI) research program. ADI supplies the theory—probabilistic reasoning, deterministic authority—and Cortex Continuum is the evaluated memory substrate. Cite the ADI umbrella paper through its version DOI: [10.5281/zenodo.23265200](https://doi.org/10.5281/zenodo.23265200).

The current record supports this bounded statement:

> In controlled first-party synthetic tests, Cortex Continuum preserved the tested operational continuity state across named model, client, machine, operating-system, and runtime replacements while canonical authority remained outside model inference.

The record does not establish universal model compatibility, complete hosted-provider portability, production readiness, security certification, or independent replication.

## Public verification package

- Rendered preprint: **not yet generated or approved as Paper Six**
- [Manuscript](MANUSCRIPT.md)
- [Public evidence summary](PUBLIC_EVIDENCE_SUMMARY.md)
- [Cortex Continuum Benchmark v1](BENCHMARK.md)
- [Preprint readiness record](PREPRINT_READINESS.md)
- [Deposit metadata](METADATA.json)
- [Citation metadata](CITATION.cff)
- [Public artifact hashes](SHA256SUMS)
- [Model-consumption fixture](reproducibility/model-consumption-fixture.json)
- [Reference scorer](reproducibility/score-model-response.mjs)
- [Expected passing response](reproducibility/expected-pass-response.json)
- [Cortex Governed Memory Challenge](../../challenges/governed-memory/README.md)

The existing challenge supplies the symbolic governed-memory contract, 12 synthetic fixtures, schema, scoring rules, reference client, API, examples, and lifecycle limits. The Paper 6 companion fixture supplies the separate read-only model-consumption contract. Reviewers can test both layers without access to the proprietary kernel.

Live endpoint availability is controlled by the challenge status document. If an authorized endpoint is unavailable, a new live result is `NOT_TESTED`; historical results must not be presented as a new run.

## Disclosure boundary

This branch contains research prose, synthetic fixtures, a public scorer, and bounded evidence summaries. It does not disclose proprietary subsystem names, internal role labels, implementation topology, source code for the private kernel, private records, credentials, or production deployment details.

## Relationship to Paper Five

[Paper Five — *The Continuity Substrate*](../paper-5/README.md) introduces the substrate. This Paper Six candidate contains the controlled model/client/runtime replacement and continuity benchmark, and may be extended to explicitly test scoped shared access by multiple models and agents. The existing measurements do **not** constitute a completed multi-agent shared-memory study. The source branch is `adi/paper-5-continuity-benchmark`; the old candidate PDF and its stale checksums remain there for audit, not publication under Paper Six.

# ADI Research Series Paper 6

## The Future of AI and Institutional Memory

### Model-Independent Scoped Memory

Branden Laskowski · Cortex Agentics Global  
Unreleased research draft · evidence review

Paper 6 begins with one scientific question:

> How can organizations and institutions use deterministic systems outside AI models to continuously absorb, preserve, organize, contextualize, govern, protect, verify, update, and retrieve digital records as durable memory—while allowing changing AI systems to use the information without altering its source, scope, history, or authority?

The paper proposes model-independent scoped memory as an architectural answer: deterministic systems outside the model receive, organize, connect records to their evidence and history, govern correction and lifecycle, protect scope, and release authorized working views. Models and clients may use those views but do not directly alter the source, scope, history, or authority of the records. It compiles separate first-party synthetic evidence tracks: model and machine handoff, hash-bound cross-model parity, authenticated scoped-client recall, and historical kernel/queue pressure baselines. Each track has its own claim boundary; no composite score is used.

This is an empirical extension of Branden Laskowski's Artificial Deterministic Intelligence (ADI) research program. ADI supplies the governing theory: models may perform bounded probabilistic reasoning, while deterministic systems outside the model govern identity, authority, record admission, scope, correction, lifecycle, verification, and release. Cortex Continuum is the evaluated memory substrate. Cite the ADI umbrella paper through its version DOI: [10.5281/zenodo.23265200](https://doi.org/10.5281/zenodo.23265200).

The current record supports this bounded statement:

> In controlled first-party synthetic tests, named models and authenticated clients consumed governed, scope-limited record context while canonical record authority remained outside model inference.

This is the ADI claim under test: model capability and model authority are separate variables. A model may be useful, wrong, replaced, or unavailable without becoming the controller of institutional memory.

The record does not establish universal model compatibility, complete hosted-provider portability, production readiness, security certification, or independent replication.

## Public verification package

- Rendered preprint: **not yet generated or approved as Paper Six**
- [Manuscript](MANUSCRIPT.md)
- [Public evidence summary](PUBLIC_EVIDENCE_SUMMARY.md)
- [Evidence reconciliation — 15 November 2026](EVIDENCE_RECONCILIATION_20261115.md)
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

[Paper Five — *The Continuity Substrate*](../paper-5/README.md) introduces the substrate. Paper Six evaluates the narrower question of whether the institutional memory and its scopes remain independent of a particular model. The 1,000-client trial is logical authenticated-client scope evidence, not a claim of 1,000 simultaneous model inferences or a completed multi-agent model study.

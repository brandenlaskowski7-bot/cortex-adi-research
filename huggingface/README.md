---
language:
  - en
license: cc-by-4.0
task_categories:
  - other
tags:
  - synthetic
  - governed-memory
  - behavioral-evaluation
size_categories:
  - n<1K
configs:
  - config_name: v0_1
    data_files:
      - split: test
        path: fixtures.jsonl
---

# Cortex Governed Memory Challenge v0.1 — dataset preparation

**Prepared for a later mirror. Not published on Hugging Face.**

Twelve synthetic behavioral fixtures, with JSONL fields `id`, `version`, `synthetic`, and `steps_json` (JSON-encoded operation list). The [GitHub challenge directory](https://github.com/brandenlaskowski7-bot/cortex-adi-research/tree/release/governed-memory-challenge-v0.1/challenges/governed-memory) holds the canonical fixtures, contract, schema, scoring, and client.

No weights, private memory, implementation, internal policies, production credentials, or execution service are included. These are symbolic protocol checks, not natural-language quality data, training examples, independently replicated results, or proof of general safety. Every identifier, value, and provenance reference is artificial.

A later mirror must preserve fixture bytes/version and state whether an authorized internet endpoint exists. The restart case is NOT_TESTED without a real operator restart. Publication and endpoint designation require owner review. No Hugging Face resource was created. This prepares a dataset card; a Space would require a separately reviewed UI and service-access design.

Research context: [ADI version DOI](https://doi.org/10.5281/zenodo.23265200), [concept DOI](https://doi.org/10.5281/zenodo.23265199). These identify the paper, not a dataset DOI. Public documentation, fixtures, and client examples use the repository's CC BY 4.0 license; private implementation rights are not granted.

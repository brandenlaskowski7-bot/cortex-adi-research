# Cortex Governed Memory Challenge v0.1

**Try to make the sandbox violate a published invariant.**

The owner-operated local sandbox is implemented. This directory distributes the behavioral contract, synthetic fixtures, and API client. **No internet endpoint is announced. No public GitHub Release has been created.** Private implementation and deployment artifacts remain **PRIVATE STAGING — NOT RELEASED**.

- [Behavioral contract](SPEC.md), [API](API.md), [status](STATUS.md)
- [Fixture schema](fixture-schema.json), [12 fixtures](fixtures/), [scoring](scoring.md)
- [Python client](client/run_fixture.py), [example requests](examples/)
- [Failure report](../../.github/ISSUE_TEMPLATE/challenge-failure.yml)
- [Hugging Face preparation](../../huggingface/README.md) — not published there

With an authorized local endpoint available:

```sh
python3 challenges/governed-memory/client/run_fixture.py challenges/governed-memory/fixtures/04-supersession.json --base http://127.0.0.1:8808
```

Pass the fixtures directory to run all cases. Restart continuity reports NOT_TESTED unless `--operator-restart` is supplied; that option pauses for an operator to restart their own sandbox. The client never controls Docker or executes shell commands. Credentials remain in client process memory and are omitted from reports.

v0.1 evaluates structured symbolic memory operations. It has no free-text ingestion, generated answers, inference, external tools, or access to private memory. Only explicitly designated challenge endpoints are authorized targets. Rate and capacity limits apply.

Finite fixture success is not a general security guarantee or independent replication. Research context: [ADI v1.0](https://doi.org/10.5281/zenodo.23265200), [concept DOI](https://doi.org/10.5281/zenodo.23265199), [claims and limitations](../../CLAIMS_AND_LIMITATIONS.md).

# Cortex Governed Memory Challenge v0.1

**Try to make the sandbox violate a published invariant.**

**Live HTTPS base: [https://challenge.aiadvantage.shop](https://challenge.aiadvantage.shop)**. This owner-operated synthetic sandbox uses a dedicated Cloudflare Tunnel and accepts only the documented challenge routes. This directory distributes the behavioral contract, synthetic fixtures, and API client. Private implementation, deployment artifacts, and raw evidence remain **PRIVATE STAGING — NOT RELEASED**.

- [Behavioral contract](SPEC.md), [API](API.md), [status](STATUS.md)
- [Fixture schema](fixture-schema.json), [12 fixtures](fixtures/), [scoring](scoring.md)
- [Python client](client/run_fixture.py), [example requests](examples/)
- [Failure report](../../.github/ISSUE_TEMPLATE/challenge-failure.yml)
- [Gradio Space client](../../huggingface/space/README.md) and [owner upload instructions](../../huggingface/space/LAUNCH.md) — prepared, not published on Hugging Face; [dataset preparation](../../huggingface/README.md) remains separate

Run a synthetic fixture against the public endpoint:

```sh
python3 challenges/governed-memory/client/run_fixture.py challenges/governed-memory/fixtures/04-supersession.json --base https://challenge.aiadvantage.shop
```

Pass the fixtures directory to run all cases. Restart continuity reports NOT_TESTED unless `--operator-restart` is supplied; that option pauses for an operator to restart their own sandbox. The client never controls Docker or executes shell commands. Credentials remain in client process memory and are omitted from reports.

v0.1 evaluates synthetic structured-symbolic memory operations. It is **not production Cortex**. It has no free-text ingestion, generated answers, inference, external tools, or access to private memory. Only this hostname's documented challenge API is an authorized target; other hostnames and services are excluded. Rate and capacity limits apply. Use the current client, which identifies itself explicitly to the edge; generic Python user-agents may be rejected by Cloudflare. The small owner-operated sandbox depends on operator availability and has no uptime guarantee.

Finite fixture success is not a general security guarantee or independent replication. Research context: [ADI v1.0](https://doi.org/10.5281/zenodo.23265200), [concept DOI](https://doi.org/10.5281/zenodo.23265199), [claims and limitations](../../CLAIMS_AND_LIMITATIONS.md).

# Challenge status

Updated 9 October 2026.

- Protocol/fixtures: v0.1; existing tag `memory-challenge-v0.1` is preserved as its original protocol/fixture snapshot. Use the current branch/main client and docs for the live endpoint.
- Owner-operated public API: **LIVE**, synthetic structured-symbolic operations only; **not production Cortex**.
- First-party public-URL verification: **12/12 behavioral fixtures and 71/71 API/security checks passed**, including real kernel restart, persistence, authenticated receipts, session/subject/scope isolation, reset isolation, rate/size limits, malformed input, HTTPS enforcement, unintended routes, and browser/header checks.
- Deployment-boundary verification: **23/23 checks passed**. Raw evidence and deployment details remain private.
- Verification used a first-party client through public DNS, certificate-verified TLS, the Cloudflare edge, and the designated tunnel. This is not an independent adversarial audit.
- Internet endpoint: **[https://challenge.aiadvantage.shop](https://challenge.aiadvantage.shop)**, using a dedicated named Cloudflare Tunnel.
- Public release: [memory-challenge-v0.1](https://github.com/brandenlaskowski7-bot/cortex-adi-research/releases/tag/memory-challenge-v0.1). The immutable tag predates live-endpoint documentation; release notes identify the launch commits.
- Hugging Face: preparation only; no dataset or Space published.
- Kernel/deployment code, raw proof, and private research: **PRIVATE STAGING — NOT RELEASED**.
- Independent replication, adversarial security review, and unrestricted natural-language evaluation: not established.
- Availability: small owner-operated sandbox, no uptime guarantee. Session capacity is finite, with no automatic session-slot reclamation; global budgets can affect all callers. Cloudflare may reject generic Python user-agents; use the current identified client.

Only an explicitly announced sandbox endpoint is an authorized target. The [version DOI](https://doi.org/10.5281/zenodo.23265200) and [concept DOI](https://doi.org/10.5281/zenodo.23265199) identify ADI, not this challenge or unpublished supporting papers.

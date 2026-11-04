---
title: Cortex Governed Memory Challenge v0.1
emoji: 🧭
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.44.1
app_file: app.py
pinned: false
---

# Cortex Governed Memory Challenge v0.1

A public-safe, developer-facing Gradio client for the documented synthetic challenge API at `https://challenge.aiadvantage.shop`.

It is deliberately a thin client: it contains no Cortex kernel, production memory, private implementation, evidence ledger, credentials, Docker configuration, or deployment controls. It sends only fixed, documented structured synthetic operations to the fixed HTTPS API. It does not offer free-text inputs, arbitrary URLs, commands, proxying, or LLM inference.

## What the demo shows

- temporal expiry
- supersession
- conflict/HOLD behavior
- provenance-required admission
- scope isolation
- session-scoped reset

The UI reports safe public fields only: decision, reason category, record ID, temporal status, provenance-presence, latency, and receipt ID. Visitor session credentials remain in server memory and never appear in UI output or application logging.

## Limitations

This is structured symbolic synthetic evaluation only—not production Cortex. The small owner-operated endpoint has finite capacity and no uptime guarantee. The Space does not create additional sessions to evade capacity or rate limits. A receipt records an API operation; it is not independent validation. No independent security audit is claimed.

Research context: [ADI paper DOI](https://doi.org/10.5281/zenodo.23265200). Public protocol, client, fixtures, and release: [GitHub challenge](https://github.com/brandenlaskowski7-bot/cortex-adi-research/tree/main/challenges/governed-memory) and [memory-challenge-v0.1](https://github.com/brandenlaskowski7-bot/cortex-adi-research/releases/tag/memory-challenge-v0.1).

## Create the Space (owner action)

The current Hugging Face connection is authenticated without repository-write permission, so this directory is upload-ready rather than published.

1. Sign in to Hugging Face as the intended owner and select **New Space**.
2. Name it `cortex-governed-memory-challenge`, choose **Gradio**, select **Public**, and create it.
3. In the new Space, choose **Files** → **Add file** → **Upload files**.
4. Upload the *contents* of this directory—`app.py`, `requirements.txt`, and this `README.md`—to the repository root. Do not upload the parent project or any private files.
5. Commit the upload. Wait for the Gradio build to finish.
6. Open the Space and run one ready-made scenario. Confirm only synthetic outcome fields appear and that a second browser session cannot see the first session's results.
7. Before announcing it publicly, obtain the owner’s explicit go-live confirmation and record the verified Space URL and commit SHA.

No Space is live merely because these files exist.

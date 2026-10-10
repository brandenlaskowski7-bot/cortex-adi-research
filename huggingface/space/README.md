---
title: Cortex Governed Memory Challenge
emoji: 🧭
colorFrom: teal
colorTo: blue
sdk: gradio
sdk_version: 6.30.0
python_version: '3.12'
app_file: app.py
pinned: false
license: cc-by-4.0
tags:
  - synthetic
  - governed-memory
  - developer-tools
  - symbolic-reasoning
short_description: Six synthetic memory experiments with decisions and receipts
---

# Cortex Governed Memory Challenge v0.1

**Upload-ready client requiring lifecycle API v0.2. Public ingress is stopped pending owner approval and external verification. No Hugging Face Space has been published or verified.**

Explore when a synthetic record should be returned, held, denied, expired, or superseded. This approachable Gradio interface is a **thin client** of the documented [public HTTPS API](https://challenge.aiadvantage.shop). It contains no private Cortex kernel or deployment code.

Choose one of six scenarios: **temporal expiry, supersession, conflict/HOLD, provenance, scope isolation, and reset**. Three synthetic subject/key sets are available. Inspect exact requests before running. The trace shows HTTP status, observed decision, reason category, temporal status, record ID, provenance presence, receipt ID, and whether the expected HTTP status/decision matched. Verify the latest receipt, reset the experiment, or end your session and erase its data. A countdown shows the remaining visit time.

## Scope and limitations

- Structured symbolic synthetic records only. No free text, LLM inference, prompts, generated answers, file uploads, arbitrary URLs, or commands.
- Not production Cortex. No proprietary source, private evidence ledger, internal policies, Docker internals, production memory, or credentials belong in this repo.
- Provenance presence indicates an artificial source reference; it does not verify a real assertion. An admission receipt records an operation, not current eligibility.
- First-party scenario matching is bounded, not independent replication or a security audit. Restart persistence is not tested by this Space.
- The owner-operated sandbox has **32 concurrent session slots, reclaimed after successful cleanup**, 256 records/session, 32 candidates/key, and documented rate limits. **Reset does not free a session slot.** Visits last at most 90 minutes and expire after 15 idle minutes. End releases a slot after cleanup; failures remain revoked and retry automatically. Persistent failures can require owner intervention. No uptime guarantee.
- This is suitable for a small, coordinated developer pilot. Broad, uncoordinated traffic may immediately exhaust the shared lab. There is no capacity-count route; successful health alone does not prove admission capacity.

## Privacy and client boundary

Tokens and upstream session IDs live only in server memory. They never enter Gradio components, logs, exported traces, URLs, or browser storage. A separate random, signed HttpOnly cookie binds each browser visitor to its server-side credentials. Hosted cookies are Secure/SameSite=None for the Space iframe. Gradio session hashes are ignored for authority. All operations use direct responses; alternate queue/call, file, proxy, and upload routes are blocked.

Cookies expire after 24 hours. Clearing cookies, restarting the Space, or changing browser/profile loses access. The client never shares or reuses credentials across visitors. End your session when finished. The server expires abandoned visits and cleans managed stores without a browser callback. The Space clears expired credentials and cached traces on a 15-second timer, including after browser closure. Open pages clear on their next timer update; disconnected pages or saved copies cannot be remotely erased. Reset does not extend the visit. Managed-store deletion is not forensic disk erasure or deletion of separate backups/exports. If iframe cookies are blocked, open the Space's app in its own tab. Ordinary hosting/network metadata may still be retained by providers.

Outbound requests use only `https://challenge.aiadvantage.shop`, certificate verification, exact documented routes, explicit `CortexGovernedMemoryChallenge/0.1`, no redirects or environment proxies, 4-second connect/write, 8-second read and 2-second pool timeouts, and bounded response sizes. Requests are spaced at least 0.5 seconds apart globally, creations are limited to four/minute, actions to one/visitor/eight seconds, with at most two concurrent actions and 24 visitors per process. Upstream 429/503 triggers a shared 60-second backoff. No automatic retries occur. Ambiguous session creation is never retried for that visitor. These client limits supplement the authoritative API limits; they are not DDoS protection.

Use one process and one replica. Multiple workers would create separate cookie-signing keys, session vaults, and rate budgets. Do not add a Hugging Face access token or production secret to Space settings: this client needs none.

## Run and verify locally

Python 3.12:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:7860`. The local bind is loopback-only; Hugging Face uses port 7860 on its hosted interface. No public Gradio share tunnel is created.

From this folder, install `pytest==9.1.1` and run `python -m pytest tests -q`. These are offline boundary/transport tests using synthetic mocks, not live-kernel evidence.

**Optional live check:** with the app running, `python tests/live_smoke.py`. This deliberately consumes **two new finite API session slots**, runs the six scenarios, checks two visitors with identical Gradio session hashes, verifies receipt and reset isolation, then ends both visits and confirms cleanup. Successful end releases their slots. Run once with owner awareness; never put it in recurring CI. Output contains sanitized outcomes only.

See [LAUNCH.md](LAUNCH.md) for the exact upload allowlist, owner creation/publication steps, and verification gate, and [VERIFICATION.md](VERIFICATION.md) for the actual preparation results.

## Research, contract, and reporting

- [ADI paper — DOI 10.5281/zenodo.23265200](https://doi.org/10.5281/zenodo.23265200)
- [Public GitHub challenge](https://github.com/brandenlaskowski7-bot/cortex-adi-research/tree/main/challenges/governed-memory)
- [API and limits](https://github.com/brandenlaskowski7-bot/cortex-adi-research/blob/main/challenges/governed-memory/API.md)
- [Live release memory-challenge-v0.1](https://github.com/brandenlaskowski7-bot/cortex-adi-research/releases/tag/memory-challenge-v0.1)
- [Report a synthetic failure](https://github.com/brandenlaskowski7-bot/cortex-adi-research/issues/new?template=challenge-failure.yml)

Attribute Branden Laskowski / Cortex Agentics Global and the public research repository. This client adapts the public v0.1 examples into guided scenarios under CC BY 4.0; it grants no rights to private implementation. Retain [LICENSE](LICENSE). The paper DOI identifies the paper, not a Space or dataset DOI.

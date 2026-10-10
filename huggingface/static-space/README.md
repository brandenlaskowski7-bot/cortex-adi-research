---
title: Cortex Governed Memory Challenge
emoji: 🧭
colorFrom: green
colorTo: blue
sdk: static
app_file: index.html
pinned: false
license: cc-by-4.0
short_description: Six synthetic memory experiments with decisions and receipts
---

# Cortex Governed Memory Challenge

This **free Static Space** introduces six governed-memory experiments and embeds or links to the interactive Gradio client at **https://challenge.aiadvantage.shop/demo/**. Hugging Face serves these static public-safe files; the existing owner-operated Mac hosts the resource-limited public client and the separate isolated synthetic challenge. No paid Hugging Face compute, GPU, API inference, or subscription is used.

The Space contains no kernel source, production memory, deployment internals, credentials, or evidence ledger. The interactive client uses only the documented fixed HTTPS synthetic API. Session credentials remain privately in the demo server's memory, separated per visitor; the static page never receives them.

## Sessions and limits

- Maximum visit: 90 minutes; idle cutoff: 15 minutes. Browser closure does not stop server expiry.
- Reset clears the experiment without extending the visit. End session revokes credentials, deletes managed synthetic session data, and releases the slot after cleanup succeeds.
- Cleanup failures remain revoked and consume capacity until automatic retry succeeds. Shared capacity is finite.
- Structured symbolic synthetic records only; no free text, LLM inference, or production Cortex. No independent security audit is claimed.
- Managed-store deletion does not promise forensic erasure or removal of separate backups, exported evidence, provider metadata, screenshots, or offline browser copies.
- The Mac, Docker, and internet connection must be running. If the lab is off or busy, the static documentation stays available. Use **Open in a new tab** if embedded cookies are blocked.

## Research and reporting

- [ADI paper — DOI 10.5281/zenodo.23265200](https://doi.org/10.5281/zenodo.23265200)
- [Public challenge and lifecycle contract](https://github.com/brandenlaskowski7-bot/cortex-adi-research/tree/feature/huggingface-memory-challenge-demo/challenges/governed-memory)
- [Original v0.1 release](https://github.com/brandenlaskowski7-bot/cortex-adi-research/releases/tag/memory-challenge-v0.1)
- [Public client source](https://github.com/brandenlaskowski7-bot/cortex-adi-research/tree/feature/huggingface-memory-challenge-demo/huggingface/space)
- [Report a synthetic counterexample](https://github.com/brandenlaskowski7-bot/cortex-adi-research/issues/new?template=challenge-failure.yml)

Report the scenario, expected and observed decision, reason category, receipt ID, and UTC time. Never send credentials or real data. Attribute Branden Laskowski / Cortex Agentics Global. This public client and guide grant no rights to private implementation.

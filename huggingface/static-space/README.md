---
title: ADI Governed Memory Lab
emoji: 🧠
colorFrom: green
colorTo: blue
sdk: static
app_file: index.html
pinned: false
license: cc-by-4.0
short_description: ADI-inspired synthetic memory decisions with receipts
---

# ADI Governed Memory Lab

ADI asks a practical question: **who or what has authority to decide?** This free, synthetic lab makes one side of that question visible in memory systems. Run six fixed experiments and observe deterministic decisions about eligibility, time, scope, conflict, provenance, replacement, and cleanup—each with an inspectable receipt.

The interactive lab is at **https://challenge.aiadvantage.shop/demo/**. Hugging Face serves these public-safe guide files; the existing owner-operated environment hosts the resource-limited synthetic client. No paid Hugging Face compute, GPU, API inference, or subscription is used.

This is not Cortex itself. The Space contains no kernel source, production memory, operational topology, credentials, or private evidence ledger. It demonstrates ADI-inspired governed-memory behavior using fixed symbolic data; it does not expose the private continuity substrate behind the work.

## What you can learn here

- A fact can be accepted but later become ineligible because time, scope, provenance, or replacement rules change.
- A correct result is sometimes **HOLD**, **DENY**, **HISTORICAL**, or **UNRESOLVED** rather than a retrieval.
- A receipt preserves what the service decided at the time of the operation; it is a trace record, not a later re-evaluation.
- The scenarios are bounded demonstrations, not claims of general-purpose memory, real-world truth verification, or an independent security audit.

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

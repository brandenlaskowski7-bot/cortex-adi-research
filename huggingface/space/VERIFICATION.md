# Preparation verification — 9 October 2026

**Status: upload-ready public client; Hugging Face Space not created or live.**

Source baseline: public `cortex-adi-research` main commit `371bb09aa923eb832d4cb877a888ad4bdc8e6a6b`. Protocol release: `memory-challenge-v0.1`; that immutable tag predates the current endpoint documentation and is unchanged.

## Current API check

A certificate-verified HTTPS request to `https://challenge.aiadvantage.shop/healthz` returned HTTP 200, `ok:true`, version `0.1`, and `inference_required:false`. A fresh synthetic session returned 201. Admission, pre-expiry recall, exact-expiry recall, and pre-effective-time recall matched RETURN/RETURN/HISTORICAL/UNRESOLVED. The session was reset afterward. No production service was inspected or modified.

## Local end-to-end result

At **2026-10-09 21:44:21–21:45:37 UTC (5:44:21–5:45:37 p.m. EDT)**, the running local Gradio app forwarded fixed synthetic operations to the public HTTPS API:

| Guided scenario | Matched HTTP/decision steps |
| --- | ---: |
| Temporal expiry | 5/5 |
| Supersession | 6/6 |
| Conflict / HOLD | 4/4 |
| Provenance | 3/3 |
| Scope isolation | 4/4 |
| Reset | 5/5 |
| **Total** | **27/27** |

Two independent HTTP cookie jars deliberately supplied the same Gradio session hash. They received distinct receipts. Same-session receipt retrieval matched the original safe response; resetting visitor A left visitor B's receipt unchanged. Alternate queued/call paths were refused. Local UI responses contained no bearer headers, token field, or upstream session ID. Both visitors were reset at completion.

A separate browser interaction rendered Temporal expiry and its five matched live decisions. Visual inspection covered the scenario controls, synthetic request preview, result table, receipt/reset controls, limitations, and links. The result table scrolls horizontally to its receipt/expectation columns. This is a local browser check, not a hosted Hugging Face check.

The later capacity-retry and crafted-input hardening was verified by offline tests without repeating live sessions.

These checks used **four new finite upstream sessions total**: one initial API check, two end-to-end visitors, and one browser visitor. Resets clear their synthetic data but **do not reclaim those session slots**. Do not repeat tests casually.

## Offline checks

**23 tests passed** using Python 3.12, Gradio 6.30.0, and pinned top-level dependencies. Coverage includes cookie/visitor separation with identical Gradio hashes, cookie forgery and missing-cookie rejection, hosted Secure/HttpOnly cookies, cross-origin refusal, actual body-size limits, blocked file/proxy/upload/queue routes, fixed HTTPS origin and User-Agent, strict timeouts, no redirects/environment proxies, response projection, invalid/oversized upstream responses, synthetic input bounds and crafted-input non-reflection in responses/logs, visitor cap, 429/503 backoff, safe manual retry after a definite capacity refusal, and no retry after ambiguous creation timeout. Mocks in these tests are explicitly client tests, not evidence of kernel behavior.

The offline CI workflow never creates public API sessions. Hosted CI status is reported separately with the final branch commit/run link.

## Limits of this evidence

No independent audit, penetration-test guarantee, production Cortex evaluation, natural-language inference, operator restart, or hosted Hugging Face functionality is claimed. Expected scenario matching checks HTTP status and decision, not every field of the full protocol contract. Capacity count is not exposed by the API. A successful health check is not a promise of capacity or uptime.

Tokens, cookie values, private source, raw deployment evidence, and internal topology are excluded from this report. No production containers or private research repositories were modified.

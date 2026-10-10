# Lifecycle preparation verification — 10 October 2026

**Current status: lifecycle v0.2 installed and verified locally; public ingress OFF; Hugging Face Space not created or live.** The October 9 public HTTPS evidence below is historical and does not establish current uptime.

The current connected Hugging Face account is `BrandenLaskowski7`, with profile/read/jobs permissions and no repository create/write permission. No write privilege was expanded. Upload remains an owner step after the API launch gate.

## Current checks

- **29/29 offline client tests passed**, including visitor/cookie isolation, bounded HTTPS transport, synthetic input and route restrictions, expiry-driven credential/trace erasure, confirmed End cleanup, reset deadline preservation, and cache reclamation after browser closure.
- **27/27 guided scenario steps passed** between 16:31:02 and 16:32:17 UTC on 10 October 2026. The local Gradio callbacks used a private test-only adapter to forward their fixed HTTPS-shaped requests through the actual local gateway and hardened Docker runtime. The published client contains no configurable URL or loopback override. This was a local end-to-end test, **not an external HTTPS test**.
- **7/7 associated checks passed:** separate cookie visitors despite an identical Gradio session hash; reset isolation; authenticated lifecycle status through the gateway; End revocation/cleared UI/other-visitor preservation; both sessions ended with confirmed cleanup; blocked alternate queue and credential-shaped output; zero occupied slots and zero cleanup backlog afterward.
- Owner-side verification recorded **16/16 lifecycle unit tests, 24/24 disposable Docker contract checks, 5/5 shortened-duration Docker timing checks, and 16/16 installed-container boundary checks**. Copied kernel source hashes remained unchanged. Implementation, images, topology, raw evidence, and private credentials are excluded from this public repository.

Timing tests used the same runtime code with owner-only limits shortened to 20 seconds absolute and 5 seconds idle. Unit tests cover the full 90-minute/15-minute boundaries. The regular installed policy was separately verified as 90 minutes absolute, 15 minutes idle, with a 10-second cleanup sweep. This is not a 90-minute wall-clock endurance result or an independent security audit.

An initial hosted timing unit test assumed creation occurred exactly at the fake clock's starting value. It was corrected to test the actual persisted deadline; the corrected private hosted checks passed. No production service was modified by the lifecycle work. Public ingress is intentionally stopped; its last pre-hardening health request returned an unavailable Cloudflare response. Reopening requires owner approval followed by fresh external health, session, isolation, and cleanup checks.

## Remaining launch gate

Approve reopening only the dedicated challenge HTTPS entrance, verify the lifecycle externally with two bounded synthetic visitors, create/upload the private Space through the owner account, inspect it, then obtain explicit owner confirmation for public visibility. A proposed Space URL is not evidence that it exists. Do not announce a live demo until public hosted interaction is verified. See [LAUNCH.md](LAUNCH.md).

---

# Historical v0.1 preparation verification — 9 October 2026

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

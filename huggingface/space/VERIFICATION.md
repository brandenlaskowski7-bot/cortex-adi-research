# Free launch preparation verification — 10 October 2026

**Status: the free Static Space is created and populated, remains PRIVATE, and public ingress is OFF. The demo client is stopped. New visits are paused; no active sessions or cleanup backlog remain. Public launch is pending explicit owner activation.**

Space: https://huggingface.co/spaces/BrandenLaskowski7/cortex-governed-memory-challenge

Private Space revision observed in the authenticated browser: `aa221d6ba217781f524b5d16bc661594b856a4ac`. Only the static page, guide, and attribution license were added; the default non-sensitive template files remain. No kernel, credentials, deployment files, or private evidence were uploaded. The browser authenticated as the owner; connector repository scopes remain read-only. No subscription or paid compute was purchased.

## Current evidence

- **30/30 offline client tests passed**, including fixed HTTPS transport, User-Agent/timeouts, bounded inputs, per-visitor credentials and cookie isolation, forged-cookie/cross-origin rejection, blocked uploads/files/proxy/queues, finite capacity/backoff, expiry-driven erasure, and the self-hosted HTTPS prefix/cookie policy. These use mocks and do not prove kernel behavior.
- **22/22 local demo proxy checks passed**: HTML/assets and callback delivery, HTTPS root, Secure/HttpOnly scoped cookies, restricted embedding, unchanged API origin denial, prohibited paths, body-size limits, and host/HTTPS enforcement. This is owner-side infrastructure evidence, not an independent audit.
- At **16:45:51–16:46:14 UTC**, certificate-verified external API lifecycle checks passed **17/17**, with two isolated synthetic visitors and confirmed cleanup. The same fixed HTTPS client also matched all **27/27** guided scenario steps.
- At **17:09:26–17:11:01 UTC**, the installed Gradio client was exercised through the actual public HTTPS `/demo/` entrance. **27/27 guided steps matched** across temporal expiry, supersession, conflict/HOLD, provenance, scope isolation, and reset. Two independent cookie jars deliberately used the same Gradio session hash. Distinct receipts, exact receipt retrieval, reset isolation, blocked alternate call path, and absence of credential-shaped UI output passed. Both visitors ended with confirmed cleanup (**7 associated checks including those two cleanups**).
- The authenticated Hugging Face **private Static Space** rendered the embedded Gradio app. A separate browser visitor completed Temporal expiry (**5/5** matched steps), verified its receipt, then ended the session; the trace and local result display cleared. This is private-preview browser evidence. Signed-out public Space access is intentionally not tested until publication is approved.
- The temporary test controller closed the public entrance at **17:14:12 UTC**, confirmed paused admission, zero active sessions, zero cleanup backlog, and stopped the separate client. The private Space still displays Running for its static page; this does not establish a public challenge launch.
- Prior lifecycle verification remains **16/16 unit tests, 24/24 disposable Docker contract checks, 5/5 shortened-duration timing checks, and 16/16 installed kernel/relay boundary checks**. Copied kernel hashes remained unchanged. Private implementation, images, topology, and raw evidence are excluded from this public repository.

An initial free-demo test matched all scenarios but encountered browser asset concurrency limits and one unconfirmed client End result from overly tight test pacing. The automatic owner shutdown confirmed final cleanup. The demo proxy concurrency ceiling was adjusted for normal browser asset loading, and the test now waits after each response before the next action. The complete corrected test and browser preview then passed. No failed attempt is reported as a successful end-to-end result.

The timing tests use the same lifecycle code with owner-only limits shortened to 20 seconds absolute and 5 seconds idle. Unit tests cover the 90-minute/15-minute boundaries; installed defaults were separately checked. This is not a 90-minute wall-clock endurance test, an independent security audit, or a production Cortex evaluation.

## Activation still pending

The free architecture uses Hugging Face Static plus the owner's existing Mac, Docker, and internet connection. Those existing resources must remain available. Availability and shared capacity are finite; no uptime guarantee or independent audit is claimed. No public launch announcement or outreach has been sent. See [LAUNCH.md](LAUNCH.md) for the one owner activation decision and exact manual steps.

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

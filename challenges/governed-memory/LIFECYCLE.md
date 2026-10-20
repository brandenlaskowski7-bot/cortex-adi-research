# Synthetic challenge lifecycle v0.2

**Prepared and installed locally; public ingress remains off pending owner approval and external verification.** The v0.1 release remains an unchanged historical release.

| Control | Visitor behavior |
| --- | --- |
| Separation | Each visitor has independent credentials, declared scopes, synthetic records, and receipts. |
| Time limit | Access ends at 90 minutes from creation, or after 15 minutes without valid record/query activity, whichever comes first. |
| Reset | Clears the experiment and prior receipts. Keeps the original deadlines, credentials, rate limits, and lifetime operation budget. |
| End | Revokes credentials immediately, erases managed session data, and frees the slot only after successful cleanup. |
| Automatic cleanup | Runs without a browser, every 10 seconds and at startup. Expired/revoked sessions stay denied while failed cleanup retries. |
| Restart | Retains existing deadlines; it never grants a fresh visit. Old sessions without trusted deadlines are retired on upgrade. |
| Capacity | 32 concurrent slots including pending cleanup; bounded requests, operations, records, CPU, RAM, processes, and storage admission. |
| Owner control | Private controls show counts, time remaining, storage, and cleanup backlog; the owner can pause new admissions or end visits. These controls are not public API routes. |

Expiry is enforced when a request runs, including after queueing and before acknowledging a completed record/query operation. The sweeper handles deletion separately; 10 seconds is the normal sweep interval, not a cleanup guarantee during failures. Neither synthetic record timestamps nor the visitor's browser clock can extend access. Significant backward clock movement across restart fails closed.

Cleanup covers this sandbox's managed synthetic stores, record indexes, replay keys, and receipts. Credentials and cached results in the demo are discarded after end/expiry; browser closure alone does not stop the backend deadline. New application logs omit credentials, record bodies, receipt IDs, and session identifiers. Fixed aggregate operational counters may remain. Previously exported private evidence, host snapshots/backups, provider metadata, offline browser pages, and saved screenshots are outside automatic session erasure. No forensic media-erasure claim is made.

Storage admission uses 32 MiB/session and 512 MiB/lab watermarks with headroom. These are application-level bounds rather than a hard Docker-volume quota. Shared capacity can still be exhausted; clients must stop on busy/full responses. No independent security audit, production Cortex access, free text, or LLM inference is included.

The public repository contains the contract, fixtures, and thin client only. Private implementation and deployment configuration must never be uploaded to Hugging Face or this public repository.

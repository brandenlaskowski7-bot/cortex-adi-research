# Challenge security and isolation

Use only synthetic fixtures and an explicitly authorized endpoint. No private or production system is a target. The public API cannot expose storage, SQL, shell, filesystem browsing, arbitrary tools, policy source, internal errors, or private evidence. Session tokens must not appear in reports.

The local implementation uses dedicated synthetic state, authenticated session/scope boundaries, rate and size limits, safe response projection, and receipts. The exact v0.1 API and limits are in [API.md](API.md). Session lifetime is owner-controlled, bounded by total capacity; explicit reset clears only the caller's data. Automatic time-based expiration is not implemented in v0.1.

Local bounded verification is not authorization to expose an arbitrary deployment. Internet exposure requires a reviewed secure transport/access boundary and an announced challenge endpoint. No internet endpoint is currently announced. Vulnerability reports should contain only safe synthetic reproduction material; use the failure template and omit credentials.

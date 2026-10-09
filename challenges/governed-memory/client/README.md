# Public challenge client

Use `python3 run_fixture.py ../fixtures --base https://challenge.aiadvantage.shop`.
The earlier `challenge_client.py --base-url URL --fixture FILE` interface is retained as a compatibility wrapper around the same tested API client. Both create authenticated synthetic sessions, execute fixtures, omit tokens from reports, and report restart continuity as NOT_TESTED unless an operator performs the restart through the primary client.

The designated public endpoint is `https://challenge.aiadvantage.shop`. The client sends `User-Agent: CortexGovernedMemoryChallenge/0.1`; Cloudflare may refuse Python's generic user-agent. Use the current client rather than the older immutable tag snapshot. The client has no kernel, Docker control, arbitrary shell execution, or private credentials. Keep generated session credentials private and respect the published budgets. This is a synthetic structured-symbolic challenge, not production Cortex or a general security guarantee.

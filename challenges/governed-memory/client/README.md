# Public challenge client

Use `python3 run_fixture.py ../fixtures --base http://127.0.0.1:8808`.
The earlier `challenge_client.py --base-url URL --fixture FILE` interface is retained as a compatibility wrapper around the same tested API client. Both create authenticated synthetic sessions, execute fixtures, omit tokens from reports, and report restart continuity as NOT_TESTED unless an operator performs the restart through the primary client.

No internet endpoint has been announced. Use only an authorized sandbox. The client has no kernel, Docker control, arbitrary shell execution, or private credentials.

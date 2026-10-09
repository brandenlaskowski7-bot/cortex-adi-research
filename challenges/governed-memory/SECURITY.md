# Challenge Security and Isolation Requirements

The public challenge runtime must be deployed in a dedicated challenge container/image and must use synthetic-only stores.

Required controls:
- no production credentials;
- no mounts to production memory or research evidence databases;
- fresh per-session namespace;
- localhost/admin control plane separated from public challenge plane;
- rate limiting and request-size limits;
- explicit session expiration/reset;
- audit receipts for challenge operations;
- fail-closed adapter behavior;
- no shell, filesystem, SQL, or arbitrary tool surface exposed to challengers;
- no raw internal error traces returned publicly.

A challenge deployment is not authorized until isolation tests demonstrate that production/research memory cannot be addressed from the challenge namespace.

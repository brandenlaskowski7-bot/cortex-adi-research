#!/usr/bin/env python3
"""Protocol plumbing example ONLY: always abstains, not a V4 adapter or a model."""
import json, sys
request=json.load(sys.stdin)
assert isinstance(request['prompt'],str)
# Replace this section with your EXISTING unchanged V4 invocation.
# Feed request['prompt'] as the user input. Preserve V4's system prompt and settings.
# Print only the exact model output to stdout; diagnostics belong on stderr.
# Do not put fixture labels or expected outcomes into model context.
print(json.dumps({'decision':'abstain','reason':'plumbing example; no model invoked','proposal':None}))

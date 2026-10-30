#!/usr/bin/env python3
"""Run ADI Authorization Boundary Challenge v0.2 synthetic fixtures.

The only sink is a local list. This program never sends, stores, or executes an
operation outside its process.
"""
import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone


def decision(fixture):
    authorization = fixture["authorization"]
    if authorization != "allow":
        return authorization, "not_evaluated", "not_executed"
    states = [parameter.get("status") for parameter in fixture["parameters"]]
    sources = [parameter.get("source") for parameter in fixture["parameters"]]
    if any(state == "unavailable" for state in states):
        return "allow", "unavailable", "not_executed"
    if any(not source for source in sources) or any(state != "current" for state in states):
        return "allow", "deny", "not_executed"
    return "allow", "allow", "executed"


def digest(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Run synthetic ADI v0.2 fixtures")
    parser.add_argument("fixtures", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    document = json.loads(args.fixtures.read_text())
    simulated_sink, rows = [], []
    for fixture in document["fixtures"]:
        observed = dict(zip(("authorization", "execution_state", "sink"), decision(fixture)))
        expected = fixture["expected"]
        passed = observed == expected
        if observed["sink"] == "executed":
            simulated_sink.append(fixture["id"])
        rows.append({"fixture_id": fixture["id"], "expected": expected, "observed": observed, "passed": passed})
    result = {
        "status": "passed" if all(row["passed"] for row in rows) else "failed",
        "scope": document["scope"],
        "fixture_version": document["version"],
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "fixture_digest": digest(args.fixtures),
        "runner_digest": digest(Path(__file__)),
        "simulated_sink": simulated_sink,
        "results": rows,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "passed" else 1)


if __name__ == "__main__":
    main()

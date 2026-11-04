#!/usr/bin/env python3
"""Run synthetic record-based fixtures and emit hash-chained local receipts."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha256(value):
    return "sha256:" + hashlib.sha256(value.encode()).hexdigest()


def decide(fixture, records):
    record = records.get(fixture.get("record_id"))
    request = fixture.get("request")
    if not record or record["status"] != "current" or not request:
        return "deny"
    return "allow" if all(record[key] == request[key] for key in ("principal", "operation", "target")) else "deny"


def execution_state(fixture, authorization):
    if authorization != "allow":
        return "not_evaluated"
    parameters = fixture.get("parameters", [])
    if any(not item.get("source") or item.get("status") != "current" for item in parameters):
        return "deny"
    return "allow"


def main():
    parser = argparse.ArgumentParser(description="Run receipted synthetic ADI v0.2.2 fixtures")
    parser.add_argument("fixtures", type=Path)
    parser.add_argument("records", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipts", type=Path, required=True)
    args = parser.parse_args()
    fixture_doc = json.loads(args.fixtures.read_text())
    records = {record["id"]: record for record in json.loads(args.records.read_text())["records"]}
    previous, rows, receipts = "sha256:genesis", [], []
    for fixture in fixture_doc["fixtures"]:
        authorization = decide(fixture, records)
        state = execution_state(fixture, authorization)
        observed = {"authorization": authorization, "execution_state": state,
                    "sink": "executed" if authorization == state == "allow" else "not_executed"}
        expected = fixture["expected"]
        passed = observed == expected if isinstance(expected, dict) else (
            observed["authorization"] == expected if expected == "deny" else observed["sink"] == "executed")
        receipt = {"fixture_id": fixture["id"], **observed,
                   "previous_receipt": previous}
        receipt["receipt_id"] = sha256(json.dumps(receipt, sort_keys=True))
        previous = receipt["receipt_id"]
        receipts.append(receipt)
        rows.append({"fixture_id": fixture["id"], "expected": expected,
                     "observed": observed, "passed": passed,
                     "receipt_id": receipt["receipt_id"]})
    args.receipts.write_text("\n".join(json.dumps(row, sort_keys=True) for row in receipts) + "\n")
    result = {"status": "passed" if all(row["passed"] for row in rows) else "failed",
              "scope": fixture_doc["scope"], "fixture_version": fixture_doc["version"],
              "recorded_at": datetime.now(timezone.utc).isoformat(), "results": rows}
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "passed" else 1)


if __name__ == "__main__":
    main()

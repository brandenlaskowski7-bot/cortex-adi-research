#!/usr/bin/env python3
"""Verify tests, disclosure markers, content scan, and release hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {".deps", "__pycache__", ".git", ".pytest_cache"}
TEXT_SUFFIXES = {"", ".cff", ".css", ".html", ".js", ".json", ".md", ".py", ".txt", ".yaml", ".yml"}
FORBIDDEN = {
    "real-retailer-name": re.compile(r"\b(?:Walmart|Kroger|Target|Costco)\b", re.IGNORECASE),
    "private-repository-url": re.compile(r"github\.com/[^\s)]+/cortex-spatial-intelligence(?:\.git)?", re.IGNORECASE),
    "local-user-path": re.compile(r"(?:/Users/[^/\s]+|/home/[^/\s]+|[A-Za-z]:\\\\Users\\\\[^\\\s]+)"),
    "github-token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "hugging-face-token": re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    "aws-access-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def scan() -> list[str]:
    findings: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        # The verifier necessarily contains the detection expressions themselves.
        if relative == Path("scripts/verify_release.py"):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in FORBIDDEN.items():
            if pattern.search(text):
                findings.append(f"{relative.as_posix()}: {label}")
    return findings


def verify_hashes() -> list[str]:
    failures: list[str] = []
    sums = ROOT / "evidence" / "SHA256SUMS"
    if not sums.exists():
        return ["evidence/SHA256SUMS is missing"]
    for line in sums.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        target = ROOT / relative
        if not target.is_file():
            failures.append(f"missing hashed file: {relative}")
        elif sha256(target) != expected:
            failures.append(f"hash mismatch: {relative}")
    return failures


def main() -> int:
    failures: list[str] = []
    tests = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=ROOT / "space",
        capture_output=True,
        text=True,
        check=False,
    )
    print(tests.stdout + tests.stderr, end="")
    if tests.returncode:
        failures.append("public reference tests failed")

    fixture = json.loads((ROOT / "space" / "fixtures" / "synthetic_store.json").read_text(encoding="utf-8"))
    if fixture.get("data_classification") != "wholly-synthetic":
        failures.append("fixture is missing the wholly-synthetic classification")
    engine = (ROOT / "space" / "reference_engine.py").read_text(encoding="utf-8")
    if "independent-public-reference" not in engine:
        failures.append("reference implementation marker is missing")

    failures.extend(scan())
    failures.extend(verify_hashes())
    if failures:
        print("\nRELEASE VERIFICATION FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("\nRELEASE VERIFICATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


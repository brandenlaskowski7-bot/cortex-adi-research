#!/usr/bin/env python3
"""Build deterministic release evidence for the sanitized public package."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
EXCLUDED_PARTS = {".deps", "__pycache__", ".git", ".pytest_cache"}
EXCLUDED_FILES = {
    Path("evidence/RELEASE_MANIFEST.json"),
    Path("evidence/SHA256SUMS"),
    Path("evidence/public_test_results.json"),
}


def release_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        if relative in EXCLUDED_FILES:
            continue
        files.append(relative)
    return sorted(files, key=lambda path: path.as_posix())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    EVIDENCE.mkdir(exist_ok=True)
    started = datetime.now(timezone.utc)
    completed = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=ROOT / "space",
        capture_output=True,
        text=True,
        check=False,
    )
    combined = completed.stdout + completed.stderr
    test_count = 0
    for line in combined.splitlines():
        match = re.match(r"Ran (\d+) tests?\b", line)
        if match:
            test_count = int(match.group(1))

    test_record = {
        "schema_version": "1.0",
        "scope": "independent-public-reference",
        "fixture_class": "wholly-synthetic",
        "command": "python -m unittest discover -s tests -v",
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "started_at_utc": started.isoformat().replace("+00:00", "Z"),
        "exit_code": completed.returncode,
        "tests_run": test_count,
        "result": "PASS" if completed.returncode == 0 else "FAIL",
        "output": combined.strip().splitlines(),
    }
    (EVIDENCE / "public_test_results.json").write_text(
        json.dumps(test_record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    files = release_files()
    manifest = {
        "schema_version": "1.0",
        "release": "cortex-spatial-intelligence-public-review-v0.1.0-rc1",
        "implementation": "independent-public-reference",
        "fixture_class": "wholly-synthetic",
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "file_count_excluding_generated_evidence": len(files),
        "files": [path.as_posix() for path in files],
        "generated_evidence": [
            "evidence/public_test_results.json",
            "evidence/RELEASE_MANIFEST.json",
            "evidence/SHA256SUMS",
        ],
    }
    (EVIDENCE / "RELEASE_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    hashed = files + [Path("evidence/public_test_results.json")]
    lines = [f"{sha256(ROOT / path)}  {path.as_posix()}" for path in hashed]
    (EVIDENCE / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"tests={test_count} result={test_record['result']} files={len(hashed)}")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())


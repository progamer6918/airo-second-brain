#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    ".venv",
    "venv",
}

EXCLUDED_FILES = {
    ".env",
}

EXCLUDED_NAMES = {
    Path(__file__).name,
}

SECRET_PATTERNS = [
    re.compile(r"(?i)\b(api[_-]?key|secret|private[_-]?key|access[_-]?token|refresh[_-]?token)\b\s*=\s*['\"][^'\"]{8,}['\"]"),
    re.compile(r"(?i)\b(api[_-]?key|secret|private[_-]?key|access[_-]?token|refresh[_-]?token)\b\s*:\s*['\"][^'\"]{8,}['\"]"),
    re.compile(r"(?i)\bNOTION_TOKEN\s*=\s*['\"]?secret_[A-Za-z0-9_\-]{10,}"),
    re.compile(r"(?i)\bTELEGRAM_BOT_TOKEN\s*=\s*['\"]?\d{6,}:[A-Za-z0-9_\-]{20,}"),
    re.compile(r"-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
]

SAFE_PLACEHOLDERS = [
    "your_",
    "example",
    "placeholder",
    "changeme",
    "<",
    ">",
    "xxx",
    "dummy",
    "dry_run",
]


def is_excluded(path: Path) -> bool:
    rel = path.relative_to(ROOT)

    if any(part in EXCLUDED_DIRS for part in rel.parts):
        return True

    if path.name in EXCLUDED_FILES:
        return True

    if path.name in EXCLUDED_NAMES:
        return True

    if ".bak." in path.name:
        return True

    if path.suffix.lower() in {".pyc", ".png", ".jpg", ".jpeg", ".gif", ".sqlite", ".db"}:
        return True

    return False


def is_safe_placeholder(line: str) -> bool:
    lower = line.lower()
    return any(marker in lower for marker in SAFE_PLACEHOLDERS)


def scan_file(path: Path) -> list[str]:
    findings: list[str] = []

    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        return [f"READ_ERROR {path.relative_to(ROOT)}: {exc}"]

    for line_no, line in enumerate(text.splitlines(), start=1):
        if is_safe_placeholder(line):
            continue

        for pattern in SECRET_PATTERNS:
            if pattern.search(line):
                findings.append(f"{path.relative_to(ROOT)}:{line_no}")
                break

    return findings


def main() -> int:
    findings: list[str] = []

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue

        if is_excluded(path):
            continue

        findings.extend(scan_file(path))

    if findings:
        print("SECURITY_SCAN FAIL possible real secret markers:")
        for item in findings:
            print(f"- {item}")
        return 1

    print("SECURITY_SCAN PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

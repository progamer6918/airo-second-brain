#!/usr/bin/env python3
"""Static validation for the AIRO WorkDesk candidate.

This validates the portable candidate itself. It does NOT prove semantic completeness,
live runtime state, canonical git parity, or fresh-AI comprehension.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except Exception:
    yaml = None

ROOT = Path(__file__).resolve().parents[2]
errors: list[str] = []
warnings: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def rows(rel: str) -> list[dict[str, str]]:
    p = ROOT / rel
    if not p.exists():
        fail(f"MISSING_FILE={rel}")
        return []
    with p.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


required = [
    "projects/airo-workdesk.md",
    "docs/prd/AIRO_WORKDESK_PRD_v0.2.0.md",
    "docs/roadmap/AIRO_WORKDESK_ROADMAP.md",
    "wiki/workdesk/HOME.md",
    "wiki/workdesk/BOOT.md",
    "wiki/workdesk/CURRENT.md",
    "wiki/workdesk/SOURCE_AUTHORITY.md",
    "wiki/workdesk/KNOWLEDGE_MAP.md",
    "wiki/workdesk/TASK_ROUTER.md",
    "wiki/workdesk/role/AREA_SALES_SUPERVISOR.md",
    "wiki/workdesk/glossary/WORK_TERMINOLOGY.md",
    "wiki/workdesk/boot/WORKDESK_BOOT_BUNDLE.md",
    "wiki/workdesk/boot/WORKDESK_BOOT_MANIFEST.tsv",
    "evidence/workdesk/SOURCE_MANIFEST.tsv",
    "evidence/workdesk/COVERAGE_MATRIX.tsv",
    "evidence/workdesk/CLAIM_LEDGER.tsv",
    "evidence/workdesk/CONFLICT_REGISTER.tsv",
    "tests/workdesk/COMPREHENSION_TEST.md",
    "tests/workdesk/HUMAN_NAVIGATION_TEST.md",
    "tests/workdesk/SOURCE_PRIORITY_TEST.md",
]
for rel in required:
    if not (ROOT / rel).exists():
        fail(f"REQUIRED_FILE_MISSING={rel}")

source = rows("evidence/workdesk/SOURCE_MANIFEST.tsv")
coverage = rows("evidence/workdesk/COVERAGE_MATRIX.tsv")
claims = rows("evidence/workdesk/CLAIM_LEDGER.tsv")
conflicts = rows("evidence/workdesk/CONFLICT_REGISTER.tsv")
boot_manifest = rows("wiki/workdesk/boot/WORKDESK_BOOT_MANIFEST.tsv")

source_ids = [r.get("source_id", "") for r in source]
coverage_ids = [r.get("source_id", "") for r in coverage]
claim_ids = [r.get("claim_id", "") for r in claims]

def duplicate_values(vals: list[str]) -> list[str]:
    seen, dup = set(), set()
    for v in vals:
        if not v:
            continue
        if v in seen:
            dup.add(v)
        seen.add(v)
    return sorted(dup)

for label, vals in [("SOURCE_ID", source_ids), ("COVERAGE_SOURCE_ID", coverage_ids), ("CLAIM_ID", claim_ids)]:
    dup = duplicate_values(vals)
    if dup:
        fail(f"DUPLICATE_{label}=" + ",".join(dup))

sset, cset = set(source_ids), set(coverage_ids)
if sset != cset:
    fail("SOURCE_COVERAGE_ID_SET_MISMATCH")
    if sset - cset:
        fail("COVERAGE_MISSING_IDS=" + ",".join(sorted(sset - cset)))
    if cset - sset:
        fail("COVERAGE_UNKNOWN_IDS=" + ",".join(sorted(cset - sset)))

for r in claims:
    sid = r.get("source_id", "")
    authority = r.get("authority", "")
    if sid and sid not in sset:
        if not (sid == "OWNER_CONFIRMATION" and authority == "OWNER_CONFIRMED"):
            fail(f"CLAIM_UNKNOWN_SOURCE={r.get('claim_id')}:{sid}")
    if sid == "OWNER_CONFIRMATION" and "decisions/approved/" not in r.get("source_location", ""):
        fail(f"OWNER_CLAIM_MISSING_DECISION_POINTER={r.get('claim_id')}")
    if not r.get("source_location", "").strip():
        fail(f"CLAIM_MISSING_LOCATION={r.get('claim_id')}")
    if not r.get("confidence", "").strip():
        fail(f"CLAIM_MISSING_CONFIDENCE={r.get('claim_id')}")

# Secret-excluded rows must not expose real path/hash.
for r in source:
    if r.get("source_class") == "SECRET_EXCLUDED":
        if r.get("display_path") != "[REDACTED_SECRET_NOTE]":
            fail(f"SECRET_ROW_PATH_NOT_REDACTED={r.get('source_id')}")
        if r.get("sha256") != "[REDACTED]":
            fail(f"SECRET_ROW_HASH_NOT_REDACTED={r.get('source_id')}")
        if r.get("raw_publication") != "NEVER_PUBLISH_RAW":
            fail(f"SECRET_ROW_PUBLICATION_POLICY_INVALID={r.get('source_id')}")

# Boot manifest is deterministic and hash-checked.
for r in boot_manifest:
    rel = r.get("path", "")
    p = ROOT / rel
    if not p.exists():
        fail(f"BOOT_MANIFEST_FILE_MISSING={rel}")
        continue
    actual_hash = sha256(p)
    if actual_hash != r.get("sha256"):
        fail(f"BOOT_MANIFEST_HASH_MISMATCH={rel}")
    try:
        expected_bytes = int(r.get("bytes", "0"))
    except ValueError:
        expected_bytes = -1
    if p.stat().st_size != expected_bytes:
        fail(f"BOOT_MANIFEST_SIZE_MISMATCH={rel}")

# Validate Obsidian wikilinks against candidate files.
workdesk_prefixes = ("wiki/workdesk", "evidence/workdesk", "tests/workdesk", "projects/airo-workdesk.md", "docs/prd/AIRO_WORKDESK", "docs/roadmap/AIRO_WORKDESK", "decisions/approved/airo-workdesk")
files = {p.relative_to(ROOT).as_posix(): p for p in ROOT.rglob("*") if p.is_file() and p.relative_to(ROOT).as_posix().startswith(workdesk_prefixes)}
md_by_stem: dict[str, list[str]] = {}
for rel in files:
    if rel.endswith(".md"):
        stem = Path(rel).stem
        md_by_stem.setdefault(stem, []).append(rel)

link_re = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
for rel, p in files.items():
    if not rel.endswith(".md"):
        continue
    text = p.read_text(encoding="utf-8", errors="replace")
    for target in link_re.findall(text):
        target = target.strip()
        if not target or target.startswith(("http://", "https://")):
            continue
        current_dir = Path(rel).parent
        candidates = []
        if "/" in target:
            t = Path(target)
            candidates.extend([
                (current_dir / (target + ".md")).as_posix(),
                (current_dir / target).as_posix(),
                (Path("wiki/workdesk") / (target + ".md")).as_posix(),
                (Path("wiki/workdesk") / target).as_posix(),
                (Path(target + ".md")).as_posix(),
                Path(target).as_posix(),
            ])
            if not any(c in files for c in candidates):
                fail(f"BROKEN_WIKILINK={rel}=>{target}")
        else:
            local = (current_dir / f"{target}.md").as_posix()
            wd = (Path("wiki/workdesk") / f"{target}.md").as_posix()
            if local not in files and wd not in files and target not in md_by_stem:
                fail(f"BROKEN_WIKILINK={rel}=>{target}")

# Canvas JSON must parse.
for p in ROOT.rglob("*.canvas"):
    try:
        json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"CANVAS_JSON_INVALID={p.relative_to(ROOT)}:{e}")

# Base files should be valid YAML when PyYAML is available.
if yaml is not None:
    for p in ROOT.rglob("*.base"):
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or "views" not in data:
                fail(f"OBSIDIAN_BASE_SCHEMA_INVALID={p.relative_to(ROOT)}")
        except Exception as e:
            fail(f"OBSIDIAN_BASE_YAML_INVALID={p.relative_to(ROOT)}:{e}")
else:
    warn("PY_YAML_UNAVAILABLE_BASE_PARSE_SKIPPED=YES")

# Detect likely real secrets. Policy prose mentioning the words is allowed.
secret_patterns = {
    "OPENAI_STYLE_KEY": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "GITHUB_TOKEN": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "GOOGLE_API_KEY": re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b"),
    "BEARER_TOKEN": re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{24,}\b", re.I),
    "PASSWORD_ASSIGNMENT": re.compile(r"\b(?:password|passwd|pwd)\s*[:=]\s*[^\s`]{6,}", re.I),
    "SECRET_ASSIGNMENT": re.compile(r"\b(?:api[_ -]?key|access[_ -]?token|refresh[_ -]?token|client[_ -]?secret)\s*[:=]\s*[^\s`]{8,}", re.I),
}
for rel, p in files.items():
    if p.suffix.lower() not in {".md", ".tsv", ".txt", ".py", ".base"}:
        continue
    text = p.read_text(encoding="utf-8", errors="replace")
    for name, pattern in secret_patterns.items():
        if pattern.search(text):
            fail(f"POSSIBLE_SECRET={name}:{rel}")

# Candidate must not claim final digestion prematurely.
health = (ROOT / "wiki/workdesk/KNOWLEDGE_HEALTH.md").read_text(encoding="utf-8")
if "FULLY_DIGESTED_AND_TRANSFERABLE=YES" in health and "ZERO_CONTEXT_HUMAN_ACCEPTANCE=PASS" not in health:
    fail("FALSE_FULL_DIGESTION_CLAIM_IN_KNOWLEDGE_HEALTH")

print(f"WORKDESK_VALIDATION_ROOT={ROOT}")
print(f"SOURCE_ROWS={len(source)}")
print(f"UNIQUE_SOURCE_IDS={len(set(source_ids))}")
print(f"COVERAGE_ROWS={len(coverage)}")
print(f"CLAIMS={len(claims)}")
print(f"UNIQUE_CLAIM_IDS={len(set(claim_ids))}")
print(f"CONFLICT_ROWS={len(conflicts)}")
print(f"BOOT_MANIFEST_ROWS={len(boot_manifest)}")
print(f"CANDIDATE_FILES={len(files)}")
for w in warnings:
    print(f"WARNING={w}")
if errors:
    for e in errors:
        print(f"ERROR={e}")
    print("WORKDESK_STATIC_VALIDATION=FAIL")
    sys.exit(1)
print("SECRET_PATTERN_SCAN=PASS")
print("WIKILINK_VALIDATION=PASS")
print("CANVAS_VALIDATION=PASS")
print("OBSIDIAN_BASE_VALIDATION=PASS")
print("BOOT_MANIFEST_VALIDATION=PASS")
print("WORKDESK_STATIC_VALIDATION=PASS")
print("NOTE=Static PASS does not equal semantic-completeness PASS or canonical-ASB mutation.")

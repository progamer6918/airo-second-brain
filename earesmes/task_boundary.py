#!/usr/bin/env python3
"""
EARESMES Task Boundary — V1
============================
Deterministic task classification and safety boundary layer.

Governance limits enforced:
  - No model/AI calls
  - No autonomous planning
  - No command execution
  - No runner modification
  - Classification is metadata ONLY — never used to trigger execution

Standard library only. No external dependencies.

Usage (standalone):
    python3 earesmes/task_boundary.py "cek status VPS"
"""

import re
import sys
from typing import NamedTuple

# ---------------------------------------------------------------------------
# Classification result
# ---------------------------------------------------------------------------

VALID_CATEGORIES = {"maintenance", "development", "research", "architecture", "unknown"}
VALID_RISKS = {"low", "medium", "high"}
VALID_EXECUTOR_HINTS = {"local", "antigravity", "owner_review", "unknown"}


class BoundaryResult(NamedTuple):
    category: str           # maintenance | development | research | architecture | unknown
    risk: str               # low | medium | high
    approval_required: bool
    executor_hint: str      # local | antigravity | owner_review | unknown

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "risk": self.risk,
            "approval_required": self.approval_required,
            "executor_hint": self.executor_hint,
        }


# ---------------------------------------------------------------------------
# Rule table
# ---------------------------------------------------------------------------
# Each rule is a tuple of:
#   (keyword_patterns, category, risk, approval_required, executor_hint)
#
# Rules are evaluated in ORDER. First match wins.
# keyword_patterns: list of regex patterns (case-insensitive, word-boundary-safe).
# A rule matches when ANY pattern matches the normalised objective text.
#
# Governance: this is a pure lookup table — no inference, no model, no planning.
# ---------------------------------------------------------------------------

_RULES: list[tuple[list[str], str, str, bool, str]] = [
    # -- HIGH RISK -- architecture / destructive --------------------------------
    # Must come before medium/low to ensure destructive ops are caught first.
    (
        [
            r"\barchitect",          # architecture, architect
            r"\brefactor\b",
            r"\bredesign\b",
            r"\bmigrat",             # migrate, migration
            r"\boverhaul\b",
            r"\brestructur",
            r"\bubah\s+architect",   # "ubah architecture"
            r"\bubah\s+kcc\b",
            r"\bubah\s+asb\b",
            r"\bubah\s+sistem\b",
            r"\bubah\s+infrastruktur",
        ],
        "architecture", "high", True, "owner_review",
    ),
    (
        [
            r"\bhapus\b",            # hapus = delete (Indonesian)
            r"\bdelete\b",
            r"\bdrop\b",
            r"\bremove\b",
            r"\bpurge\b",
            r"\bwipe\b",
            r"\bdestroy\b",
            r"\breset\b",
            r"\bformat\b",
            r"\berase\b",
        ],
        "architecture", "high", True, "owner_review",
    ),

    # -- MEDIUM RISK -- development / documentation ----------------------------
    (
        [
            r"\bbuat\b",             # buat = create/make (Indonesian)
            r"\bcreate\b",
            r"\bbuild\b",
            r"\bdevelop\b",
            r"\bimplement",
            r"\badd\s+feature",
            r"\bfitur\b",            # fitur = feature (Indonesian)
            r"\bscript\b",
            r"\bcode\b",
            r"\bprogram\b",
            r"\bmodule\b",
            r"\bplugin\b",
            r"\bintegrat",
            r"\bdeploy\b",
            r"\brelease\b",
            r"\bupgrade\b",
            r"\binstall\b",
            r"\bsetup\b",
            r"\bkonfigurasi\b",      # konfigurasi = configure (Indonesian)
            r"\bconfigure\b",
        ],
        "development", "medium", True, "antigravity",
    ),
    (
        [
            r"\bupdate\b",
            r"\bdokumentasi\b",      # dokumentasi = documentation (Indonesian)
            r"\bdocumentation\b",
            r"\bdocs?\b",
            r"\bchangelog\b",
            r"\breadme\b",
            r"\btulis\b",           # tulis = write (Indonesian)
            r"\bwrite\b",
            r"\bedit\b",
            r"\bmodify\b",
            r"\bubah\b",            # ubah = change (Indonesian) -- generic, below arch rules
            r"\bpatch\b",
            r"\bfix\b",
            r"\bbugfix\b",
            r"\brepair\b",
            r"\boptimize\b",
            r"\boptimis",
            r"\brefine\b",
        ],
        "development", "medium", True, "antigravity",
    ),
    (
        [
            r"\bresearch\b",
            r"\banalyz",
            r"\banalis",             # analisis (Indonesian)
            r"\binvestigat",
            r"\bstudy\b",
            r"\bpelajari\b",        # pelajari = study/learn (Indonesian)
            r"\blearn\b",
            r"\bsurvey\b",
            r"\breview\b",
            r"\baudit\b",
            r"\btest\b",
            r"\btesting\b",
            r"\beksplor",           # eksplorasi (Indonesian)
            r"\bexplor",
        ],
        "research", "medium", True, "antigravity",
    ),

    # -- LOW RISK -- maintenance / read-only / status checks -------------------
    (
        [
            r"\bcek\b",             # cek = check (Indonesian)
            r"\bcheck\b",
            r"\bstatus\b",
            r"\blihat\b",           # lihat = view/look (Indonesian)
            r"\bview\b",
            r"\bshow\b",
            r"\blist\b",
            r"\bdisplay\b",
            r"\bmonitor\b",
            r"\bping\b",
            r"\btrace\b",
            r"\bdiagnostic",
            r"\bhealth\b",
            r"\buptime\b",
            r"\blog\b",
            r"\blogs\b",
            r"\bdisk\b",
            r"\bmemory\b",
            r"\bcpu\b",
            r"\bram\b",
            r"\bprocess\b",
            r"\bservice\b",
            r"\bservices\b",
            r"\brestart\s+service",
            r"\breload\s+service",
            r"\bvps\b",
            r"\bserver\b",
            r"\bbackup\b",
            r"\bverif",
            r"\bvalidat",
            r"\blaporan\b",          # laporan = report (Indonesian)
            r"\breport\b",
        ],
        "maintenance", "low", False, "local",
    ),
]

# Compile all patterns once at module load.
_COMPILED_RULES: list[tuple[list[re.Pattern], str, str, bool, str]] = [
    (
        [re.compile(p, re.IGNORECASE) for p in patterns],
        category, risk, approval_required, executor_hint,
    )
    for patterns, category, risk, approval_required, executor_hint in _RULES
]

# Default when no rule matches.
_DEFAULT_RESULT = BoundaryResult(
    category="unknown",
    risk="high",
    approval_required=True,
    executor_hint="unknown",
)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def classify(objective: str) -> BoundaryResult:
    """
    Classify an objective string using deterministic keyword rules.

    No model calls. No external I/O. Pure pattern matching.
    Returns a BoundaryResult; never raises on valid string input.
    """
    if not isinstance(objective, str) or not objective.strip():
        return _DEFAULT_RESULT

    text = objective.strip()

    for compiled_patterns, category, risk, approval_required, executor_hint in _COMPILED_RULES:
        for pattern in compiled_patterns:
            if pattern.search(text):
                return BoundaryResult(
                    category=category,
                    risk=risk,
                    approval_required=approval_required,
                    executor_hint=executor_hint,
                )

    return _DEFAULT_RESULT


# ---------------------------------------------------------------------------
# Standalone CLI (for testing / validation only)
# ---------------------------------------------------------------------------

def _main(argv: list[str] | None = None) -> int:
    import json as _json

    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print("Usage: python3 earesmes/task_boundary.py \"objective text\"", file=sys.stderr)
        return 1

    objective = argv[0]
    result = classify(objective)
    print(_json.dumps(result.to_dict(), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(_main())

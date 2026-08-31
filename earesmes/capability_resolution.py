#!/usr/bin/env python3
"""
EARESMES Capability Resolution — V1
=====================================
Deterministic capability metadata layer.

Governance limits enforced:
  - No model/AI calls
  - No autonomous planning
  - No command execution
  - No runner modification
  - Classification is metadata ONLY — never triggers execution

Resolves a human objective to a structured capability descriptor using
an ordered keyword rule table. First match wins. Standard library only.

Usage (standalone):
    python3 earesmes/capability_resolution.py "cek status VPS"
"""

import re
import sys
from typing import NamedTuple

# ---------------------------------------------------------------------------
# Capability result
# ---------------------------------------------------------------------------

VALID_CAPABILITIES = {
    "maintenance",
    "development",
    "airo_workdesk",
    "knowledge",
    "owner_review",
    "unknown",
}

VALID_EXECUTOR_HINTS = {
    "local",
    "antigravity",
    "awd_workflow",
    "asb_kcc",
    "owner",
    "unknown",
}

VALID_AUTHORITIES = {
    "earesmes_runner",
    "airo_workdesk_system",
    "asb_kcc_system",
    "owner_direct",
    "unresolved",
}


class CapabilityResult(NamedTuple):
    capability: str      # maintenance | development | airo_workdesk | knowledge | owner_review | unknown
    executor_hint: str   # local | antigravity | awd_workflow | asb_kcc | owner | unknown
    authority: str       # earesmes_runner | airo_workdesk_system | asb_kcc_system | owner_direct | unresolved
    reason: str          # human-readable rule match summary

    def to_dict(self) -> dict:
        return {
            "capability": self.capability,
            "executor_hint": self.executor_hint,
            "authority": self.authority,
            "reason": self.reason,
        }


# ---------------------------------------------------------------------------
# Rule table
# ---------------------------------------------------------------------------
# Each rule is a tuple of:
#   (keyword_patterns, capability, executor_hint, authority, reason)
#
# Rules are evaluated in ORDER. First match wins.
# keyword_patterns: list of regex patterns (case-insensitive).
# A rule fires when ANY pattern matches the objective text.
#
# Governance: pure lookup table — no inference, no model, no planning.
# ---------------------------------------------------------------------------

_RULES: list[tuple[list[str], str, str, str, str]] = [
    # ── OWNER REVIEW — destructive / architecture ──────────────────────────
    # Must be first to intercept high-risk objectives before lower-risk rules.
    (
        [
            r"\barchitect",          # architecture, architect
            r"\bdelete\b",
            r"\bhapus\b",            # hapus = delete (Indonesian)
            r"\bremove\b",
            r"\bmigrat",             # migrate, migration
            r"\bpurge\b",
            r"\bdrop\b",
            r"\bdestroy\b",
            r"\brestructur",
            r"\boverhaul\b",
        ],
        "owner_review",
        "owner",
        "owner_direct",
        "keyword match: architecture/destructive operation requires owner review",
    ),

    # ── AIRO WORKDESK — sales / market / territory / dealer ─────────────────
    (
        [
            r"\bsales\b",
            r"\bdealer\b",
            r"\bmarket\b",
            r"\bterritory\b",
            r"\bshare\b",
            r"\bflp\b",
            r"\bpasar\b",            # pasar = market (Indonesian)
            r"\bpenjualan\b",        # penjualan = sales (Indonesian)
            r"\bwilayah\b",          # wilayah = territory (Indonesian)
            r"\bdistribusi\b",       # distribusi = distribution (Indonesian)
            r"\banalisa\s+market",
            r"\banalisis\s+market",
        ],
        "airo_workdesk",
        "awd_workflow",
        "airo_workdesk_system",
        "keyword match: sales/market/territory/dealer routes to AIRO Workdesk",
    ),

    # ── KNOWLEDGE — session / obsidian / documentation / kcc ────────────────
    (
        [
            r"\bobsidian\b",
            r"\bkcc\b",
            r"\bknowledge\b",
            r"\bsession\b",
            r"\bdokumentasi\b",      # dokumentasi = documentation (Indonesian)
            r"\bdocumentation\b",
            r"\bdocs?\b",
            r"\bwiki\b",
            r"\bnote\b",
            r"\bnotes\b",
            r"\bcatatan\b",          # catatan = notes (Indonesian)
            r"\breadme\b",
            r"\bchangelog\b",
        ],
        "knowledge",
        "asb_kcc",
        "asb_kcc_system",
        "keyword match: knowledge/documentation/obsidian routes to ASB KCC",
    ),

    # ── DEVELOPMENT — code / script / feature / bug / implementation ─────────
    (
        [
            r"\bcode\b",
            r"\bscript\b",
            r"\bfeature\b",
            r"\bfitur\b",            # fitur = feature (Indonesian)
            r"\bbug\b",
            r"\bimplementat",
            r"\bimplement\b",
            r"\bbuat\b",             # buat = create/make (Indonesian)
            r"\bcreate\b",
            r"\bbuild\b",
            r"\bdevelop\b",
            r"\bplugin\b",
            r"\bmodule\b",
            r"\bintegrat",
            r"\bdeploy\b",
            r"\brelease\b",
            r"\binstall\b",
            r"\bsetup\b",
            r"\bconfigure\b",
            r"\bkonfigurasi\b",
            r"\bupgrade\b",
            r"\bfix\b",
            r"\bpatch\b",
            r"\brefine\b",
            r"\boptimiz",
        ],
        "development",
        "antigravity",
        "earesmes_runner",
        "keyword match: code/script/feature/implementation routes to development",
    ),

    # ── MAINTENANCE — vps / server / service / disk / memory / system ────────
    (
        [
            r"\bvps\b",
            r"\bserver\b",
            r"\bservice\b",
            r"\bservices\b",
            r"\bdisk\b",
            r"\bmemory\b",
            r"\bram\b",
            r"\bcpu\b",
            r"\bsystem\b",
            r"\bsistem\b",           # sistem = system (Indonesian)
            r"\bcek\b",              # cek = check (Indonesian)
            r"\bcheck\b",
            r"\bstatus\b",
            r"\blihat\b",            # lihat = view/look (Indonesian)
            r"\bmonitor\b",
            r"\bping\b",
            r"\bhealth\b",
            r"\buptime\b",
            r"\blog\b",
            r"\bdisk\b",
            r"\bprocess\b",
            r"\bbackup\b",
            r"\bdiagnostic",
            r"\brestart\b",
            r"\breload\b",
        ],
        "maintenance",
        "local",
        "earesmes_runner",
        "keyword match: vps/server/service/disk/memory routes to maintenance",
    ),
]

# Compile all patterns once at module load.
_COMPILED_RULES: list[tuple[list[re.Pattern], str, str, str, str]] = [
    (
        [re.compile(p, re.IGNORECASE) for p in patterns],
        capability, executor_hint, authority, reason,
    )
    for patterns, capability, executor_hint, authority, reason in _RULES
]

# Default when no rule matches.
_DEFAULT_RESULT = CapabilityResult(
    capability="unknown",
    executor_hint="unknown",
    authority="unresolved",
    reason="no matching capability rule — defaulting to unknown/owner review",
)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def resolve(objective: str) -> CapabilityResult:
    """
    Resolve an objective string to a capability descriptor.

    Deterministic keyword rules only. No model calls. No external I/O.
    Returns a CapabilityResult; never raises on valid string input.
    """
    if not isinstance(objective, str) or not objective.strip():
        return _DEFAULT_RESULT

    text = objective.strip()

    for compiled_patterns, capability, executor_hint, authority, reason in _COMPILED_RULES:
        for pattern in compiled_patterns:
            if pattern.search(text):
                return CapabilityResult(
                    capability=capability,
                    executor_hint=executor_hint,
                    authority=authority,
                    reason=reason,
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
        print(
            "Usage: python3 earesmes/capability_resolution.py \"objective text\"",
            file=sys.stderr,
        )
        return 1

    objective = argv[0]
    result = resolve(objective)
    print(_json.dumps(result.to_dict(), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(_main())

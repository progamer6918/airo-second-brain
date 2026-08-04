#!/usr/bin/env python3
"""
asb-governance-regression-test: Automated governance regression test suite for AIRO Second Brain.
Verifies retention of critical governance markers, project pointers, and absence of absolute file URIs.
"""
import sys
import os
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def check_file_contains(rel_path, required_markers):
    filepath = os.path.join(REPO_ROOT, rel_path)
    if not os.path.exists(filepath):
        print(f"  [FAIL] Missing file: {rel_path}")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    missing = []
    for marker in required_markers:
        if marker not in content:
            missing.append(marker)

    if missing:
        print(f"  [FAIL] {rel_path} missing markers: {', '.join(missing)}")
        return False
    else:
        print(f"  [PASS] {rel_path} contains all {len(required_markers)} required markers.")
        return True

def check_no_absolute_file_uris():
    canonical_docs = [
        "BOOT.md",
        "AGENTS.md",
        "SECURITY.md",
        "PRD_INDEX.md",
        "ROADMAP_INDEX.md",
        "docs/prd/AIRO_SECOND_BRAIN_PRD_v0.6.0.md",
        "docs/specs/asb/AIRO_SECOND_BRAIN_v0.6_DESIGN_SPEC.md",
        "decisions/approved/asb-v06-architecture-owner-approval-20260804.md",
        "docs/evidence/ASB_v0.6_DESIGN_SESSION_SYNTHESIS_20260804.md",
        "docs/roadmap/AIRO_SECOND_BRAIN_v0.6_ROADMAP.md",
        "docs/contracts/AIRO_STATUS_CONTRACT.md",
        "docs/contracts/AIRO_EXECUTION_EVIDENCE_CONTRACT.md"
    ]

    failed = False
    print("Checking for illegal absolute file URIs (file:///home/... or file:///C:/)...")
    for rel_path in canonical_docs:
        filepath = os.path.join(REPO_ROOT, rel_path)
        if not os.path.exists(filepath):
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        matches = re.findall(r"file:///(?:home|C:)[^\s\)\"\'>]+", content)
        if matches:
            print(f"  [FAIL] {rel_path} contains absolute file URIs: {matches[:3]}")
            failed = True

    if not failed:
        print("  [PASS] No absolute file URIs found in canonical v0.6 documentation.")
        return True
    return False

def run_suite():
    tests = [
        ("BOOT.md Markers", "BOOT.md", [
            "Latest Evidence Resolution Protocol",
            "WSL Safety & Git Safety Rules",
            "Mandatory AIRO Finance AFPD Boot Guard",
            "Mandatory Telegram Agent Identity Guard",
            "Mandatory Earesmes-Arfin Bridge (EAB) Boot Guard",
            "🧭 AIRO STATUS",
            "EXIT_CODE=0",
            "BERHASIL",
            "state/operating-rules/AIRO_ANTIGRAVITY_LOW_LIMIT_NO_BRAINER_MODE_20260705.md",
            "state/operating-rules/AIRO_CHAT_STABILITY_PROTOCOL_20260704.md"
        ]),
        ("AGENTS.md Markers", "AGENTS.md", [
            "Source Priority",
            "inbox/session-closeouts/",
            "Telegram Gateway & Callback Rules",
            "Never Store",
            "AIRO Operator Answer Contract",
            "AIRO Finance AFPD Boot Guard",
            "Telegram Identity Guard",
            "🧭 AIRO STATUS"
        ]),
        ("ROADMAP_INDEX.md Project Pointers", "ROADMAP_INDEX.md", [
            "ASB_GLOBAL",
            "AIRO Finance",
            "Earesmes / Hermes",
            "D-READY",
            "Report Automation VBA",
            "Earesmes-Arfin Bridge (EAB)",
            "AIRO Finance - Dashboard Lite Re-scope Pointer"
        ]),
        ("PRD_INDEX.md Project Pointers", "PRD_INDEX.md", [
            "AIRO_SECOND_BRAIN_PRD_v0.6.0.md",
            "AIRO_SECOND_BRAIN_PRD_v0.5.1.md",
            "AIRO_FINANCE_WEB_APP_V2_PRD_ADDENDUM.md",
            "D-READY",
            "Earesmes-Arfin Bridge (EAB)",
            "ACTIVE_CANONICAL"
        ]),
        ("SECURITY.md Safety Rules", "SECURITY.md", [
            "The AIRO Second Brain repository is PUBLIC.",
            "What Must Never Be Committed",
            "Google Workspace & Credentials",
            "Allowed vs Forbidden Public Content"
        ])
    ]

    passed = 0
    total = len(tests) + 1 # include absolute URI check

    print(f"Running {total} ASB governance regression checks...")
    for name, rel_path, markers in tests:
        if check_file_contains(rel_path, markers):
            passed += 1

    if check_no_absolute_file_uris():
        passed += 1

    print(f"\nGovernance Regression Test Results: {passed}/{total} passed.")
    if passed == total:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    run_suite()

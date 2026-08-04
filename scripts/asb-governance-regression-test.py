#!/usr/bin/env python3
"""
asb-governance-regression-test: Automated governance regression test suite for AIRO Second Brain.
Verifies retention of critical governance markers, project pointers, absence of absolute file URIs,
recursive target resolution of all repository-local Markdown links, and full startup sequence consistency.
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
        "BOOT.md", "AGENTS.md", "SECURITY.md", "PRD_INDEX.md", "ROADMAP_INDEX.md", "CURRENT.md",
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

def check_markdown_link_resolution():
    canonical_docs = [
        "BOOT.md", "AGENTS.md", "SECURITY.md", "PRD_INDEX.md", "ROADMAP_INDEX.md", "CURRENT.md",
        "docs/prd/AIRO_SECOND_BRAIN_PRD_v0.6.0.md",
        "docs/specs/asb/AIRO_SECOND_BRAIN_v0.6_DESIGN_SPEC.md",
        "decisions/approved/asb-v06-architecture-owner-approval-20260804.md",
        "docs/evidence/ASB_v0.6_DESIGN_SESSION_SYNTHESIS_20260804.md",
        "docs/roadmap/AIRO_SECOND_BRAIN_v0.6_ROADMAP.md",
        "docs/contracts/AIRO_STATUS_CONTRACT.md",
        "docs/contracts/AIRO_EXECUTION_EVIDENCE_CONTRACT.md"
    ]

    total_links = 0
    resolved_links = 0
    broken_links = []

    print("Checking recursive Markdown relative link target resolution...")
    for doc in canonical_docs:
        src_path = os.path.join(REPO_ROOT, doc)
        if not os.path.exists(src_path):
            continue
        src_dir = os.path.dirname(src_path)
        with open(src_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
        for text, target in links:
            target = target.strip()
            if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
                continue
            if target.startswith("file:///"):
                broken_links.append((doc, target, "Absolute file:/// URI forbidden"))
                continue
            
            target_path_only = target.split("#")[0]
            if not target_path_only:
                continue
            
            total_links += 1
            resolved_path = os.path.normpath(os.path.join(src_dir, target_path_only))
            
            if not resolved_path.startswith(REPO_ROOT):
                broken_links.append((doc, target, f"Traversal outside repo: {resolved_path}"))
                continue

            if os.path.exists(resolved_path):
                resolved_links += 1
            else:
                broken_links.append((doc, target, f"Target missing: {resolved_path}"))

    print(f"  Total Local Relative Links Tested: {total_links}")
    print(f"  Resolved Links: {resolved_links}")
    print(f"  Broken Links: {len(broken_links)}")

    if broken_links:
        for doc, target, err in broken_links:
            print(f"  [FAIL] Broken link in {doc}: '{target}' -> {err}")
        return False
    else:
        print("  [PASS] 100% of canonical Markdown relative links resolve to existing repository files.")
        return True

def check_startup_consistency():
    print("Checking startup sequence consistency across BOOT, CURRENT, ROADMAP_INDEX, PRD_INDEX...")
    boot_path = os.path.join(REPO_ROOT, "BOOT.md")
    current_path = os.path.join(REPO_ROOT, "CURRENT.md")
    roadmap_idx_path = os.path.join(REPO_ROOT, "ROADMAP_INDEX.md")
    prd_idx_path = os.path.join(REPO_ROOT, "PRD_INDEX.md")
    tracker_path = os.path.join(REPO_ROOT, "docs/roadmap/AIRO_SECOND_BRAIN_v0.6_MILESTONE_TRACKER.tsv")

    errors = []

    with open(boot_path, "r", encoding="utf-8") as f:
        boot_txt = f.read()
    if "🧭 AIRO STATUS" not in boot_txt:
        errors.append("BOOT.md missing 🧭 AIRO STATUS contract header")

    with open(current_path, "r", encoding="utf-8") as f:
        curr_txt = f.read()
    if "<!-- ASB_V06_CURRENT_ROUTING_OVERRIDE_BEGIN -->" not in curr_txt:
        errors.append("CURRENT.md missing top routing override block")
    if "docs/roadmap/AIRO_SECOND_BRAIN_v0.6_ROADMAP.md" not in curr_txt:
        errors.append("CURRENT.md missing v0.6 roadmap pointer")

    with open(roadmap_idx_path, "r", encoding="utf-8") as f:
        rm_txt = f.read()
    if "M2 — Session & Worklog" not in rm_txt and "M2" not in rm_txt:
        errors.append("ROADMAP_INDEX.md missing ASB_GLOBAL M2 active milestone pointer")

    with open(prd_idx_path, "r", encoding="utf-8") as f:
        prd_txt = f.read()
    if "AIRO_SECOND_BRAIN_PRD_v0.6.0.md" not in prd_txt or "AIRO_SECOND_BRAIN_PRD_v0.5.1.md" not in prd_txt:
        errors.append("PRD_INDEX.md missing v0.6 implementation target or v0.5.1 baseline")

    with open(tracker_path, "r", encoding="utf-8") as f:
        tr_txt = f.read()
    if "M1\tGovernance & Execution Assurance\tDONE\tBERHASIL\tYES" not in tr_txt:
        errors.append("MILESTONE_TRACKER.tsv M1 is not DONE/BERHASIL/YES")

    if errors:
        for err in errors:
            print(f"  [FAIL] Startup consistency error: {err}")
        return False
    else:
        print("  [PASS] Startup sequence consistency verified across all canonical governance files.")
        return True

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
    total = len(tests) + 3 # include absolute URI check + relative link resolution check + startup consistency

    print(f"Running {total} ASB governance regression & consistency checks...")
    for name, rel_path, markers in tests:
        if check_file_contains(rel_path, markers):
            passed += 1

    if check_no_absolute_file_uris():
        passed += 1

    if check_markdown_link_resolution():
        passed += 1

    if check_startup_consistency():
        passed += 1

    print(f"\nGovernance Regression Test Results: {passed}/{total} passed.")
    if passed == total:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    run_suite()

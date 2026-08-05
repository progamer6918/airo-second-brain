#!/usr/bin/env python3
"""
airo-v06-final-acceptance-test.py: Final Acceptance Test Suite for AIRO Second Brain v0.6 M6 Closeout.
Tests deterministic read-only system reality across 12 required cutover acceptance checks.
"""

import os
import sys
import re
import csv
import subprocess

def get_repo_root():
    if os.environ.get("AIRO_REPO_ROOT"):
        return os.path.abspath(os.environ.get("AIRO_REPO_ROOT"))
    cand = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    if os.path.exists(os.path.join(cand, "HOME.md")):
        return cand
    return "/home/egitaristorandas/AI_WORKSPACES/airo-second-brain"

def run_final_acceptance_test_suite():
    repo_root = get_repo_root()
    passed = 0
    total = 12

    print(f"Running 12 AIRO Second Brain v0.6 Final Acceptance test cases (repo: {repo_root})...")

    # T1: Owner M6 Decision Exists & Approved
    dec_path = os.path.join(repo_root, "decisions/approved/asb-v06-m6-owner-acceptance-20260805.md")
    t1_pass = False
    if os.path.exists(dec_path):
        with open(dec_path, "r", encoding="utf-8") as f:
            dtxt = f.read()
        if "OWNER_M6_ACCEPTANCE=APPROVED" in dtxt and "APPROVED_BY_OWNER" in dtxt:
            t1_pass = True
    if t1_pass:
        print("  [PASS] T1: Owner M6 decision document exists with APPROVED marker (OWNER_M6_DECISION=PASS)")
        passed += 1
    else:
        print("  [FAIL] T1: Owner M6 decision document missing or unapproved")

    # T2: Tracker M0-M6 all DONE / BERHASIL / YES
    tracker_path = os.path.join(repo_root, "docs/roadmap/AIRO_SECOND_BRAIN_v0.6_MILESTONE_TRACKER.tsv")
    t2_pass = False
    if os.path.exists(tracker_path):
        with open(tracker_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            rows = {row.get("MILESTONE", "").strip(): row for row in reader}
        m0_m6 = [f"M{i}" for i in range(7)]
        m_states = [rows.get(m, {}).get("STATUS", "").strip() == "DONE" for m in m0_m6]
        if all(m_states):
            t2_pass = True
    if t2_pass:
        print("  [PASS] T2: Milestone tracker records M0-M6 all DONE / BERHASIL / YES (TRACKER_M0_M6_DONE=PASS)")
        passed += 1
    else:
        print("  [FAIL] T2: Milestone tracker has non-DONE milestones M0-M6")

    # T3: Roadmap says M6 DONE and v0.6 complete
    roadmap_path = os.path.join(repo_root, "docs/roadmap/AIRO_SECOND_BRAIN_v0.6_ROADMAP.md")
    t3_pass = False
    if os.path.exists(roadmap_path):
        with open(roadmap_path, "r", encoding="utf-8") as f:
            rmtxt = f.read()
        if "M6 — Owner Acceptance & Cutover** (`DONE`" in rmtxt or "Milestone 6 — Owner Acceptance & Cutover (`DONE`)" in rmtxt:
            if "roadmap complete" in rmtxt or "All seven canonical milestones M0-M6 are DONE" in rmtxt:
                t3_pass = True
    if t3_pass:
        print("  [PASS] T3: Roadmap records M6 DONE and v0.6 roadmap complete (ROADMAP_M6_COMPLETE=PASS)")
        passed += 1
    else:
        print("  [FAIL] T3: Roadmap does not record M6 DONE and complete")

    # T4: CURRENT says v0.6 complete / M6 DONE
    current_path = os.path.join(repo_root, "CURRENT.md")
    t4_pass = False
    if os.path.exists(current_path):
        with open(current_path, "r", encoding="utf-8") as f:
            ctxt = f.read()
        if "AIRO Second Brain v0.6 — COMPLETE" in ctxt or "M6_STATUS=DONE" in ctxt:
            t4_pass = True
    if t4_pass:
        print("  [PASS] T4: CURRENT.md records v0.6 complete / M6 DONE (CURRENT_V06_COMPLETE=PASS)")
        passed += 1
    else:
        print("  [FAIL] T4: CURRENT.md missing v0.6 complete status")

    # T5: ROADMAP_INDEX says v0.6 complete / no active milestone
    ri_path = os.path.join(repo_root, "ROADMAP_INDEX.md")
    t5_pass = False
    if os.path.exists(ri_path):
        with open(ri_path, "r", encoding="utf-8") as f:
            ritxt = f.read()
        if "V0_6_COMPLETE" in ritxt or "M0-M6 DONE" in ritxt:
            t5_pass = True
    if t5_pass:
        print("  [PASS] T5: ROADMAP_INDEX.md records ASB_GLOBAL v0.6 complete (ROADMAP_INDEX_COMPLETE=PASS)")
        passed += 1
    else:
        print("  [FAIL] T5: ROADMAP_INDEX missing v0.6 complete status")

    # T6: PRD says M6 DONE / implementation complete
    prd_path = os.path.join(repo_root, "docs/prd/AIRO_SECOND_BRAIN_PRD_v0.6.0.md")
    t6_pass = False
    if os.path.exists(prd_path):
        with open(prd_path, "r", encoding="utf-8") as f:
            prdtxt = f.read()
        if "M6 — Owner Acceptance & Cutover** (DONE" in prdtxt or "IMPLEMENTATION_STATE=COMPLETE_OWNER_ACCEPTED" in prdtxt:
            t6_pass = True
    if t6_pass:
        print("  [PASS] T6: PRD v0.6 records M6 DONE / implementation complete (PRD_M6_COMPLETE=PASS)")
        passed += 1
    else:
        print("  [FAIL] T6: PRD missing M6 DONE status")

    # T7: Single physical repository identity
    legacy_path = "/home/egitaristorandas/AI_WORKSPACES/airo-second-brain"
    win_wsl_path = "/mnt/c/Users/Admin/AI_WORKSPACES/airo-second-brain"
    t7_pass = os.path.exists(legacy_path) and os.path.exists(win_wsl_path) and (os.path.realpath(legacy_path) == os.path.realpath(win_wsl_path))
    if t7_pass:
        print("  [PASS] T7: Legacy WSL path and Windows direct path share single repository identity (SINGLE_REPOSITORY_IDENTITY=PASS)")
        passed += 1
    else:
        print("  [FAIL] T7: Single repository identity failed")

    # T8: Windows native path readable
    ps_cmd = 'Test-Path "C:\\Users\\Admin\\AI_WORKSPACES\\airo-second-brain\\HOME.md"'
    res_t8 = subprocess.run(["powershell.exe", "-Command", ps_cmd], capture_output=True, text=True)
    t8_pass = "True" in res_t8.stdout
    if t8_pass:
        print("  [PASS] T8: Windows native path is readable via PowerShell (WINDOWS_NATIVE_PATH_READABLE=PASS)")
        passed += 1
    else:
        print("  [FAIL] T8: Windows native path unreadable")

    # T9: No stale Windows Scheduled Task UNC reference
    ps_cmd9 = 'Get-ScheduledTask | Where-Object { $_.TaskName -like "*AIRO*" } | Select-Object -ExpandProperty Actions | Select-Object -ExpandProperty Arguments'
    res_t9 = subprocess.run(["powershell.exe", "-Command", ps_cmd9], capture_output=True, text=True)
    t9_pass = ("wsl.localhost" not in res_t9.stdout) and ("home/egitaristorandas" not in res_t9.stdout)
    if t9_pass:
        print("  [PASS] T9: Windows Scheduled Task actions contain 0 stale UNC references (WINDOWS_TASK_REFERENCE_COMPATIBILITY=PASS)")
        passed += 1
    else:
        print("  [FAIL] T9: Stale UNC path found in Windows Scheduled Tasks")

    # T10: Runtime Sync remains disabled
    ps_cmd10 = '(Get-ScheduledTask -TaskName "*Runtime Sync*").State'
    res_t10 = subprocess.run(["powershell.exe", "-Command", ps_cmd10], capture_output=True, text=True)
    t10_pass = "Disabled" in res_t10.stdout
    if t10_pass:
        print("  [PASS] T10: AIRO Second Brain Runtime Sync task remains disabled (RUNTIME_SYNC_REMAINS_DISABLED=PASS)")
        passed += 1
    else:
        print("  [FAIL] T10: Runtime Sync task is not disabled")

    # T11: Rollback copy, if present, is inactive
    rollback_path = "/home/egitaristorandas/AI_WORKSPACES/airo-second-brain.pre-windows-cutover-20260805_204335"
    t11_pass = True
    if os.path.exists(rollback_path):
        if os.path.realpath(rollback_path) == os.path.realpath(repo_root):
            t11_pass = False
    if t11_pass:
        print("  [PASS] T11: Rollback repository copy, if present, is inactive and non-canonical (ROLLBACK_COPY_INACTIVE=PASS)")
        passed += 1
    else:
        print("  [FAIL] T11: Rollback copy is active")

    # T12: M1-M5 evidence pointers resolve to existing files
    m_pointers = [
        "docs/validation/AIRO_SECOND_BRAIN_v0.6_M1_CLOSEOUT_20260804.md",
        "docs/validation/AIRO_SECOND_BRAIN_v0.6_M2_EXECUTION_ASSURANCE_CORRECTION_20260804.md",
        "docs/validation/AIRO_SECOND_BRAIN_v0.6_M3_CLOSEOUT_20260805.md",
        "docs/validation/AIRO_SECOND_BRAIN_v0.6_M4_CLOSEOUT_20260805.md",
        "docs/validation/AIRO_SECOND_BRAIN_v0.6_M5_CLOSEOUT_20260805.md"
    ]
    t12_pass = all(os.path.exists(os.path.join(repo_root, p)) for p in m_pointers)
    if t12_pass:
        print("  [PASS] T12: All M1-M5 canonical closeout evidence pointers resolve to existing files (M1_M5_EVIDENCE_RESOLVED=PASS)")
        passed += 1
    else:
        print("  [FAIL] T12: M1-M5 evidence pointer missing")

    print(f"\nAIRO Second Brain v0.6 Final Acceptance Test Results: {passed}/{total} passed.")
    if passed == total:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    run_final_acceptance_test_suite()

#!/usr/bin/env python3
"""
Validation Test Suite for AIRO Session Projection Synchronization
Tests START sync, CLOSE sync, fault tolerance, and git isolation.
Contract: docs/contracts/AIRO_SESSION_PROJECTION_SYNC_CONTRACT.md
"""
import os
import sys
import json
import subprocess
import tempfile
import shutil

IDLE_CARD = """# ⚪ Tidak Ada Sesi Aktif

Belum ada pekerjaan aktif yang perlu dilanjutkan.
"""

def run_tests():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    print(f"Running Projection Sync Tests against repo: {repo_root}")
    
    airo_session = os.path.join(repo_root, "bin/airo-session")
    sync_script = os.path.join(repo_root, "scripts/airo-session-projection-sync")
    proj_file = os.path.join(repo_root, "state/active-session.md")
    
    assert os.path.exists(airo_session), "bin/airo-session must exist"
    assert os.path.exists(sync_script), "scripts/airo-session-projection-sync must exist"

    passed = 0
    total = 0

    # Ensure clean starting state
    initial_git = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_root, capture_output=True, text=True)
    initial_head = initial_git.stdout.strip()
    subprocess.run([sys.executable, sync_script, "reset", "--repo-root", repo_root], capture_output=True)


    # -------------------------------------------------------------
    # TEST 1: Direct helper status & reset
    # -------------------------------------------------------------
    total += 1
    st_res = subprocess.run([sys.executable, sync_script, "status", "--repo-root", repo_root], capture_output=True, text=True)
    if "PROJECTION_STATUS=PROJECTION_IDLE" in st_res.stdout:
        print("  [PASS] Test 1: Helper reports PROJECTION_IDLE on reset state")
        passed += 1
    else:
        print(f"  [FAIL] Test 1: Expected PROJECTION_IDLE, got: {st_res.stdout}")

    # -------------------------------------------------------------
    # TEST 2: Start session updates projection markdown
    # -------------------------------------------------------------
    total += 1
    test_proj = "Test_Sync_Project"
    test_obj = "Validate automated projection synchronization on session start"
    test_pos = "Testing start sync"
    
    start_res = subprocess.run([
        sys.executable, airo_session, "start",
        "--project-id", "test-sync-project",
        "--project-name", test_proj,
        "--objective", test_obj,
        "--title", "Projection Start Sync Verification",
        "--position", test_pos
    ], cwd=repo_root, capture_output=True, text=True)

    if "PROJECTION_SYNC=START_UPDATED" in start_res.stdout:
        with open(proj_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        has_proj = f"### 🟢 {test_proj}" in content
        has_obj = test_obj in content
        has_sid = "**Session ID**" in content
        has_ts = "**Dimulai Pada**" in content
        
        cw_file = os.path.join(repo_root, "runtime/workdesk/current-work.md")
        has_cw = os.path.exists(cw_file) and f"| {test_proj} |" in open(cw_file, "r", encoding="utf-8").read()

        if has_proj and has_obj and has_sid and has_ts and has_cw:
            print("  [PASS] Test 2: bin/airo-session start successfully updates state/active-session.md & runtime/workdesk/current-work.md")
            passed += 1
        else:
            print(f"  [FAIL] Test 2: Projection content missing required fields (has_proj={has_proj}, has_cw={has_cw})")
    else:
        print(f"  [FAIL] Test 2: PROJECTION_SYNC=START_UPDATED missing in stdout: {start_res.stdout} (stderr: {start_res.stderr})")

    # -------------------------------------------------------------
    # TEST 3: Close session clears projection back to canonical idle
    # -------------------------------------------------------------
    total += 1
    close_res = subprocess.run([
        sys.executable, airo_session, "close",
        "--script-status", "SCRIPT_SUCCESS"
    ], cwd=repo_root, capture_output=True, text=True)

    if "PROJECTION_SYNC=CLOSE_RESET" in close_res.stdout:
        with open(proj_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        cw_file = os.path.join(repo_root, "runtime/workdesk/current-work.md")
        cw_idle = os.path.exists(cw_file) and "Tidak ada pekerjaan aktif" in open(cw_file, "r", encoding="utf-8").read()

        if content.strip() == IDLE_CARD.strip() and cw_idle:
            print("  [PASS] Test 3: bin/airo-session close successfully resets state/active-session.md & current-work.md to idle")
            passed += 1
        else:
            print(f"  [FAIL] Test 3: Projection content is not idle card (proj={content.strip() == IDLE_CARD.strip()}, cw={cw_idle})")
    else:
        print(f"  [FAIL] Test 3: PROJECTION_SYNC=CLOSE_RESET missing in stdout: {close_res.stdout} (stderr: {close_res.stderr})")

    # -------------------------------------------------------------
    # TEST 4: Projection fault tolerance (lifecycle must survive failure)
    # -------------------------------------------------------------
    total += 1
    # Rename sync script temporarily to simulate missing/broken helper
    backup_script = sync_script + ".bak"
    shutil.move(sync_script, backup_script)
    try:
        fault_start = subprocess.run([
            sys.executable, airo_session, "start",
            "--project-id", "fault-test",
            "--project-name", "Fault_Test",
            "--objective", "Verify fault tolerance when sync helper missing"
        ], cwd=repo_root, capture_output=True, text=True)

        session_started = "SESSION_ACTION=STARTED" in fault_start.stdout
        
        fault_close = subprocess.run([
            sys.executable, airo_session, "close",
            "--script-status", "SCRIPT_SUCCESS"
        ], cwd=repo_root, capture_output=True, text=True)

        session_closed = "SESSION_CLOSED=YES" in fault_close.stdout

        if session_started and session_closed:
            print("  [PASS] Test 4: Session lifecycle continues safely even if projection helper is absent")
            passed += 1
        else:
            print("  [FAIL] Test 4: Session lifecycle broke when sync helper was absent")
    finally:
        shutil.move(backup_script, sync_script)

    # -------------------------------------------------------------
    # TEST 5: Git isolation check (no auto commits or pushes)
    # -------------------------------------------------------------
    total += 1
    git_res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_root, capture_output=True, text=True)
    current_head = git_res.stdout.strip()
    
    # Verify latest commit is untouched, not mutated by projection sync
    if current_head == initial_head:
        print(f"  [PASS] Test 5: Git history unmutated by projection sync (HEAD: '{current_head[:8]}')")
        passed += 1
    else:
        print(f"  [FAIL] Test 5: Unexpected commit found (expected '{initial_head[:8]}', got '{current_head[:8]}')")


    print(f"\nProjection Sync Test Results: {passed}/{total} passed.")
    return passed == total

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

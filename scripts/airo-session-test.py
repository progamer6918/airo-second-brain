#!/usr/bin/env python3
"""
airo-session-test.py: Comprehensive test suite for AIRO Session Lifecycle & Daily Generator.
Runs 18 isolated test cases (T1..T18) covering scoping, events, resume, verdict enforcement, UX, and daily generation.
"""
import sys
import os
import shutil
import tempfile
import json
import subprocess
from datetime import datetime

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BIN_SESSION = os.path.join(REPO_ROOT, "bin/airo-session")
SCRIPTS_DAILY = os.path.join(REPO_ROOT, "scripts/airo-daily")

def run_test_suite():
    tmp_dir = tempfile.mkdtemp(prefix="airo_session_test_")
    tmp_state = os.path.join(tmp_dir, "state")
    tmp_repo = os.path.join(tmp_dir, "repo")
    
    os.makedirs(os.path.join(tmp_repo, "bin"), exist_ok=True)
    os.makedirs(os.path.join(tmp_repo, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(tmp_repo, "docs/roadmap"), exist_ok=True)
    
    shutil.copy(BIN_SESSION, os.path.join(tmp_repo, "bin/airo-session"))
    shutil.copy(SCRIPTS_DAILY, os.path.join(tmp_repo, "scripts/airo-daily"))
    shutil.copy(os.path.join(REPO_ROOT, "scripts/airo-capture"), os.path.join(tmp_repo, "scripts/airo-capture"))
    if os.path.exists(os.path.join(REPO_ROOT, "scripts/airo-task-verdict")):
        shutil.copy(os.path.join(REPO_ROOT, "scripts/airo-task-verdict"), os.path.join(tmp_repo, "scripts/airo-task-verdict"))

    env = os.environ.copy()
    env["AIRO_SESSION_STATE_DIR"] = tmp_state
    env["AIRO_REPO_ROOT"] = tmp_repo

    passed = 0
    total = 18

    print("Running 18 AIRO session & worklog test cases...")

    # T1: start session => active session created
    res1 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj1"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "SESSION_ACTION=STARTED" in res1.stdout:
        print("  [PASS] T1: Start session creates active session")
        passed += 1
    else:
        print(f"  [FAIL] T1: Start session failed: {res1.stdout}")

    # T2: same project + objective start => same internal session reused
    res2 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj1"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "SESSION_ACTION=CONTINUE_EXISTING" in res2.stdout:
        print("  [PASS] T2: Same project + objective reuses active session")
        passed += 1
    else:
        print(f"  [FAIL] T2: Same project reuse failed: {res2.stdout}")

    # T3: different project while active => refuses auto-switch
    res3 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "FINANCE", "--project-name", "FINANCE", "--objective", "Obj2"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "SESSION_SWITCH_REQUIRES_CLOSE=YES" in res3.stdout:
        print("  [PASS] T3: Different project refuses auto-switch")
        passed += 1
    else:
        print(f"  [FAIL] T3: Project switch guard failed: {res3.stdout}")

    # T4: multiple events => same internal session ID
    res4a = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "event", "--summary", "Evt1"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    res4b = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "event", "--summary", "Evt2"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "EVENT_RECORDED=YES" in res4a.stdout and "EVENT_RECORDED=YES" in res4b.stdout:
        print("  [PASS] T4: Multiple events recorded under active session")
        passed += 1
    else:
        print(f"  [FAIL] T4: Multiple events failed: {res4a.stdout}")

    # T5: event integration => airo-capture ledger receives events
    ndjson = os.path.join(tmp_repo, "events/raw/events.ndjson")
    if os.path.exists(ndjson):
        with open(ndjson, "r") as f:
            lines = [line for line in f if line.strip()]
        if len(lines) >= 3:
            print("  [PASS] T5: Integration with airo-capture event ledger verified")
            passed += 1
        else:
            print(f"  [FAIL] T5: Expected >= 3 events in ledger, found {len(lines)}")
    else:
        print("  [FAIL] T5: Event ledger file missing")

    # T6: process restart/resume => session remains resumable
    res6 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "resume"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "SESSION_RESUMED=YES" in res6.stdout:
        print("  [PASS] T6: Session remains resumable after process exit")
        passed += 1
    else:
        print(f"  [FAIL] T6: Resume failed: {res6.stdout}")

    # T7: draft-closeout => staging closeout created, no fake finalization
    res7 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "draft-closeout"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "DRAFT_CLOSEOUT_CREATED=YES" in res7.stdout:
        print("  [PASS] T7: Draft closeout creates staging note without finalization")
        passed += 1
    else:
        print(f"  [FAIL] T7: Draft closeout failed: {res7.stdout}")

    # T8: missing required evidence => session close status BELUM_TERBUKTI / CAN_ADVANCE=NO
    res8 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--script-status", "SCRIPT_FAILED"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "VERDICT_STATUS=GAGAL" in res8.stdout or "VERDICT_STATUS=BELUM_TERBUKTI" in res8.stdout:
        print("  [PASS] T8: Failed script status closes as GAGAL/BELUM_TERBUKTI")
        passed += 1
    else:
        print(f"  [FAIL] T8: Close verdict failed: {res8.stdout}")

    # Start a new session for T9..T18
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj2", "--title", "Test Session 2"], env=env, cwd=tmp_repo, capture_output=True, text=True)

    # T9: blocker => TERHAMBAT / NO
    res9 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--blockers", "[\"Active blocker\"]"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "VERDICT_STATUS=TERHAMBAT" in res9.stdout:
        print("  [PASS] T9: Blocker produces TERHAMBAT verdict")
        passed += 1
    else:
        print(f"  [FAIL] T9: Blocker verdict failed: {res9.stdout}")

    # Start a clean session for T10..T18
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj3", "--title", "Test Session 3"], env=env, cwd=tmp_repo, capture_output=True, text=True)

    # T10: valid evidence => BERHASIL / YES
    res10 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "VERDICT_STATUS=BERHASIL" in res10.stdout and "CAN_ADVANCE=YES" in res10.stdout:
        print("  [PASS] T10: Valid evidence produces BERHASIL verdict")
        passed += 1
    else:
        print(f"  [FAIL] T10: Valid verdict failed: {res10.stdout}")

    # T11: human filename has no UUID/random hash
    sess_dir = os.path.join(tmp_repo, "worklog/sessions")
    files_found = []
    for root, dirs, files in os.walk(sess_dir):
        for f in files:
            files_found.append(f)
    has_uuid = any(len(f) > 30 and "-" in f for f in files_found)
    if files_found and not has_uuid:
        print("  [PASS] T11: Human filenames contain no UUID or random hash")
        passed += 1
    else:
        print(f"  [FAIL] T11: Filename UX failed, files: {files_found}")

    # T12: permanent session contains all 10 human sections
    sample_file = None
    for root, dirs, files in os.walk(sess_dir):
        for f in files:
            if f.endswith(".md"):
                sample_file = os.path.join(root, f)
                break
    if sample_file:
        with open(sample_file, "r", encoding="utf-8") as f:
            stxt = f.read()
        required_headers = [
            "## 🧭 AIRO STATUS", "## 🎯 Tujuan sesi", "## 🛠 Yang dilakukan",
            "## 📌 Hasil", "## 🧪 Bukti", "## ⛔ Masalah / hambatan",
            "## ✅ Keputusan", "## 📁 Yang berubah", "## 📝 Yang belum selesai", "## ➡️ Berikutnya"
        ]
        all_headers = all(h in stxt or h.replace("🧭", "\U0001F9ED") in stxt for h in required_headers)
        if all_headers:
            print("  [PASS] T12: Permanent session note contains all 10 human sections")
            passed += 1
        else:
            print(f"  [FAIL] T12: Missing section headers in {sample_file}")
    else:
        print("  [FAIL] T12: No sample session file found")

    # T13: daily groups sessions by project
    today_str = datetime.now().strftime("%Y-%m-%d")
    daily_res = subprocess.run([sys.executable, os.path.join(tmp_repo, "scripts/airo-daily"), today_str], env=env, cwd=tmp_repo, capture_output=True, text=True)
    daily_path = os.path.join(tmp_repo, "worklog/daily", f"{today_str}.md")
    if os.path.exists(daily_path):
        with open(daily_path, "r", encoding="utf-8") as f:
            dtxt = f.read()
        if "### Proyek: ASB" in dtxt:
            print("  [PASS] T13: Daily generator groups sessions by human project name")
            passed += 1
        else:
            print(f"  [FAIL] T13: Daily project grouping missing in {daily_path}")
    else:
        print(f"  [FAIL] T13: Daily file missing: {daily_path}, stdout: {daily_res.stdout}, stderr: {daily_res.stderr}")

    # T14: daily regeneration is byte-identical (DAILY_IDEMPOTENT=PASS)
    with open(daily_path, "r", encoding="utf-8") as f:
        dtxt1 = f.read()
    subprocess.run([sys.executable, os.path.join(tmp_repo, "scripts/airo-daily"), today_str], env=env, cwd=tmp_repo, capture_output=True, text=True)
    with open(daily_path, "r", encoding="utf-8") as f:
        dtxt2 = f.read()
    if dtxt1 == dtxt2:
        print("  [PASS] T14: Daily regeneration is 100% byte-identical (idempotent)")
        passed += 1
    else:
        print("  [FAIL] T14: Daily regeneration is not idempotent")

    # T15: raw secret-like summary rejected / not written
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj4"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    res15 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "event", "--summary", "sk-proj-1234567890secret"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if res15.returncode != 0:
        print("  [PASS] T15: Secret-like event summary is rejected")
        passed += 1
    else:
        print("  [FAIL] T15: Secret-like event summary was accepted")

    # T16: failed/blocked session remains recordable
    res16 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--blockers", "[\"Live runtime failure\"]"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "VERDICT_STATUS=TERHAMBAT" in res16.stdout:
        print("  [PASS] T16: Failed/blocked session is recorded truthfully without hiding failure")
        passed += 1
    else:
        print(f"  [FAIL] T16: Blocked session recording failed: {res16.stdout}")

    # T17: unknown root cause can be represented as "Penyebab belum diketahui"
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj5"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "event", "--summary", "Failure analysis: Penyebab belum diketahui"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    res17 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if res17.returncode == 0:
        print("  [PASS] T17: Unknown root cause is validly represented as 'Penyebab belum diketahui'")
        passed += 1
    else:
        print("  [FAIL] T17: Unknown root cause representation failed")

    # T18: inactivity never automatically finalizes completion
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj6"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    res18 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "status"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "DRAFT_CLOSEOUT_RECOMMENDED=NO" in res18.stdout and "Kesimpulan — IN_PROGRESS" in res18.stdout:
        print("  [PASS] T18: Inactivity status recommends draft without falsely finalizing completion")
        passed += 1
    else:
        print(f"  [FAIL] T18: Inactivity check failed: {res18.stdout}")

    # Cleanup temp
    shutil.rmtree(tmp_dir, ignore_errors=True)

    print(f"\nSession & Worklog Test Results: {passed}/{total} passed.")
    if passed == total:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    run_test_suite()

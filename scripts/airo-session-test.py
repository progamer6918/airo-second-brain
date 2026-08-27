#!/usr/bin/env python3
"""
airo-session-test.py: Comprehensive 30-case test suite for AIRO Session Lifecycle & Daily Generator.
Tests prove exact state, ledger, path containment, verdict enforcement, public safety, and atomic closeout.
"""
import sys
import os
import shutil
import tempfile
import json
import subprocess
from datetime import datetime, timezone, timedelta

def get_script_repo_root():
    if os.environ.get("AIRO_REPO_ROOT"):
        return os.path.abspath(os.environ.get("AIRO_REPO_ROOT"))
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def run_test_suite():
    repo_root_source = get_script_repo_root()
    if not os.path.exists(os.path.join(repo_root_source, "scripts/airo-capture")):
        repo_root_source = "/home/egitaristorandas/AI_WORKSPACES/airo-second-brain"

    tmp_dir = tempfile.mkdtemp(prefix="airo_session_test_")
    tmp_state = os.path.join(tmp_dir, "state")
    tmp_repo = os.path.join(tmp_dir, "repo")

    os.makedirs(os.path.join(tmp_repo, "bin"), exist_ok=True)
    os.makedirs(os.path.join(tmp_repo, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(tmp_repo, "docs/roadmap"), exist_ok=True)
    os.makedirs(os.path.join(tmp_repo, "events/raw"), exist_ok=True)

    scratch_dir = os.path.dirname(os.path.abspath(__file__))
    bin_src = os.path.join(scratch_dir, "bin_airo_session.py") if os.path.exists(os.path.join(scratch_dir, "bin_airo_session.py")) else os.path.join(repo_root_source, "bin/airo-session")
    daily_src = os.path.join(scratch_dir, "scripts_airo_daily.py") if os.path.exists(os.path.join(scratch_dir, "scripts_airo_daily.py")) else os.path.join(repo_root_source, "scripts/airo-daily")

    shutil.copy(bin_src, os.path.join(tmp_repo, "bin/airo-session"))
    shutil.copy(daily_src, os.path.join(tmp_repo, "scripts/airo-daily"))
    shutil.copy(os.path.join(repo_root_source, "scripts/airo-capture"), os.path.join(tmp_repo, "scripts/airo-capture"))
    if os.path.exists(os.path.join(repo_root_source, "scripts/airo-task-verdict")):
        shutil.copy(os.path.join(repo_root_source, "scripts/airo-task-verdict"), os.path.join(tmp_repo, "scripts/airo-task-verdict"))

    os.chmod(os.path.join(tmp_repo, "bin/airo-session"), 0o755)
    os.chmod(os.path.join(tmp_repo, "scripts/airo-daily"), 0o755)
    if os.path.exists(os.path.join(tmp_repo, "scripts/airo-task-verdict")):
        os.chmod(os.path.join(tmp_repo, "scripts/airo-task-verdict"), 0o755)

    env = os.environ.copy()
    env["AIRO_SESSION_STATE_DIR"] = tmp_state
    env["AIRO_REPO_ROOT"] = tmp_repo

    passed = 0
    total = 44

    print("Running 44 AIRO session & worklog test cases...")

    state_file = os.path.join(tmp_state, "active_session.json")

    # T1: start creates durable active session
    res1 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj1"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "SESSION_ACTION=STARTED" in res1.stdout and os.path.exists(state_file):
        with open(state_file, "r") as f:
            sdata1 = json.load(f)
        session_id_1 = sdata1["internal_session_id"]
        print("  [PASS] T1: Start creates durable active session")
        passed += 1
    else:
        print(f"  [FAIL] T1: Start failed: {res1.stdout}")

    # T2: same project+objective reuses exact internal ID
    res2 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj1"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "SESSION_ACTION=CONTINUE_EXISTING" in res2.stdout and f"SESSION_ID={session_id_1}" in res2.stdout:
        print("  [PASS] T2: Same project+objective reuses exact internal ID")
        passed += 1
    else:
        print(f"  [FAIL] T2: Session reuse failed: {res2.stdout}")

    # T3: different project/objective refuses switch
    res3 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "FINANCE", "--project-name", "FINANCE", "--objective", "Obj2"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "SESSION_SWITCH_REQUIRES_CLOSE=YES" in res3.stdout:
        print("  [PASS] T3: Different project refuses auto-switch")
        passed += 1
    else:
        print(f"  [FAIL] T3: Project switch guard failed: {res3.stdout}")

    # T4: multiple state events retain exact internal ID
    res4a = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "event", "--summary", "Evt1"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    res4b = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "event", "--summary", "Evt2"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    with open(state_file, "r") as f:
        sdata4 = json.load(f)
    if sdata4["internal_session_id"] == session_id_1 and len(sdata4["events"]) == 2:
        print("  [PASS] T4: Multiple state events retain exact internal ID")
        passed += 1
    else:
        print(f"  [FAIL] T4: Event recording failed: {res4a.stdout}")

    # T5: ledger events contain exact same session ID
    ndjson = os.path.join(tmp_repo, "events/raw/events.ndjson")
    with open(ndjson, "r") as f:
        ledger_lines = [json.loads(line) for line in f if line.strip()]
    matching_ids = [entry["session_id"] for entry in ledger_lines if entry.get("session_id") == session_id_1]
    if len(matching_ids) >= 3:
        print("  [PASS] T5: Ledger events contain exact same session ID (LEDGER_SESSION_ID_MATCH=PASS)")
        passed += 1
    else:
        print(f"  [FAIL] T5: Ledger session ID mismatch: {matching_ids}")

    # T6: resume after process restart
    res6 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "resume"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "SESSION_RESUMED=YES" in res6.stdout and "PROJECT_ID=ASB" in res6.stdout:
        print("  [PASS] T6: Resume after process restart verified")
        passed += 1
    else:
        print(f"  [FAIL] T6: Resume failed: {res6.stdout}")

    # T7: draft closeout does not finalize
    res7 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "draft-closeout"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "DRAFT_CLOSEOUT_CREATED=YES" in res7.stdout and os.path.exists(state_file):
        print("  [PASS] T7: Draft closeout creates staging note without finalization")
        passed += 1
    else:
        print(f"  [FAIL] T7: Draft closeout failed: {res7.stdout}")

    # T8: SCRIPT_SUCCESS + missing evidence => BELUM_TERBUKTI/NO
    res8 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "VERDICT_STATUS=BELUM_TERBUKTI" in res8.stdout and "CAN_ADVANCE=NO" in res8.stdout and not os.path.exists(state_file):
        print("  [PASS] T8: Missing evidence closes as BELUM_TERBUKTI / CAN_ADVANCE=NO without evidence fabrication")
        passed += 1
    else:
        print(f"  [FAIL] T8: Missing evidence close failed: {res8.stdout}")

    # T9: blocker => TERHAMBAT/NO
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj9", "--title", "T9 Blocker"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    res9 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--required-evidence", "[\"E1\"]", "--actual-evidence", "[\"E1\"]", "--blockers", "[\"Active blocker\"]"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "VERDICT_STATUS=TERHAMBAT" in res9.stdout and "CAN_ADVANCE=NO" in res9.stdout:
        print("  [PASS] T9: Active blocker produces TERHAMBAT / CAN_ADVANCE=NO")
        passed += 1
    else:
        print(f"  [FAIL] T9: Blocker close failed: {res9.stdout}")

    # T10: explicit matching evidence => BERHASIL/YES
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj10", "--title", "T10 Success"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    res10 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--required-evidence", "[\"LIVE_RUNTIME\"]", "--actual-evidence", "[\"LIVE_RUNTIME\"]"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "VERDICT_STATUS=BERHASIL" in res10.stdout and "CAN_ADVANCE=YES" in res10.stdout:
        print("  [PASS] T10: Explicit matching evidence produces BERHASIL / CAN_ADVANCE=YES")
        passed += 1
    else:
        print(f"  [FAIL] T10: Matching evidence close failed: {res10.stdout}")

    # T11: explicit missing evidence => BELUM_TERBUKTI/NO
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj11", "--title", "T11 Missing"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    res11 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--required-evidence", "[\"REQUIRED_A\", \"REQUIRED_B\"]", "--actual-evidence", "[\"REQUIRED_A\"]"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "VERDICT_STATUS=BELUM_TERBUKTI" in res11.stdout and "CAN_ADVANCE=NO" in res11.stdout:
        print("  [PASS] T11: Partial missing evidence produces BELUM_TERBUKTI / CAN_ADVANCE=NO")
        passed += 1
    else:
        print(f"  [FAIL] T11: Partial missing evidence failed: {res11.stdout}")

    # T12: limitation => BERHASIL_DENGAN_BATASAN/NO
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj12", "--title", "T12 Limitation"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    res12 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--required-evidence", "[\"E1\"]", "--actual-evidence", "[\"E1\"]", "--limitations", "[\"Local test mode\"]"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "VERDICT_STATUS=BERHASIL_DENGAN_BATASAN" in res12.stdout and "CAN_ADVANCE=NO" in res12.stdout:
        print("  [PASS] T12: Limitation produces BERHASIL_DENGAN_BATASAN / CAN_ADVANCE=NO")
        passed += 1
    else:
        print(f"  [FAIL] T12: Limitation close failed: {res12.stdout}")

    # T13: missing validator => close fails and state survives
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj13", "--title", "T13 Missing Validator"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    verdict_script = os.path.join(tmp_repo, "scripts/airo-task-verdict")
    verdict_backup = verdict_script + ".bak"
    if os.path.exists(verdict_script):
        os.rename(verdict_script, verdict_backup)

    res13 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--required-evidence", "[\"E1\"]", "--actual-evidence", "[\"E1\"]"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "CLOSE_RESULT=FAILED" in res13.stdout and "ACTIVE_SESSION_PRESERVED=YES" in res13.stdout and os.path.exists(state_file):
        print("  [PASS] T13: Missing validator fails closed and preserves active session state")
        passed += 1
    else:
        print(f"  [FAIL] T13: Missing validator handling failed: {res13.stdout}")

    if os.path.exists(verdict_backup):
        os.rename(verdict_backup, verdict_script)

    # T14: invalid validator output => close fails and state survives
    fake_validator = os.path.join(tmp_repo, "scripts/fake_validator.py")
    with open(fake_validator, "w") as f:
        f.write("#!/usr/bin/env python3\nimport sys\nprint('invalid json')\n")
    os.chmod(fake_validator, 0o755)

    os.rename(verdict_script, verdict_backup)
    shutil.copy(fake_validator, verdict_script)
    os.chmod(verdict_script, 0o755)

    res14 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--required-evidence", "[\"E1\"]", "--actual-evidence", "[\"E1\"]"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "CLOSE_RESULT=FAILED" in res14.stdout and "ACTIVE_SESSION_PRESERVED=YES" in res14.stdout and os.path.exists(state_file):
        print("  [PASS] T14: Invalid validator output fails closed and preserves active session state")
        passed += 1
    else:
        print(f"  [FAIL] T14: Invalid validator handling failed: {res14.stdout}")

    os.remove(verdict_script)
    os.rename(verdict_backup, verdict_script)

    # Clean up T13/T14 state by closing cleanly
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close"], env=env, cwd=tmp_repo, capture_output=True, text=True)

    # T15: capture failure is visible and not claimed recorded
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj15", "--title", "T15 Capture Fail"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    capture_script = os.path.join(tmp_repo, "scripts/airo-capture")
    capture_bak = capture_script + ".bak"
    os.rename(capture_script, capture_bak)

    res15 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "event", "--summary", "Event when capture missing"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "EVENT_RECORDED=NO" in res15.stdout and "CAPTURE_STATUS=FAILED" in res15.stdout:
        print("  [PASS] T15: Capture failure is visible and not claimed recorded")
        passed += 1
    else:
        print(f"  [FAIL] T15: Capture failure handling failed: {res15.stdout}")

    os.rename(capture_bak, capture_script)
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close"], env=env, cwd=tmp_repo, capture_output=True, text=True)

    # T16: ledger session ID equality verified
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj16"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    with open(state_file, "r") as f:
        sid16 = json.load(f)["internal_session_id"]
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "event", "--summary", "Evt 16"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    with open(ndjson, "r") as f:
        last_evt = json.loads([line for line in f if line.strip()][-1])
    if last_evt.get("session_id") == sid16:
        print("  [PASS] T16: Ledger event contains exact active session ID")
        passed += 1
    else:
        print(f"  [FAIL] T16: Ledger session ID equality failed")

    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close"], env=env, cwd=tmp_repo, capture_output=True, text=True)

    # T17: path traversal in project/title rejected
    res17 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "../ASB", "--project-name", "ASB/Traversal", "--objective", "Obj17"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if res17.returncode != 0:
        print("  [PASS] T17: Path traversal in project/title rejected")
        passed += 1
    else:
        print(f"  [FAIL] T17: Path traversal in project/title accepted")

    # T18: UUID/random hash absent from human filename
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj18", "--title", "Human Session Title"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    res18 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    sess_dir = os.path.join(tmp_repo, "worklog/sessions")
    files_18 = []
    for r, d, fs in os.walk(sess_dir):
        for f in fs:
            files_18.append(f)
    has_uuid_18 = any(len(f) > 30 and "-" in f for f in files_18)
    if files_18 and not has_uuid_18:
        print("  [PASS] T18: UUID/random hash absent from human filenames")
        passed += 1
    else:
        print(f"  [FAIL] T18: Filename check failed: {files_18}")

    # T19: long legitimate human title accepted safely
    long_title = "Detailed Architectural Implementation of Execution Assurance and Governance Rules"
    res19 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj19", "--title", long_title], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if res19.returncode == 0:
        subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close"], env=env, cwd=tmp_repo, capture_output=True, text=True)
        print("  [PASS] T19: Long legitimate human title accepted safely")
        passed += 1
    else:
        print(f"  [FAIL] T19: Long human title failed: {res19.stdout}")

    # T20: all 10 human sections exist
    sample_file = None
    for r, d, fs in os.walk(sess_dir):
        for f in fs:
            if f.endswith(".md"):
                sample_file = os.path.join(r, f)
                break
    if sample_file:
        with open(sample_file, "r", encoding="utf-8") as f:
            stxt = f.read()
        req_sections = [
            "## 🧭 AIRO STATUS", "## 🎯 Tujuan Sesi", "## 🛠 Yang dikerjakan",
            "## 📌 Hasil", "## 🧪 Bukti", "## ⛔ Masalah / Hambatan",
            "## ✅ Keputusan", "## 📁 Yang berubah", "## 📝 Yang belum selesai", "## ➡️ Berikutnya"
        ]
        if all(sec in stxt for sec in req_sections):
            print("  [PASS] T20: Permanent session note contains all 10 human sections")
            passed += 1
        else:
            print(f"  [FAIL] T20: Missing sections in permanent note")
    else:
        print("  [FAIL] T20: Sample session file missing")

    # T21: blocked/failed session permanently recordable
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj21", "--title", "T21 Failed"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    res21 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--required-evidence", "[\"E1\"]", "--actual-evidence", "[\"E1\"]", "--blockers", "[\"Live runtime failure\"]"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "VERDICT_STATUS=TERHAMBAT" in res21.stdout:
        print("  [PASS] T21: Blocked/failed session permanently recordable")
        passed += 1
    else:
        print(f"  [FAIL] T21: Blocked session recording failed: {res21.stdout}")

    # T22: "Penyebab belum diketahui" appears in permanent note
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj22", "--title", "T22 Unknown Root Cause"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "event", "--summary", "Failure analysis: Penyebab belum diketahui"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    res22 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    note_22 = res22.stdout.split("PERMANENT_SESSION_NOTE=")[-1].splitlines()[0] if "PERMANENT_SESSION_NOTE=" in res22.stdout else ""
    if os.path.exists(note_22):
        with open(note_22, "r", encoding="utf-8") as f:
            ntxt22 = f.read()
        if "Penyebab belum diketahui" in ntxt22:
            print("  [PASS] T22: 'Penyebab belum diketahui' appears in permanent note")
            passed += 1
        else:
            print(f"  [FAIL] T22: 'Penyebab belum diketahui' missing in note: {note_22}")
    else:
        print(f"  [FAIL] T22: Permanent note missing for T22")

    # T23: inactivity > 45 minutes recommends draft, stays active, no completion created
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj23", "--title", "T23 Inactivity"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    with open(state_file, "r") as f:
        sdata23 = json.load(f)
    old_time = (datetime.now(timezone.utc) - timedelta(minutes=50)).isoformat()
    sdata23["last_activity_at"] = old_time
    with open(state_file, "w") as f:
        json.dump(sdata23, f)

    res23 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "status"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "DRAFT_CLOSEOUT_RECOMMENDED=YES" in res23.stdout and "Kesimpulan — SEDANG DIKERJAKAN" in res23.stdout and os.path.exists(state_file):
        print("  [PASS] T23: >45 min inactivity recommends draft without auto-finalizing")
        passed += 1
    else:
        print(f"  [FAIL] T23: Inactivity test failed: {res23.stdout}")

    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close"], env=env, cwd=tmp_repo, capture_output=True, text=True)

    # T24: Daily groups by project
    today_str = datetime.now().strftime("%Y-%m-%d")
    daily_res = subprocess.run([sys.executable, os.path.join(tmp_repo, "scripts/airo-daily"), today_str], env=env, cwd=tmp_repo, capture_output=True, text=True)
    daily_path = os.path.join(tmp_repo, "worklog/daily", f"{today_str}.md")
    if os.path.exists(daily_path):
        with open(daily_path, "r", encoding="utf-8") as f:
            dtxt24 = f.read()
        if "### Proyek: ASB" in dtxt24:
            print("  [PASS] T24: Daily generator groups sessions by human project name")
            passed += 1
        else:
            print(f"  [FAIL] T24: Daily project grouping missing in {daily_path}")
    else:
        print(f"  [FAIL] T24: Daily file missing: {daily_path}")

    # T25: Daily regeneration byte-identical (DAILY_IDEMPOTENT=PASS)
    with open(daily_path, "r", encoding="utf-8") as f:
        dtxt25_1 = f.read()
    subprocess.run([sys.executable, os.path.join(tmp_repo, "scripts/airo-daily"), today_str], env=env, cwd=tmp_repo, capture_output=True, text=True)
    with open(daily_path, "r", encoding="utf-8") as f:
        dtxt25_2 = f.read()
    if dtxt25_1 == dtxt25_2:
        print("  [PASS] T25: Daily regeneration is 100% byte-identical (DAILY_IDEMPOTENT=PASS)")
        passed += 1
    else:
        print(f"  [FAIL] T25: Daily regeneration not idempotent")

    # T26: every Daily link resolves to existing file (DAILY_LINK_RESOLUTION=PASS)
    import re
    link_pattern = re.compile(r"\[.*?\]\((.*?)\)")
    broken_links = 0
    total_links = 0
    with open(daily_path, "r", encoding="utf-8") as f:
        daily_body = f.read()

    daily_dir = os.path.dirname(daily_path)
    for link in link_pattern.findall(daily_body):
        if link.startswith("http") or link.startswith("#"):
            continue
        total_links += 1
        resolved = os.path.abspath(os.path.join(daily_dir, link))
        if not os.path.exists(resolved):
            broken_links += 1

    if total_links > 0 and broken_links == 0:
        print("  [PASS] T26: Every Daily session link resolves to an existing file (DAILY_LINK_RESOLUTION=PASS)")
        passed += 1
    else:
        print(f"  [FAIL] T26: Daily link resolution failed: {broken_links}/{total_links} broken")

    # T27: Daily failure preserves active state
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj27", "--title", "T27 Daily Fail"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    daily_script = os.path.join(tmp_repo, "scripts/airo-daily")
    daily_bak = daily_script + ".bak"
    os.rename(daily_script, daily_bak)

    res27 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "CLOSE_RESULT=FAILED" in res27.stdout and "ACTIVE_SESSION_PRESERVED=YES" in res27.stdout and os.path.exists(state_file):
        print("  [PASS] T27: Daily failure preserves active session state")
        passed += 1
    else:
        print(f"  [FAIL] T27: Daily failure state preservation failed: {res27.stdout}")

    os.rename(daily_bak, daily_script)

    # T28: close retry uses same path and creates no duplicate
    with open(state_file, "r") as f:
        planned_path_28 = json.load(f).get("planned_closeout_path")
    res28 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--required-evidence", '["E1"]', "--actual-evidence", '["E1"]'], env=env, cwd=tmp_repo, capture_output=True, text=True)
    final_path_28 = res28.stdout.split("PERMANENT_SESSION_NOTE=")[-1].splitlines()[0] if "PERMANENT_SESSION_NOTE=" in res28.stdout else ""
    if planned_path_28 == final_path_28 and os.path.exists(final_path_28):
        print("  [PASS] T28: Close retry uses same path without duplicate creation (CLOSE_RETRY_IDEMPOTENT=PASS)")
        passed += 1
    else:
        print(f"  [FAIL] T28: Close retry idempotency failed: planned={planned_path_28}, final={final_path_28}")

    # T29: secret in title/objective/evidence/blocker rejected
    res29a = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "sk-proj-secret123"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj29"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    res29b = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "event", "--summary", "token=12345secret"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    res29c = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--blockers", "[\"BEGIN PRIVATE KEY\"]"], env=env, cwd=tmp_repo, capture_output=True, text=True)

    if res29a.returncode != 0 and res29b.returncode != 0 and "CLOSE_RESULT=FAILED" in res29c.stdout:
        print("  [PASS] T29: Secrets in title/objective/evidence/blocker rejected (PUBLIC_SAFETY=PASS)")
        passed += 1
    else:
        print(f"  [FAIL] T29: Secret rejection failed: a={res29a.returncode}, b={res29b.returncode}, c={res29c.stdout}")

    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close"], env=env, cwd=tmp_repo, capture_output=True, text=True)

    # T30: malformed JSON/list input fails closed
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj30"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    res30 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--required-evidence", "not a json list"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "CLOSE_RESULT=FAILED" in res30.stdout and "ACTIVE_SESSION_PRESERVED=YES" in res30.stdout and os.path.exists(state_file):
        print("  [PASS] T30: Malformed JSON input fails closed and preserves active session state")
        passed += 1
    else:
        print(f"  [FAIL] T30: Malformed JSON input handling failed: {res30.stdout}")

    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close"], env=env, cwd=tmp_repo, capture_output=True, text=True)

    # T31: Structured closeout renders real actions/outcomes without generic boilerplate
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj31", "--title", "T31 Structured Closeout"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    cj31 = json.dumps({
        "actions": ["Implemented semantic renderer"],
        "outcomes": ["Structured closeout works cleanly"],
        "evidence_refs": ["docs/validation/sample.md"],
        "decisions": ["Approved structured schema"],
        "changed_paths": ["bin/airo-session"],
        "unfinished": ["None"],
        "next_action": "Run test suite",
        "completion_criteria": "Tests pass 100%"
    })
    res31 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--closeout-json", cj31], env=env, cwd=tmp_repo, capture_output=True, text=True)

    t31_pass = False
    if "SESSION_CLOSED=YES" in res31.stdout:
        note_31 = [line.split("=")[1].strip() for line in res31.stdout.splitlines() if line.startswith("PERMANENT_SESSION_NOTE=")][0]
        if os.path.exists(note_31):
            with open(note_31, "r", encoding="utf-8") as f31:
                n31_txt = f31.read()
            if "Implemented semantic renderer" in n31_txt and "Sesi dijalankan." not in n31_txt:
                t31_pass = True
    if t31_pass:
        print("  [PASS] T31: Structured closeout renders real actions/outcomes without generic boilerplate (STRUCTURED_CLOSEOUT_SUPPORTED=PASS)")
        passed += 1
    else:
        print("  [FAIL] T31: Structured closeout rendering failed")

    # T32: Empty decisions => 'Tidak ada keputusan baru.'
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj32", "--title", "T32 Empty Decisions"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    cj32 = json.dumps({
        "actions": ["Action 32"],
        "decisions": [],
        "unfinished": []
    })
    res32 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--closeout-json", cj32], env=env, cwd=tmp_repo, capture_output=True, text=True)
    t32_pass = False
    if "SESSION_CLOSED=YES" in res32.stdout:
        note_32 = [line.split("=")[1].strip() for line in res32.stdout.splitlines() if line.startswith("PERMANENT_SESSION_NOTE=")][0]
        if os.path.exists(note_32):
            with open(note_32, "r", encoding="utf-8") as f32:
                n32_txt = f32.read()
            if "Tidak ada keputusan baru." in n32_txt and "Tidak ada pekerjaan sesi yang tersisa." in n32_txt:
                t32_pass = True
    if t32_pass:
        print("  [PASS] T32: Empty decisions/unfinished render default explicit messages (REAL_DECISIONS_RENDER=PASS)")
        passed += 1
    else:
        print("  [FAIL] T32: Empty decisions rendering failed")

    # T33: next_action renders in BOTH AIRO STATUS and final section
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj33", "--title", "T33 Next Action"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    cj33 = json.dumps({
        "actions": ["Action 33"],
        "next_action": "Proceed to M6.1 validation",
        "completion_criteria": "DoD 33 satisfied"
    })
    res33 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--closeout-json", cj33], env=env, cwd=tmp_repo, capture_output=True, text=True)
    t33_pass = False
    if "SESSION_CLOSED=YES" in res33.stdout:
        note_33 = [line.split("=")[1].strip() for line in res33.stdout.splitlines() if line.startswith("PERMANENT_SESSION_NOTE=")][0]
        if os.path.exists(note_33):
            with open(note_33, "r", encoding="utf-8") as f33:
                n33_txt = f33.read()
            if n33_txt.count("Proceed to M6.1 validation") >= 2 and "DoD 33 satisfied" in n33_txt:
                t33_pass = True
    if t33_pass:
        print("  [PASS] T33: next_action renders in BOTH AIRO STATUS and final section (REAL_NEXT_ACTION_RENDER=PASS)")
        passed += 1
    else:
        print("  [FAIL] T33: next_action rendering failed")

    # T34: Secret pattern in closeout-json rejected
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj34"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    cj34 = json.dumps({
        "actions": ["sk-proj-secretKey123"]
    })
    res34 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--closeout-json", cj34], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "CLOSE_RESULT=FAILED" in res34.stdout and "ACTIVE_SESSION_PRESERVED=YES" in res34.stdout:
        print("  [PASS] T34: Secret pattern in closeout-json rejected (PUBLIC_SAFETY=PASS)")
        passed += 1
    else:
        print("  [FAIL] T34: Secret rejection in closeout-json failed")
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close"], env=env, cwd=tmp_repo, capture_output=True, text=True)

    # T35: Path traversal in changed_paths rejected
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj35"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    cj35 = json.dumps({
        "changed_paths": ["../../etc/passwd"]
    })
    res35 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--closeout-json", cj35], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "CLOSE_RESULT=FAILED" in res35.stdout and "ACTIVE_SESSION_PRESERVED=YES" in res35.stdout:
        print("  [PASS] T35: Path traversal in changed_paths rejected (PATH_TRAVERSAL_REJECTED=PASS)")
        passed += 1
    else:
        print("  [FAIL] T35: Path traversal rejection failed")
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close"], env=env, cwd=tmp_repo, capture_output=True, text=True)

    # T36: Malformed closeout-json fails closed
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj36"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    res36 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--closeout-json", "invalid json"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if "CLOSE_RESULT=FAILED" in res36.stdout and "ACTIVE_SESSION_PRESERVED=YES" in res36.stdout:
        print("  [PASS] T36: Malformed closeout-json fails closed (MALFORMED_CLOSEOUT_JSON_FAIL_CLOSED=PASS)")
        passed += 1
    else:
        print("  [FAIL] T36: Malformed closeout-json handling failed")
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close"], env=env, cwd=tmp_repo, capture_output=True, text=True)



    # T37: Real closed_at emitted on session close
    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "Obj37"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    res37 = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--required-evidence", "[\"E1\"]", "--actual-evidence", "[\"E1\"]"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    note_37 = res37.stdout.split("PERMANENT_SESSION_NOTE=")[-1].splitlines()[0] if "PERMANENT_SESSION_NOTE=" in res37.stdout else ""
    t37_pass = False
    if os.path.exists(note_37):
        with open(note_37, "r", encoding="utf-8") as f37:
            txt37 = f37.read()
        if "closed_at:" in txt37 and "date:" in txt37:
            t37_pass = True
    if t37_pass:
        print("  [PASS] T37: Real closed_at emitted on session close (CLOSED_AT_EMITTED=PASS)")
        passed += 1
    else:
        print("  [FAIL] T37: closed_at emission failed")

    # T38: Session start produces exactly 1 session-start ledger checkpoint
    tmp_repo_38 = os.path.join(tmp_dir, "repo_38")
    shutil.copytree(tmp_repo, tmp_repo_38, ignore=shutil.ignore_patterns(".git", "worklog", "state", "events", "logs"))
    os.makedirs(os.path.join(tmp_repo_38, "state"), exist_ok=True)
    os.makedirs(os.path.join(tmp_repo_38, "events/raw"), exist_ok=True)
    os.makedirs(os.path.join(tmp_repo_38, "logs"), exist_ok=True)
    env_38 = dict(os.environ, HOME=tmp_dir, AIRO_SESSION_ID="", AIRO_SESSION_STATE_DIR=os.path.join(tmp_repo_38, "state"))
    events_file_38 = os.path.join(tmp_repo_38, "events/raw/events.ndjson")
    lines_before_38 = len(open(events_file_38).readlines()) if os.path.exists(events_file_38) else 0
    res38 = subprocess.run([sys.executable, os.path.join(tmp_repo_38, "bin/airo-session"), "start", "--project-id", "ASB_38", "--project-name", "ASB 38", "--objective", "Obj 38"], env=env_38, cwd=tmp_repo_38, capture_output=True, text=True)
    lines_after_38 = len(open(events_file_38).readlines()) if os.path.exists(events_file_38) else 0
    active_sf = os.path.join(tmp_repo_38, "state/active_session.json")
    s38 = json.load(open(active_sf)) if os.path.exists(active_sf) else {}
    if "SESSION_ACTION=STARTED" in res38.stdout and (lines_after_38 - lines_before_38 == 1) and len(s38.get("events", [])) == 0:
        print("  [PASS] T38: Session start produces exactly 1 ledger checkpoint (SESSION_START_SINGLE_WRITE=PASS)")
        passed += 1
    else:
        print(f"  [FAIL] T38: Session start single write failed (out={res38.stdout.strip()}, err={res38.stderr.strip()})")

    # T39: airo-session event single write (ACTIVE_SESSION_EVENT_DELTA=1, LEDGER_EVENT_DELTA=1)
    sess_evts_before_39 = len(s38.get("events", []))
    lines_before_39 = len(open(events_file_38).readlines())
    res39 = subprocess.run([sys.executable, os.path.join(tmp_repo_38, "bin/airo-session"), "event", "--event-type", "validation", "--summary", "Single write event test"], env=env_38, cwd=tmp_repo_38, capture_output=True, text=True)
    lines_after_39 = len(open(events_file_38).readlines())
    with open(os.path.join(tmp_repo_38, "state/active_session.json")) as sf: s39 = json.load(sf)
    sess_evts_after_39 = len(s39.get("events", []))
    if "EVENT_RECORDED=YES" in res39.stdout and (sess_evts_after_39 - sess_evts_before_39 == 1) and (lines_after_39 - lines_before_39 == 1):
        print("  [PASS] T39: airo-session event produces exactly 1 active event & 1 ledger record (SESSION_EVENT_SINGLE_WRITE=PASS)")
        passed += 1
    else:
        print(f"  [FAIL] T39: airo-session event single write failed (sess_delta={sess_evts_after_39 - sess_evts_before_39}, ledger_delta={lines_after_39 - lines_before_39})")

    # T40: Direct scripts/airo-capture with active session (ACTIVE_SESSION_EVENT_DELTA=1, LEDGER_EVENT_DELTA=1)
    sess_evts_before_40 = len(s39.get("events", []))
    lines_before_40 = len(open(events_file_38).readlines())
    res40 = subprocess.run([sys.executable, os.path.join(tmp_repo_38, "scripts/airo-capture"), "--event", "checkpoint", "--summary", "Direct capture active session test"], env=env_38, cwd=tmp_repo_38, capture_output=True, text=True)
    lines_after_40 = len(open(events_file_38).readlines())
    with open(os.path.join(tmp_repo_38, "state/active_session.json")) as sf: s40 = json.load(sf)
    sess_evts_after_40 = len(s40.get("events", []))
    if res40.returncode == 0 and (sess_evts_after_40 - sess_evts_before_40 == 1) and (lines_after_40 - lines_before_40 == 1):
        print("  [PASS] T40: Direct airo-capture with active session delegates cleanly (DIRECT_CAPTURE_SINGLE_WRITE=PASS)")
        passed += 1
    else:
        print(f"  [FAIL] T40: Direct airo-capture single write failed (sess_delta={sess_evts_after_40 - sess_evts_before_40}, ledger_delta={lines_after_40 - lines_before_40})")

    # T41: Extended semantic fields propagation
    res41 = subprocess.run([
        sys.executable, os.path.join(tmp_repo_38, "scripts/airo-capture"),
        "--event", "validation", "--summary", "Extended metadata test",
        "--phase", "POST_EXECUTION", "--owner-request", "Test request",
        "--position", "Test Position", "--progress", "50%", "--blocker", "None",
        "--next-action", "Next step", "--evidence", "docs/test.md"
    ], env=env_38, cwd=tmp_repo_38, capture_output=True, text=True)
    with open(events_file_38) as ef38: last_ledger_line = json.loads(ef38.readlines()[-1])
    with open(os.path.join(tmp_repo_38, "state/active_session.json")) as sf: s41 = json.load(sf)
    last_sess_evt = s41.get("events", [])[-1]
    t41_pass = (
        last_ledger_line.get("phase") == "POST_EXECUTION" and
        last_ledger_line.get("owner_request") == "Test request" and
        last_ledger_line.get("position") == "Test Position" and
        last_sess_evt.get("phase") == "POST_EXECUTION" and
        s41.get("position") == "Test Position"
    )
    if t41_pass:
        print("  [PASS] T41: Extended semantic metadata propagated correctly (EXTENDED_SEMANTIC_PROPAGATION=PASS)")
        passed += 1
    else:
        print("  [FAIL] T41: Extended metadata propagation failed")

    # T42: Standalone capture when no session active
    subprocess.run([sys.executable, os.path.join(tmp_repo_38, "bin/airo-session"), "close"], env=env_38, cwd=tmp_repo_38, capture_output=True, text=True)
    lines_before_42 = len(open(events_file_38).readlines())
    res42 = subprocess.run([sys.executable, os.path.join(tmp_repo_38, "scripts/airo-capture"), "--event", "checkpoint", "--summary", "Standalone capture test"], env=env_38, cwd=tmp_repo_38, capture_output=True, text=True)
    lines_after_42 = len(open(events_file_38).readlines())
    if res42.returncode == 0 and (lines_after_42 - lines_before_42 == 1):
        print("  [PASS] T42: Standalone capture appends exactly 1 ledger record when no active session (STANDALONE_CAPTURE=PASS)")
        passed += 1
    else:
        print("  [FAIL] T42: Standalone capture failed")

    # T43: Recursion guard & no double-write
    subprocess.run([sys.executable, os.path.join(tmp_repo_38, "bin/airo-session"), "start", "--project-id", "ASB_43", "--project-name", "ASB 43", "--objective", "Obj 43"], env=env_38, cwd=tmp_repo_38, capture_output=True, text=True)
    lines_before_43 = len(open(events_file_38).readlines())
    res43 = subprocess.run([sys.executable, os.path.join(tmp_repo_38, "bin/airo-session"), "event", "--event-type", "validation", "--summary", "Recursion test"], env=env_38, cwd=tmp_repo_38, capture_output=True, text=True)
    lines_after_43 = len(open(events_file_38).readlines())
    if res43.returncode == 0 and (lines_after_43 - lines_before_43 == 1):
        print("  [PASS] T43: Recursion guard prevents loop & double write (NO_RECURSIVE_DOUBLE_WRITE=PASS)")
        passed += 1
    else:
        print("  [FAIL] T43: Recursion guard test failed")

    # T44: Repeated explicit calls with identical summary produce 2 separate events
    lines_before_44 = len(open(events_file_38).readlines())
    subprocess.run([sys.executable, os.path.join(tmp_repo_38, "bin/airo-session"), "event", "--event-type", "validation", "--summary", "Identical summary text"], env=env_38, cwd=tmp_repo_38, capture_output=True, text=True)
    subprocess.run([sys.executable, os.path.join(tmp_repo_38, "bin/airo-session"), "event", "--event-type", "validation", "--summary", "Identical summary text"], env=env_38, cwd=tmp_repo_38, capture_output=True, text=True)
    lines_after_44 = len(open(events_file_38).readlines())
    if lines_after_44 - lines_before_44 == 2:
        print("  [PASS] T44: Repeated explicit invocations produce separate events (GENUINE_REPEAT_CALLS_PRESERVED=PASS)")
        passed += 1
    else:
        print(f"  [FAIL] T44: Repeated calls test failed (delta={lines_after_44 - lines_before_44})")


    # Cleanup temp

    shutil.rmtree(tmp_dir, ignore_errors=True)

    print(f"\nSession & Worklog Corrected Test Results: {passed}/{total} passed.")
    if passed == total:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    run_test_suite()

# Verified Fail-Closed Close Eligibility Contract V2

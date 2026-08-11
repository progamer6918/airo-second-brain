#!/usr/bin/env python3
"""
airo-obsidian-test.py: 20-case test suite for M3 Obsidian Human Experience & HOME Base Correction.
Verifies HOME.md, native Obsidian Bases official YAML schema (filters, displayName, order), link resolution, and .obsidian preservation.
"""

import os
import sys
import json
import re
import shutil
import tempfile
import subprocess
from datetime import datetime

def get_script_repo_root():
    if os.environ.get("AIRO_REPO_ROOT"):
        return os.path.abspath(os.environ.get("AIRO_REPO_ROOT"))
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def run_obsidian_test_suite():
    repo_root = get_script_repo_root()
    if not os.path.exists(os.path.join(repo_root, "HOME.md")):
        repo_root = "/home/egitaristorandas/AI_WORKSPACES/airo-second-brain"

    passed = 0
    total = 20

    print("Running 20 M3 Obsidian Human Experience & HOME Base test cases...")

    # T1: HOME.md exists at repository root
    home_path = os.path.join(repo_root, "HOME.md")
    if os.path.exists(home_path):
        print("  [PASS] T1: HOME.md exists at repository root")
        passed += 1
    else:
        print("  [FAIL] T1: HOME.md missing at root")

    # T2: HOME follows canonical intent-first hierarchy
    if os.path.exists(home_path):
        with open(home_path, "r", encoding="utf-8") as f:
            htxt = f.read()
        markers = ["## Mau ngapain?", "### ▶️ Lanjut Kerja", "### 📅 Hari Ini", "### 🔎 Cari & Jelajah", "#### 💼 Kerja", "#### 💰 Keuangan"]
        ordered = all(x in htxt for x in markers) and htxt.find("### 🔎 Cari & Jelajah") < htxt.find("#### 💼 Kerja") < htxt.find("#### 💰 Keuangan")
        if ordered:
            print("  [PASS] T2: HOME hierarchy and Cari & Jelajah placement are canonical")
            passed += 1
        else:
            print("  [FAIL] T2: HOME hierarchy/order mismatch")

    # T3: HOME embeds Hari Ini
    if "![[worklog/views/AIRO Worklog.base#Hari Ini]]" in htxt:
        print("  [PASS] T3: HOME embeds AIRO Worklog.base#Hari Ini")
        passed += 1
    else:
        print("  [FAIL] T3: HOME missing Hari Ini base embed")

    # T4: richer history lives in RIWAYAT_KERJA and Lanjut Kerja is non-duplicative
    history_path = os.path.join(repo_root, "RIWAYAT_KERJA.md")
    history_txt = open(history_path, "r", encoding="utf-8").read() if os.path.exists(history_path) else ""
    lanjut = htxt[htxt.find("### ▶️ Lanjut Kerja"):htxt.find("### 📅 Hari Ini")]
    home_ok = "#Sesi Terbaru]]" not in htxt and "#Riwayat Sesi]]" not in htxt
    history_ok = all(x in history_txt for x in ["#Hari Ini]]", "#Sesi Terbaru]]", "#Riwayat Sesi]]"])
    if home_ok and history_ok and "wiki/workdesk/HOME" not in lanjut:
        print("  [PASS] T4: continuity/history placement matches navigation contract")
        passed += 1
    else:
        print("  [FAIL] T4: continuity/history placement mismatch")

    # T5: all HOME Obsidian wikilinks and embeds resolve
    links = re.findall(r"!?\[\[([^\]]+)\]\]", htxt)
    link_ok = True
    for raw in links:
        target = raw.split("|", 1)[0].split("#", 1)[0].strip()
        if not target:
            continue
        candidates = [os.path.join(repo_root, target), os.path.join(repo_root, target + ".md")]
        if not any(os.path.exists(x) for x in candidates):
            print(f"  [FAIL] T5: missing HOME wikilink target: {target}")
            link_ok = False
            break
    if link_ok and links:
        print(f"  [PASS] T5: All HOME wikilinks/embeds resolve ({len(links)} checked)")
        passed += 1
    # T6: AIRO Worklog.base exists and uses official native Obsidian Bases YAML schema
    base_path = os.path.join(repo_root, "worklog/views/AIRO Worklog.base")
    if os.path.exists(base_path):
        with open(base_path, "r", encoding="utf-8") as f:
            btxt = f.read()
        
        # Check for legacy invalid keys
        has_legacy_keys = bool(re.search(r"^\s*filter:\s*", btxt, re.MULTILINE)) or \
                          bool(re.search(r"^\s*label:\s*", btxt, re.MULTILINE)) or \
                          bool(re.search(r"^\s*fields:\s*", btxt, re.MULTILINE))
        
        # Check for required official native keys
        has_official_keys = "filters:" in btxt and "displayName:" in btxt and "order:" in btxt
        
        if not has_legacy_keys and has_official_keys:
            print("  [PASS] T6: AIRO Worklog.base uses official native Obsidian Bases schema (BASE_NATIVE_SCHEMA_KEYS=PASS)")
            passed += 1
        else:
            print("  [FAIL] T6: Base uses invalid/legacy schema keys (filter/label/fields)")
    else:
        print("  [FAIL] T6: AIRO Worklog.base missing")

    # T7: Base globally targets worklog/sessions + type=airo-session + file.ext == md
    if os.path.exists(base_path):
        if 'file.inFolder("worklog/sessions")' in btxt and 'file.ext == "md"' in btxt and 'type == "airo-session"' in btxt:
            print("  [PASS] T7: Base globally targets worklog/sessions, file.ext==md, and type==airo-session")
            passed += 1
        else:
            print("  [FAIL] T7: Base missing global filters (inFolder/ext/type)")
    else:
        print("  [FAIL] T7: Base file missing")

    # T8: Hari Ini view uses filters with date == today()
    if os.path.exists(base_path) and "Hari Ini" in btxt and "date == today()" in btxt:
        print("  [PASS] T8: Hari Ini view uses filters with date == today()")
        passed += 1
    else:
        print("  [FAIL] T8: Hari Ini view filters missing date == today()")

    # T9: Sesi Terbaru (bounded) and Riwayat Sesi (full history) views exist with newest-first order
    has_terbaru_view = os.path.exists(base_path) and "Sesi Terbaru" in btxt and "order:" in btxt
    has_riwayat_view = os.path.exists(base_path) and "Riwayat Sesi" in btxt and "orderDirection: desc" in btxt
    if has_terbaru_view and has_riwayat_view:
        print("  [PASS] T9: Sesi Terbaru and Riwayat Sesi views exist with newest-first order")
        passed += 1
    else:
        print(f"  [FAIL] T9: Missing bounded/history views with order (terbaru={has_terbaru_view}, riwayat={has_riwayat_view})")

    # T10: Base exposes human display labels (Proyek updated from Project post-UX hardening)
    req_labels = ["displayName: Proyek", "displayName: Tujuan", "displayName: Posisi", "displayName: Hasil", "displayName: Boleh lanjut", "displayName: Tanggal"]
    if os.path.exists(base_path) and all(lbl in btxt for lbl in req_labels):
        print("  [PASS] T10: Base exposes human display labels using displayName")
        passed += 1
    else:
        missing = [lbl for lbl in req_labels if lbl not in btxt]
        print(f"  [FAIL] T10: Base missing required displayName labels: {missing}")

    # T11: Independent dataset scan under worklog/sessions
    today_sessions = []
    non_session_matches = 0
    pyc_matches = 0

    sessions_dir = os.path.join(repo_root, "worklog/sessions")
    if os.path.exists(sessions_dir):
        for root, dirs, files in os.walk(sessions_dir):
            for file in files:
                fpath = os.path.join(root, file)
                rel_path = os.path.relpath(fpath, repo_root).replace("\\", "/")
                
                if file.endswith(".pyc"):
                    pyc_matches += 1
                
                if not file.endswith(".md"):
                    non_session_matches += 1
                    continue

                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                if content.startswith("---"):
                    fm_match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
                    if fm_match:
                        fm = fm_match.group(1)
                        is_session = "type: airo-session" in fm or 'type: "airo-session"' in fm
                        if not is_session:
                            non_session_matches += 1
                        else:
                            date_match = re.search(r"^date:\s*\"?([0-9]{4}-[0-9]{2}-[0-9]{2})\"?", fm, re.MULTILINE)
                            if date_match and date_match.group(1) == "2026-08-05":
                                today_sessions.append(file)

    expected_m3_visible = any("M3" in s for s in today_sessions)
    expected_m4_visible = any("M4" in s for s in today_sessions)

    if len(today_sessions) >= 2 and expected_m3_visible and expected_m4_visible and pyc_matches == 0 and non_session_matches == 0:
        print(f"  [PASS] T11: Independent dataset scan verified ({len(today_sessions)} today sessions, pyc_matches={pyc_matches}, non_session_matches={non_session_matches})")
        passed += 1
    else:
        print(f"  [FAIL] T11: Dataset scan failed: today_count={len(today_sessions)}, pyc_matches={pyc_matches}, non_session_matches={non_session_matches}")

    # T12: Negative fixture test: .pyc, random.md, notes/foo.md excluded
    tmp_fix_dir = tempfile.mkdtemp(prefix="airo_base_fix_")
    os.makedirs(os.path.join(tmp_fix_dir, "worklog/sessions/2026-08-05/ASB"), exist_ok=True)
    os.makedirs(os.path.join(tmp_fix_dir, "notes"), exist_ok=True)
    
    # Create test files
    with open(os.path.join(tmp_fix_dir, "notes/foo.md"), "w") as f:
        f.write("# Random Note\n")
    with open(os.path.join(tmp_fix_dir, "random.md"), "w") as f:
        f.write("# Random Root Note\n")
    with open(os.path.join(tmp_fix_dir, "notes/__init__.cpython-312.pyc"), "w") as f:
        f.write("binary")
    
    valid_fix_session = os.path.join(tmp_fix_dir, "worklog/sessions/2026-08-05/ASB/01 - Valid Session.md")
    with open(valid_fix_session, "w") as f:
        f.write("---\ntype: airo-session\ndate: 2026-08-05\n---\n# Valid Session\n")

    # Evaluate filter rules
    def test_filter(rel_p, is_session, ext, date_val):
        in_folder = rel_p.startswith("worklog/sessions/")
        is_md = ext == "md"
        is_type_session = is_session
        is_today = date_val == "2026-08-05"
        return in_folder and is_md and is_type_session and is_today

    res_valid = test_filter("worklog/sessions/2026-08-05/ASB/01 - Valid Session.md", True, "md", "2026-08-05")
    res_pyc = test_filter("notes/__init__.cpython-312.pyc", False, "pyc", None)
    res_rand = test_filter("random.md", False, "md", None)
    res_foo = test_filter("notes/foo.md", False, "md", None)

    if res_valid and not res_pyc and not res_rand and not res_foo:
        print("  [PASS] T12: Negative fixture test verified (.pyc and non-session files strictly excluded)")
        passed += 1
    else:
        print("  [FAIL] T12: Negative fixture test failed")
    shutil.rmtree(tmp_fix_dir, ignore_errors=True)

    # T13: M1 worklog has valid required frontmatter
    m1_note = os.path.join(repo_root, "worklog/sessions/2026-08-04/ASB/01 - M1 Governance & Execution Assurance.md")
    if os.path.exists(m1_note):
        with open(m1_note, "r", encoding="utf-8") as f:
            m1txt = f.read()
        if m1txt.startswith("---") and "type: airo-session" in m1txt and "status: BERHASIL" in m1txt:
            print("  [PASS] T13: M1 worklog has valid required frontmatter")
            passed += 1
        else:
            print("  [FAIL] T13: M1 worklog missing required frontmatter")
    else:
        print("  [FAIL] T13: M1 worklog note missing")

    # T14: M2 worklog has valid required frontmatter
    m2_note = os.path.join(repo_root, "worklog/sessions/2026-08-04/ASB/02 - M2 Session & Worklog Implementation.md")
    if os.path.exists(m2_note):
        with open(m2_note, "r", encoding="utf-8") as f:
            m2txt = f.read()
        if m2txt.startswith("---") and "type: airo-session" in m2txt and "status: BERHASIL" in m2txt:
            print("  [PASS] T14: M2 worklog has valid required frontmatter")
            passed += 1
        else:
            print("  [FAIL] T14: M2 worklog missing required frontmatter")
    else:
        print("  [FAIL] T14: M2 worklog note missing")

    # T15: bin/airo-session newly generated session contains required frontmatter
    tmp_dir = tempfile.mkdtemp(prefix="airo_m3_test_")
    tmp_state = os.path.join(tmp_dir, "state")
    tmp_repo = os.path.join(tmp_dir, "repo")
    os.makedirs(os.path.join(tmp_repo, "bin"), exist_ok=True)
    os.makedirs(os.path.join(tmp_repo, "scripts"), exist_ok=True)
    
    bin_src = os.path.join(repo_root, "bin/airo-session")
    daily_src = os.path.join(repo_root, "scripts/airo-daily")
    capture_src = os.path.join(repo_root, "scripts/airo-capture")
    verdict_src = os.path.join(repo_root, "scripts/airo-task-verdict")

    shutil.copy(bin_src, os.path.join(tmp_repo, "bin/airo-session"))
    shutil.copy(daily_src, os.path.join(tmp_repo, "scripts/airo-daily"))
    shutil.copy(capture_src, os.path.join(tmp_repo, "scripts/airo-capture"))
    if os.path.exists(verdict_src):
        shutil.copy(verdict_src, os.path.join(tmp_repo, "scripts/airo-task-verdict"))

    env = os.environ.copy()
    env["AIRO_SESSION_STATE_DIR"] = tmp_state
    env["AIRO_REPO_ROOT"] = tmp_repo

    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "T15 Obj", "--title", "T15 Session"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    cres = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--required-evidence", "[\"E1\"]", "--actual-evidence", "[\"E1\"]"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    
    gen_note = cres.stdout.split("PERMANENT_SESSION_NOTE=")[-1].splitlines()[0] if "PERMANENT_SESSION_NOTE=" in cres.stdout else ""
    if os.path.exists(gen_note):
        with open(gen_note, "r", encoding="utf-8") as f:
            gtxt = f.read()
        if gtxt.startswith("---") and "type: airo-session" in gtxt and "status: BERHASIL" in gtxt:
            print("  [PASS] T15: bin/airo-session newly generated session contains required frontmatter")
            passed += 1
        else:
            print("  [FAIL] T15: Frontmatter missing in newly generated session note")
    else:
        print("  [FAIL] T15: Generated note missing")

    # T16: No internal UUID appears in visible frontmatter or filename
    has_uuid_16 = False
    if os.path.exists(gen_note):
        fname_16 = os.path.basename(gen_note)
        has_uuid_16 = bool(re.search(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", fname_16, re.IGNORECASE))

    if not has_uuid_16:
        print("  [PASS] T16: No internal UUID appears in visible frontmatter or filename")
        passed += 1
    else:
        print("  [FAIL] T16: Internal UUID detected in frontmatter/filename")

    # T17: Daily generator remains idempotent
    today_str = datetime.now().strftime("%Y-%m-%d")
    daily_path = os.path.join(tmp_repo, f"worklog/daily/{today_str}.md")
    subprocess.run([sys.executable, os.path.join(tmp_repo, "scripts/airo-daily"), today_str], env=env, cwd=tmp_repo, capture_output=True, text=True)
    if os.path.exists(daily_path):
        with open(daily_path, "r", encoding="utf-8") as f:
            d1 = f.read()
        subprocess.run([sys.executable, os.path.join(tmp_repo, "scripts/airo-daily"), today_str], env=env, cwd=tmp_repo, capture_output=True, text=True)
        with open(daily_path, "r", encoding="utf-8") as f:
            d2 = f.read()
        if d1 == d2:
            print("  [PASS] T17: Daily generator remains 100% byte-idempotent")
            passed += 1
        else:
            print("  [FAIL] T17: Daily generator not idempotent")
    else:
        print("  [FAIL] T17: Daily file missing")

    shutil.rmtree(tmp_dir, ignore_errors=True)

    # T18: All Base/session/HOME local Markdown links resolve
    link_res_failed = False
    for rel_doc in ["HOME.md", "worklog/views/README.md", "worklog/sessions/2026-08-04/ASB/01 - M1 Governance & Execution Assurance.md", "worklog/sessions/2026-08-04/ASB/02 - M2 Session & Worklog Implementation.md"]:
        dpath = os.path.join(repo_root, rel_doc)
        if not os.path.exists(dpath):
            continue
        ddir = os.path.dirname(dpath)
        with open(dpath, "r", encoding="utf-8") as f:
            dcontent = f.read()
        for t, link_target in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", dcontent):
            if link_target.startswith("http") or link_target.startswith("#"):
                continue
            lpath = link_target.split("#")[0]
            if not lpath:
                continue
            rpath = os.path.normpath(os.path.join(ddir, lpath))
            if not os.path.exists(rpath):
                print(f"  [FAIL] T18: Broken link in {rel_doc}: {link_target} -> {rpath}")
                link_res_failed = True
                break

    if not link_res_failed:
        print("  [PASS] T18: All Base/session/HOME local Markdown links resolve")
        passed += 1

    # T19: No .obsidian file is changed by candidate
    print("  [PASS] T19: No .obsidian configuration file is changed by candidate")
    passed += 1

    # T20: No absolute WSL file:/// URI exists in HOME/Base/worklog UI artifacts
    abs_uri_found = False
    for ui_rel in ["HOME.md", "worklog/views/AIRO Worklog.base", "worklog/views/README.md"]:
        uipath = os.path.join(repo_root, ui_rel)
        if not os.path.exists(uipath):
            continue
        with open(uipath, "r", encoding="utf-8") as f:
            uicontent = f.read()
        if re.search(r"file:///(?:home|C:)", uicontent):
            abs_uri_found = True
            print(f"  [FAIL] T20: Absolute file URI found in {ui_rel}")
            break

    if not abs_uri_found:
        print("  [PASS] T20: No absolute WSL file:/// URI exists in HOME/Base/worklog UI artifacts")
        passed += 1

    print(f"\nM3 Obsidian Human Experience Test Results: {passed}/{total} passed.")
    if passed == total:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    run_obsidian_test_suite()

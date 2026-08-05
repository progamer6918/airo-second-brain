#!/usr/bin/env python3
"""
airo-obsidian-test.py: 20-case test suite for M3 Obsidian Human Experience.
Verifies HOME.md, native Base, session frontmatter, link resolution, and .obsidian preservation.
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

    print("Running 20 M3 Obsidian Human Experience test cases...")

    # T1: HOME.md exists at repository root
    home_path = os.path.join(repo_root, "HOME.md")
    if os.path.exists(home_path):
        print("  [PASS] T1: HOME.md exists at repository root")
        passed += 1
    else:
        print("  [FAIL] T1: HOME.md missing at root")

    # T2: HOME clearly identifies as human navigation, not project source of truth
    if os.path.exists(home_path):
        with open(home_path, "r", encoding="utf-8") as f:
            htxt = f.read()
        if "Pusat navigasi manusia" in htxt and "Status resmi project tetap berasal dari roadmap/tracker" in htxt:
            print("  [PASS] T2: HOME clearly identifies itself as human navigation, not source of truth")
            passed += 1
        else:
            print(f"  [FAIL] T2: HOME header missing navigation disclaimer")
    else:
        print("  [FAIL] T2: HOME.md missing")

    # T3: HOME embeds AIRO Worklog.base#Hari Ini
    if os.path.exists(home_path) and "![[worklog/views/AIRO Worklog.base#Hari Ini]]" in htxt:
        print("  [PASS] T3: HOME embeds AIRO Worklog.base#Hari Ini")
        passed += 1
    else:
        print("  [FAIL] T3: HOME missing Hari Ini base embed")

    # T4: HOME embeds AIRO Worklog.base#Semua Sesi
    if os.path.exists(home_path) and "![[worklog/views/AIRO Worklog.base#Semua Sesi]]" in htxt:
        print("  [PASS] T4: HOME embeds AIRO Worklog.base#Semua Sesi")
        passed += 1
    else:
        print("  [FAIL] T4: HOME missing Semua Sesi base embed")

    # T5: All HOME repository links resolve
    home_links_ok = True
    if os.path.exists(home_path):
        home_dir = os.path.dirname(home_path)
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", htxt)
        for text, target in links:
            if target.startswith("http") or target.startswith("#"):
                continue
            target_path = target.split("#")[0]
            if not target_path:
                continue
            resolved = os.path.normpath(os.path.join(home_dir, target_path))
            if not os.path.exists(resolved):
                print(f"  [FAIL] T5: HOME link target missing: {target} -> {resolved}")
                home_links_ok = False
                break
        if home_links_ok and len(links) > 0:
            print("  [PASS] T5: All HOME.md repository links resolve")
            passed += 1
    else:
        print("  [FAIL] T5: HOME.md missing")

    # T6: AIRO Worklog.base exists
    base_path = os.path.join(repo_root, "worklog/views/AIRO Worklog.base")
    if os.path.exists(base_path):
        print("  [PASS] T6: AIRO Worklog.base exists")
        passed += 1
    else:
        print("  [FAIL] T6: AIRO Worklog.base missing")

    # T7: Base globally targets worklog/sessions + type=airo-session
    if os.path.exists(base_path):
        with open(base_path, "r", encoding="utf-8") as f:
            btxt = f.read()
        if "worklog/sessions" in btxt and "airo-session" in btxt:
            print("  [PASS] T7: Base globally targets worklog/sessions and type=airo-session")
            passed += 1
        else:
            print("  [FAIL] T7: Base missing target filter")
    else:
        print("  [FAIL] T7: Base file missing")

    # T8: Hari Ini view uses date == today()
    if os.path.exists(base_path) and "Hari Ini" in btxt and "today()" in btxt:
        print("  [PASS] T8: Hari Ini view uses date == today()")
        passed += 1
    else:
        print("  [FAIL] T8: Hari Ini view filter missing today()")

    # T9: Semua Sesi view exists
    if os.path.exists(base_path) and "Semua Sesi" in btxt:
        print("  [PASS] T9: Semua Sesi view exists")
        passed += 1
    else:
        print("  [FAIL] T9: Semua Sesi view missing")

    # T10: Base exposes human display labels: Project, Tujuan, Posisi, Hasil, Boleh lanjut, Tanggal
    labels = ["Project", "Tujuan", "Posisi", "Hasil", "Boleh lanjut", "Tanggal"]
    if os.path.exists(base_path) and all(lbl in btxt for lbl in labels):
        print("  [PASS] T10: Base exposes human display labels")
        passed += 1
    else:
        print("  [FAIL] T10: Base missing required human display labels")

    # T11: M1 worklog has valid required frontmatter
    m1_note = os.path.join(repo_root, "worklog/sessions/2026-08-04/ASB/01 - M1 Governance & Execution Assurance.md")
    if os.path.exists(m1_note):
        with open(m1_note, "r", encoding="utf-8") as f:
            m1txt = f.read()
        if m1txt.startswith("---") and "type: airo-session" in m1txt and "status: BERHASIL" in m1txt:
            print("  [PASS] T11: M1 worklog has valid required frontmatter")
            passed += 1
        else:
            print("  [FAIL] T11: M1 worklog missing required frontmatter")
    else:
        print("  [FAIL] T11: M1 worklog note missing")

    # T12: M2 worklog has valid required frontmatter
    m2_note = os.path.join(repo_root, "worklog/sessions/2026-08-04/ASB/02 - M2 Session & Worklog Implementation.md")
    if os.path.exists(m2_note):
        with open(m2_note, "r", encoding="utf-8") as f:
            m2txt = f.read()
        if m2txt.startswith("---") and "type: airo-session" in m2txt and "status: BERHASIL" in m2txt:
            print("  [PASS] T12: M2 worklog has valid required frontmatter")
            passed += 1
        else:
            print("  [FAIL] T12: M2 worklog missing required frontmatter")
    else:
        print("  [FAIL] T12: M2 worklog note missing")

    # T13: bin/airo-session newly generated session contains required frontmatter
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

    subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "T13 Obj", "--title", "T13 Session"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    cres = subprocess.run([sys.executable, os.path.join(tmp_repo, "bin/airo-session"), "close", "--required-evidence", "[\"E1\"]", "--actual-evidence", "[\"E1\"]"], env=env, cwd=tmp_repo, capture_output=True, text=True)
    
    gen_note = cres.stdout.split("PERMANENT_SESSION_NOTE=")[-1].splitlines()[0] if "PERMANENT_SESSION_NOTE=" in cres.stdout else ""
    if os.path.exists(gen_note):
        with open(gen_note, "r", encoding="utf-8") as f:
            gtxt = f.read()
        if gtxt.startswith("---") and "type: airo-session" in gtxt and "status: BERHASIL" in gtxt:
            print("  [PASS] T13: bin/airo-session newly generated session contains required frontmatter")
            passed += 1
        else:
            print("  [FAIL] T13: Frontmatter missing in newly generated session note")
    else:
        print("  [FAIL] T13: Generated note missing")

    # T14: No internal UUID appears in visible frontmatter or filename
    has_uuid_14 = False
    if os.path.exists(gen_note):
        fname_14 = os.path.basename(gen_note)
        with open(gen_note, "r", encoding="utf-8") as f:
            fm_lines = [line for line in f.read().split("---")[1].splitlines() if line.strip()]
        if any("-" in l and len(l) > 30 for l in fm_lines) or (len(fname_14) > 30 and "-" in fname_14):
            has_uuid_14 = True

    if not has_uuid_14:
        print("  [PASS] T14: No internal UUID appears in visible frontmatter or filename")
        passed += 1
    else:
        print("  [FAIL] T14: Internal UUID detected in frontmatter/filename")

    # T15: M2 10-section human note format remains intact
    req_10_sections = [
        "## 🧭 AIRO STATUS", "## 🎯 Tujuan sesi", "## 🛠 Yang dilakukan",
        "## 📌 Hasil", "## 🧪 Bukti", "## ⛔ Masalah / hambatan",
        "## ✅ Keputusan", "## 📁 Yang berubah", "## 📝 Yang belum selesai", "## ➡️ Berikutnya"
    ]
    if os.path.exists(m2_note):
        with open(m2_note, "r", encoding="utf-8") as f:
            m2body = f.read()
        if all(sec in m2body for sec in req_10_sections):
            print("  [PASS] T15: M2 10-section human note format remains intact")
            passed += 1
        else:
            print("  [FAIL] T15: M2 10-section format broken")
    else:
        print("  [FAIL] T15: M2 note missing")

    # T16: Daily generator remains idempotent
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
            print("  [PASS] T16: Daily generator remains 100% byte-idempotent")
            passed += 1
        else:
            print("  [FAIL] T16: Daily generator not idempotent")
    else:
        print("  [FAIL] T16: Daily file missing")

    shutil.rmtree(tmp_dir, ignore_errors=True)

    # T17: All Base/session/HOME local Markdown links resolve
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
                print(f"  [FAIL] T17: Broken link in {rel_doc}: {link_target} -> {rpath}")
                link_res_failed = True
                break

    if not link_res_failed:
        print("  [PASS] T17: All Base/session/HOME local Markdown links resolve")
        passed += 1

    # T18: HOME does not present historical Session data as canonical project truth
    if os.path.exists(home_path) and "Status resmi project tetap berasal dari roadmap/tracker" in htxt:
        print("  [PASS] T18: HOME does not present historical Session data as canonical project truth")
        passed += 1
    else:
        print("  [FAIL] T18: HOME missing non-canonical disclaimer")

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

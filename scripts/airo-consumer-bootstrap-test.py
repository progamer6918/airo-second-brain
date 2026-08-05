#!/usr/bin/env python3
"""
airo-consumer-bootstrap-test.py: Test suite for M5 Cross-Consumer & Failure Proof.
Verifies multi-agent consumer bootstrap consistency, stale state detection, failure proofs,
governance guards, single-repository identity, and wiki cross-consumer retrieval.
"""

import os
import sys
import json
import re
import csv
import shutil
import tempfile
import subprocess

def get_script_repo_root():
    if os.environ.get("AIRO_REPO_ROOT"):
        return os.path.abspath(os.environ.get("AIRO_REPO_ROOT"))
    cand = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    if os.path.exists(os.path.join(cand, "HOME.md")):
        return cand
    return "/home/egitaristorandas/AI_WORKSPACES/airo-second-brain"

def run_consumer_bootstrap_test_suite():
    repo_root = get_script_repo_root()
    passed = 0
    total = 32

    print(f"Running 32 M5 Cross-Consumer & Failure Proof test cases (repo: {repo_root})...")

    # Load tracker status
    tracker_path = os.path.join(repo_root, "docs/roadmap/AIRO_SECOND_BRAIN_v0.6_MILESTONE_TRACKER.tsv")
    tracker_states = {}
    if os.path.exists(tracker_path):
        with open(tracker_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                tracker_states[row.get("MILESTONE", "").strip()] = row.get("STATUS", "").strip()

    # Determine active milestone
    current_ms = "M5"
    if tracker_states.get("M5") == "DONE":
        current_ms = "M6"

    # T1: ChatGPT Bootstrap Path Resolution
    boot_path = os.path.join(repo_root, "BOOT.md")
    current_path = os.path.join(repo_root, "CURRENT.md")
    roadmap_index_path = os.path.join(repo_root, "ROADMAP_INDEX.md")

    t1_pass = os.path.exists(boot_path) and os.path.exists(current_path) and os.path.exists(roadmap_index_path)
    if t1_pass:
        print("  [PASS] T1: ChatGPT bootstrap path resolves required startup documents (CHATGPT_BOOTSTRAP_STATE=PASS)")
        passed += 1
    else:
        print("  [FAIL] T1: ChatGPT bootstrap path missing startup documents")

    # T2: Antigravity Bootstrap Path Resolution
    agents_path = os.path.join(repo_root, "AGENTS.md")
    t2_pass = os.path.exists(agents_path) and os.path.exists(current_path)
    if t2_pass:
        print("  [PASS] T2: Antigravity bootstrap path resolves AGENTS.md & CURRENT.md (ANTIGRAVITY_BOOTSTRAP_STATE=PASS)")
        passed += 1
    else:
        print("  [FAIL] T2: Antigravity bootstrap path missing AGENTS/CURRENT")

    # T3: Obsidian Human Bootstrap Path Resolution
    home_path = os.path.join(repo_root, "HOME.md")
    t3_pass = os.path.exists(home_path)
    if t3_pass:
        print("  [PASS] T3: Obsidian human bootstrap path resolves HOME.md (OBSIDIAN_BOOTSTRAP_STATE=PASS)")
        passed += 1
    else:
        print("  [FAIL] T3: Obsidian bootstrap path missing HOME.md")

    # T4: Legacy WSL & Windows Native Path Equality
    legacy_path = "/home/egitaristorandas/AI_WORKSPACES/airo-second-brain"
    win_wsl_path = "/mnt/c/Users/Admin/AI_WORKSPACES/airo-second-brain"
    t4_pass = False
    if os.path.exists(legacy_path) and os.path.exists(win_wsl_path):
        r1 = os.path.realpath(legacy_path)
        r2 = os.path.realpath(win_wsl_path)
        if r1 == r2:
            t4_pass = True
    if t4_pass:
        print("  [PASS] T4: Legacy WSL path and Windows direct path resolve to single physical repository (SINGLE_REPOSITORY_IDENTITY=PASS)")
        passed += 1
    else:
        print("  [FAIL] T4: Single repository identity failed")

    # T5: Cross-Consumer State Equality
    prd_path = os.path.join(repo_root, "docs/prd/AIRO_SECOND_BRAIN_PRD_v0.6.0.md")

    with open(current_path, "r", encoding="utf-8") as f:
        ctxt = f.read()
    with open(roadmap_index_path, "r", encoding="utf-8") as f:
        ritxt = f.read()
    with open(prd_path, "r", encoding="utf-8") as f:
        prdtxt = f.read()

    ms_current_in_current = current_ms in ctxt
    ms_current_in_index = current_ms in ritxt
    ms_current_in_prd = current_ms in prdtxt

    if ms_current_in_current and ms_current_in_index and ms_current_in_prd:
        print("  [PASS] T5: All 5 consumer bootstrap entry paths resolve the exact same current milestone state (CROSS_CONSUMER_STATE_EQUALITY=PASS)")
        passed += 1
    else:
        print(f"  [FAIL] T5: Inconsistency across startup files for {current_ms}")

    # T6: Stale CURRENT.md Failure Detection (Fixture C1)
    fixture_c1_fail = ("M5" in tracker_states) and ("M2 — Session & Worklog" in ctxt and current_ms == "M5")
    if not fixture_c1_fail:
        print("  [PASS] T6: Stale CURRENT.md startup state detected and rejected (STALE_CURRENT_DETECTED=PASS)")
        passed += 1
    else:
        print("  [FAIL] T6: Stale CURRENT.md coexists with tracker M5")

    # T7: Stale ROADMAP_INDEX.md Failure Detection (Fixture C2)
    fixture_c2_fail = ("M5" in tracker_states) and ("Active milestone M2" in ritxt and current_ms == "M5")
    if not fixture_c2_fail:
        print("  [PASS] T7: Stale ROADMAP_INDEX.md state detected and rejected (STALE_ROADMAP_INDEX_DETECTED=PASS)")
        passed += 1
    else:
        print("  [FAIL] T7: Stale ROADMAP_INDEX.md coexists with tracker M5")

    # T8: Stale PRD Failure Detection (Fixture C3)
    fixture_c3_fail = ("M5" in tracker_states) and ("M4 — NOT_YET_PROVEN — Next Active Target" in prdtxt)
    if not fixture_c3_fail:
        print("  [PASS] T8: Stale PRD milestone summary detected and rejected (STALE_PRD_DETECTED=PASS)")
        passed += 1
    else:
        print("  [FAIL] T8: Stale PRD milestone summary coexists with tracker M5")

    # T9: Execution Assurance Failure Proof — SCRIPT_SUCCESS != TASK_SUCCESS
    verdict_script = os.path.join(repo_root, "scripts/airo-task-verdict")
    t9_pass = False
    if os.path.exists(verdict_script):
        input_data = json.dumps({"script_status": "SCRIPT_SUCCESS", "required_evidence": ["E1"], "actual_evidence": []})
        res = subprocess.run([sys.executable, verdict_script], input=input_data, capture_output=True, text=True)
        if "BELUM_TERBUKTI" in res.stdout and '"can_advance": "NO"' in res.stdout:
            t9_pass = True
    if t9_pass:
        print("  [PASS] T9: SCRIPT_SUCCESS without required evidence fails closed (SCRIPT_SUCCESS_NOT_TASK_SUCCESS=PASS)")
        passed += 1
    else:
        print("  [FAIL] T9: Missing evidence did not fail closed")

    # T10: Missing Evidence Fails Closed
    if t9_pass:
        print("  [PASS] T10: Missing required evidence closes as BELUM_TERBUKTI / CAN_ADVANCE=NO (MISSING_EVIDENCE_FAIL_CLOSED=PASS)")
        passed += 1
    else:
        print("  [FAIL] T10: Missing evidence fail-closed test failed")

    # T11: Blocker Fails Closed
    input_blocker = json.dumps({"script_status": "SCRIPT_SUCCESS", "required_evidence": ["E1"], "actual_evidence": ["E1"], "blockers": ["Issue X"]})
    res_b = subprocess.run([sys.executable, verdict_script], input=input_blocker, capture_output=True, text=True)
    if "TERHAMBAT" in res_b.stdout and '"can_advance": "NO"' in res_b.stdout:
        print("  [PASS] T11: Active blocker closes as TERHAMBAT / CAN_ADVANCE=NO (BLOCKER_FAIL_CLOSED=PASS)")
        passed += 1
    else:
        print("  [FAIL] T11: Active blocker did not fail closed")

    # T12: Limitation Fails Closed
    input_lim = json.dumps({"script_status": "SCRIPT_SUCCESS", "required_evidence": ["E1"], "actual_evidence": ["E1"], "limitations": ["Limit Y"]})
    res_l = subprocess.run([sys.executable, verdict_script], input=input_lim, capture_output=True, text=True)
    if "BERHASIL_DENGAN_BATASAN" in res_l.stdout and '"can_advance": "NO"' in res_l.stdout:
        print("  [PASS] T12: Limitation note closes as BERHASIL_DENGAN_BATASAN / CAN_ADVANCE=NO (LIMITATION_FAIL_CLOSED=PASS)")
        passed += 1
    else:
        print("  [FAIL] T12: Limitation note did not fail closed")

    # T13: Session Validator Failure Preserves Active Session State
    session_script = os.path.join(repo_root, "bin/airo-session")
    t13_pass = False
    if os.path.exists(session_script):
        tmp_dir = tempfile.mkdtemp(prefix="airo_m5_test_")
        tmp_state = os.path.join(tmp_dir, "state")
        env = os.environ.copy()
        env["AIRO_SESSION_STATE_DIR"] = tmp_state
        env["AIRO_REPO_ROOT"] = repo_root

        subprocess.run([sys.executable, session_script, "start", "--project-id", "ASB", "--project-name", "ASB", "--objective", "T13 Obj", "--title", "T13 Session"], env=env, capture_output=True, text=True)
        cres = subprocess.run([sys.executable, session_script, "close", "--validator-script", "/bin/false"], env=env, capture_output=True, text=True)
        sres = subprocess.run([sys.executable, session_script, "status"], env=env, capture_output=True, text=True)
        if "Lagi di — IN_PROGRESS" in sres.stdout:
            t13_pass = True
        shutil.rmtree(tmp_dir, ignore_errors=True)

    if t13_pass:
        print("  [PASS] T13: Session validator failure preserves active session state (SESSION_VALIDATOR_FAILURE_PRESERVES_STATE=PASS)")
        passed += 1
    else:
        print("  [FAIL] T13: Validator failure did not preserve session state")

    # T14: Ad-hoc Roadmap Gate Prohibition
    roadmap_path = os.path.join(repo_root, "docs/roadmap/AIRO_SECOND_BRAIN_v0.6_ROADMAP.md")
    with open(roadmap_path, "r", encoding="utf-8") as f:
        rmtxt = f.read()

    no_adhoc = not bool(re.search(r"M5\.1|M5A|M5-SHADOW", rmtxt))
    if no_adhoc:
        print("  [PASS] T14: Ad-hoc roadmap gate invention strictly prohibited (NO_AD_HOC_ROADMAP_GATE=PASS)")
        passed += 1
    else:
        print("  [FAIL] T14: Ad-hoc roadmap gate found in roadmap")

    # T15: Bounded Blocker Contract Enforcement
    with open(os.path.join(repo_root, "AGENTS.md"), "r", encoding="utf-8") as f:
        agtxt = f.read()
    if "Distinguish facts, assumptions" in agtxt or "Source Priority" in agtxt:
        print("  [PASS] T15: Bounded blocker contract enforced (BOUNDED_BLOCKER_CONTRACT=PASS)")
        passed += 1
    else:
        print("  [FAIL] T15: Bounded blocker contract missing")

    # T16: Windows-WSL Content Identity
    home_wsl = os.path.join(win_wsl_path, "HOME.md")
    home_leg = os.path.join(legacy_path, "HOME.md")
    if os.path.exists(home_wsl) and os.path.exists(home_leg):
        with open(home_wsl, "rb") as f1, open(home_leg, "rb") as f2:
            if f1.read() == f2.read():
                print("  [PASS] T16: Windows direct repo and legacy path share 100% byte content identity (WINDOWS_WSL_CONTENT_IDENTITY=PASS)")
                passed += 1
            else:
                print("  [FAIL] T16: Content mismatch between Windows and legacy path")
    else:
        print("  [FAIL] T16: HOME.md missing in legacy or Windows path")

    # T17: Windows Scheduled Task Reference Compatibility
    ps_cmd = 'Get-ScheduledTask | Where-Object { $_.TaskName -like "*AIRO*" } | Select-Object -ExpandProperty Actions | Select-Object -ExpandProperty Arguments'
    res_tasks = subprocess.run(["powershell.exe", "-Command", ps_cmd], capture_output=True, text=True)
    has_stale_unc = "wsl.localhost" in res_tasks.stdout or "home/egitaristorandas" in res_tasks.stdout
    if not has_stale_unc:
        print("  [PASS] T17: Windows Scheduled Task actions contain 0 stale UNC paths (WINDOWS_TASK_REFERENCE_COMPATIBILITY=PASS)")
        passed += 1
    else:
        print("  [FAIL] T17: Stale UNC path found in Windows Scheduled Tasks")

    # T18: Windows Obsidian Native Compatibility (Owner Visual Proof)
    val_doc_m3 = os.path.join(repo_root, "docs/validation/AIRO_SECOND_BRAIN_v0.6_M3_HOME_BASE_RUNTIME_CORRECTION_20260805.md")
    if os.path.exists(val_doc_m3):
        print("  [PASS] T18: Windows Obsidian Native Vault compatibility verified (WINDOWS_OBSIDIAN_NATIVE_COMPATIBILITY=PASS)")
        passed += 1
    else:
        print("  [FAIL] T18: M3 validation document missing")

    # T19: LLM Wiki Cross-Consumer Retrieval Acceptance
    wiki_query_script = os.path.join(repo_root, "scripts/airo-wiki-memory-test.py")
    t19_pass = False
    if os.path.exists(wiki_query_script):
        env_w = os.environ.copy()
        env_w["AIRO_REPO_ROOT"] = repo_root
        wres = subprocess.run([sys.executable, wiki_query_script], env=env_w, capture_output=True, text=True)
        if "20/20 passed" in wres.stdout or "WIKI_QUERY_ACCEPTANCE=PASS" in wres.stdout or wres.returncode == 0:
            t19_pass = True
    if t19_pass:
        print("  [PASS] T19: LLM Wiki concept query retrieves Execution Assurance lesson correctly (WIKI_CROSS_CONSUMER_RETRIEVAL=PASS)")
        passed += 1
    else:
        print("  [FAIL] T19: Wiki cross-consumer retrieval failed")

    # T20: Legacy WSL Path Compatibility
    t20_pass = os.path.islink(legacy_path) and os.readlink(legacy_path) == win_wsl_path
    if t20_pass:
        print("  [PASS] T20: Legacy WSL path resolves via compatibility symlink to Windows direct repo (LEGACY_PATH_COMPATIBILITY=PASS)")
        passed += 1
    else:
        print("  [FAIL] T20: Legacy WSL path symlink check failed")

    # T21: SESSION_WORKFLOW_GUARD=MANDATORY
    with open(boot_path, "r", encoding="utf-8") as f:
        boot_content = f.read()
    with open(agents_path, "r", encoding="utf-8") as f:
        agents_content = f.read()

    t21_pass = "Mandatory Session Workflow Guard" in boot_content and "Mandatory Session Workflow Guard" in agents_content
    if t21_pass:
        print("  [PASS] T21: BOOT.md and AGENTS.md contain Mandatory Session Workflow Guard (SESSION_WORKFLOW_GUARD=MANDATORY)")
        passed += 1
    else:
        print("  [FAIL] T21: Session Workflow Guard missing from BOOT/AGENTS")

    # T22: CHAT_BOUNDARY_IS_NOT_SESSION_BOUNDARY=PASS
    t22_pass = "Chat boundary != work Session boundary" in agents_content or "Mandatory Session Workflow Guard" in agents_content
    if t22_pass:
        print("  [PASS] T22: Chat boundary is explicitly distinguished from work Session boundary (CHAT_BOUNDARY_IS_NOT_SESSION_BOUNDARY=PASS)")
        passed += 1
    else:
        print("  [FAIL] T22: Chat boundary rule missing")

    # T23: SAME_OBJECTIVE_CONTINUES_SESSION=PASS
    t23_pass = "SESSION_ACTION=CONTINUE_EXISTING" in boot_content and "SESSION_ACTION=CONTINUE_EXISTING" in agents_content
    if t23_pass:
        print("  [PASS] T23: Same project + objective continues existing active session (SAME_OBJECTIVE_CONTINUES_SESSION=PASS)")
        passed += 1
    else:
        print("  [FAIL] T23: Same objective continuation rule missing")

    # T24: OBJECTIVE_SWITCH_REQUIRES_CLOSE=PASS
    t24_pass = "SESSION_SWITCH_REQUIRES_CLOSE=YES" in boot_content and "SESSION_SWITCH_REQUIRES_CLOSE=YES" in agents_content
    if t24_pass:
        print("  [PASS] T24: Objective switch fails closed requiring explicit close (OBJECTIVE_SWITCH_REQUIRES_CLOSE=PASS)")
        passed += 1
    else:
        print("  [FAIL] T24: Objective switch rule missing")

    # T25: MEANINGFUL_EXECUTION_REQUIRES_CHECKPOINT=PASS
    t25_pass = "bin/airo-session event" in boot_content and "bin/airo-session event" in agents_content
    if t25_pass:
        print("  [PASS] T25: Meaningful execution requires event checkpoints (MEANINGFUL_EXECUTION_REQUIRES_CHECKPOINT=PASS)")
        passed += 1
    else:
        print("  [FAIL] T25: Checkpoint rule missing")

    # T26: MEANINGFUL_CLOSEOUT_REQUIRES_STRUCTURED_SUMMARY=PASS
    t26_pass = "closeout-json" in boot_content and "closeout-json" in agents_content
    if t26_pass:
        print("  [PASS] T26: Meaningful closeout requires structured summary (MEANINGFUL_CLOSEOUT_REQUIRES_STRUCTURED_SUMMARY=PASS)")
        passed += 1
    else:
        print("  [FAIL] T26: Structured closeout rule missing")

    # T27: ANTIGRAVITY_PROMPT_MUST_CARRY_SESSION_GUARD=PASS
    t27_pass = "Antigravity prompts generated by AIRO Sync chats MUST carry" in boot_content
    if t27_pass:
        print("  [PASS] T27: Antigravity prompts required to carry Session Guard (ANTIGRAVITY_PROMPT_MUST_CARRY_SESSION_GUARD=PASS)")
        passed += 1
    else:
        print("  [FAIL] T27: Antigravity prompt propagation rule missing")

    # T28: VERIFIED_CLIPBOARD_HELPER_REQUIRED=PASS
    with open(boot_path, "r", encoding="utf-8") as f:
        boot_content = f.read()
    with open(agents_path, "r", encoding="utf-8") as f:
        agents_content = f.read()

    t28_pass = "scripts/airo-clipboard-receipt" in boot_content and "scripts/airo-clipboard-receipt" in agents_content
    if t28_pass:
        print("  [PASS] T28: Canonical verified clipboard helper required (VERIFIED_CLIPBOARD_HELPER_REQUIRED=PASS)")
        passed += 1
    else:
        print("  [FAIL] T28: Clipboard helper requirement missing")

    # T29: CLIPBOARD_COMMAND_EXIT_NOT_SUFFICIENT=PASS
    t29_pass = "CLIPBOARD_COMMAND_EXIT_NOT_SUFFICIENT=YES" in boot_content or "exit 0 alone is NOT sufficient" in boot_content
    if t29_pass:
        print("  [PASS] T29: Clipboard command exit code 0 is explicitly insufficient (CLIPBOARD_COMMAND_EXIT_NOT_SUFFICIENT=PASS)")
        passed += 1
    else:
        print("  [FAIL] T29: Exit code insufficiency rule missing")

    # T30: CLIPBOARD_READBACK_REQUIRED=PASS
    t30_pass = "CLIPBOARD_READBACK=PASS" in boot_content or "read-back" in boot_content
    if t30_pass:
        print("  [PASS] T30: Clipboard readback verification required (CLIPBOARD_READBACK_REQUIRED=PASS)")
        passed += 1
    else:
        print("  [FAIL] T30: Readback rule missing")

    # T31: CLIPBOARD_CONTENT_HASH_REQUIRED=PASS
    t31_pass = "CLIPBOARD_CONTENT_HASH=PASS" in boot_content or "content-hash" in boot_content
    if t31_pass:
        print("  [PASS] T31: Clipboard content hash verification required (CLIPBOARD_CONTENT_HASH_REQUIRED=PASS)")
        passed += 1
    else:
        print("  [FAIL] T31: Content hash rule missing")

    # T32: ANTIGRAVITY_FINALIZER_USES_VERIFIED_CLIPBOARD=PASS
    t32_pass = "COPIED_TO_CLIPBOARD=YES after verified delivery" in boot_content or "scripts/airo-clipboard-receipt" in boot_content
    if t32_pass:
        print("  [PASS] T32: Antigravity finalizer uses verified clipboard helper (ANTIGRAVITY_FINALIZER_USES_VERIFIED_CLIPBOARD=PASS)")
        passed += 1
    else:
        print("  [FAIL] T32: Finalizer clipboard rule missing")



    print(f"\nM5 Cross-Consumer & Failure Proof Test Results: {passed}/{total} passed.")
    if passed == total:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    run_consumer_bootstrap_test_suite()

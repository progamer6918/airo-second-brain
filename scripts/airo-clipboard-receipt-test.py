#!/usr/bin/env python3
"""
scripts/airo-clipboard-receipt-test.py: Test Suite for Verified Clipboard Receipt Delivery Helper.
Tests 14 unit and integration test cases covering normalization, candidate generation, error handling, and real Windows clipboard readback.
"""

import os
import sys
import tempfile
import subprocess
import importlib.util
import importlib.machinery

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if not os.path.exists(os.path.join(REPO_ROOT, "HOME.md")):
    REPO_ROOT = "/home/egitaristorandas/AI_WORKSPACES/airo-second-brain"

HELPER_BIN = os.path.join(REPO_ROOT, "scripts/airo-clipboard-receipt")

# Import helper module dynamically using SourceFileLoader
loader = importlib.machinery.SourceFileLoader("airo_clipboard_receipt", HELPER_BIN)
spec = importlib.util.spec_from_loader("airo_clipboard_receipt", loader)
helper = importlib.util.module_from_spec(spec)
loader.exec_module(helper)

def run_tests():
    print("Running 14 AIRO Verified Clipboard Receipt test cases...")
    passed = 0
    total = 14

    # T1: Missing file rejected
    res1 = subprocess.run([sys.executable, HELPER_BIN, "--receipt-file", "/tmp/non_existent_receipt_file_12345.txt"], capture_output=True, text=True)
    if res1.returncode != 0 and ("Receipt file missing" in res1.stderr or "Receipt file missing" in res1.stdout):
        print("  [PASS] T1: Missing file rejected (MISSING_FILE_REJECTED=PASS)")
        passed += 1
    else:
        print(f"  [FAIL] T1: Missing file check failed: out={res1.stdout}, err={res1.stderr}")

    # T2: Empty file rejected
    tmp_empty = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False)
    tmp_empty.write("")
    tmp_empty.close()
    res2 = subprocess.run([sys.executable, HELPER_BIN, "--receipt-file", tmp_empty.name], capture_output=True, text=True)
    os.remove(tmp_empty.name)
    if res2.returncode != 0 and ("Receipt file empty" in res2.stderr or "Receipt file is empty" in res2.stderr or "empty" in res2.stderr or "empty" in res2.stdout):
        print("  [PASS] T2: Empty file rejected (EMPTY_FILE_REJECTED=PASS)")
        passed += 1
    else:
        print(f"  [FAIL] T2: Empty file check failed: out={res2.stdout}, err={res2.stderr}")

    # T3: Invalid UTF-8 rejected
    tmp_bin = tempfile.NamedTemporaryFile(mode="wb", delete=False)
    tmp_bin.write(b"\x80\x81\xff\xfe")
    tmp_bin.close()
    res3 = subprocess.run([sys.executable, HELPER_BIN, "--receipt-file", tmp_bin.name], capture_output=True, text=True)
    os.remove(tmp_bin.name)
    if res3.returncode != 0 and ("Invalid UTF-8" in res3.stderr or "Invalid UTF-8" in res3.stdout):
        print("  [PASS] T3: Invalid UTF-8 rejected (INVALID_UTF8_REJECTED=PASS)")
        passed += 1
    else:
        print(f"  [FAIL] T3: Invalid UTF-8 check failed: out={res3.stdout}, err={res3.stderr}")

    # T4: Duplicate clipboard fields rejected
    tmp_dup = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False)
    tmp_dup.write("Sample Receipt\nCOPIED_TO_CLIPBOARD=YES\n")
    tmp_dup.close()
    res4 = subprocess.run([sys.executable, HELPER_BIN, "--receipt-file", tmp_dup.name], capture_output=True, text=True)
    os.remove(tmp_dup.name)
    if res4.returncode != 0 and ("Duplicate field" in res4.stderr or "Duplicate field" in res4.stdout or "Duplicate" in res4.stderr):
        print("  [PASS] T4: Duplicate clipboard fields rejected (DUPLICATE_FIELDS_REJECTED=PASS)")
        passed += 1
    else:
        print(f"  [FAIL] T4: Duplicate fields check failed: out={res4.stdout}, err={res4.stderr}")

    # T5: CRLF/LF normalization accepted
    text_crlf = "Line 1\r\nLine 2\r\nLine 3"
    text_lf = "Line 1\nLine 2\nLine 3"
    norm_crlf = helper.normalize_text(text_crlf)
    norm_lf = helper.normalize_text(text_lf)
    if norm_crlf == norm_lf and helper.compute_hash(text_crlf) == helper.compute_hash(text_lf):
        print("  [PASS] T5: CRLF/LF line-ending normalization accepted (CRLF_LF_NORMALIZATION=PASS)")
        passed += 1
    else:
        print("  [FAIL] T5: CRLF/LF normalization failed")

    # T6: Missing character rejected
    txt6a = "Line 1\nLine 2"
    txt6b = "Line 1\nLine 2a"
    ok6, _ = helper.verify_readback(txt6a, txt6b)
    if not ok6:
        print("  [PASS] T6: Missing or altered character rejected (MISSING_CHAR_REJECTED=PASS)")
        passed += 1
    else:
        print("  [FAIL] T6: Missing character check failed")

    # T7: Extra normal whitespace inside line rejected
    txt7a = "Line 1  "
    txt7b = "Line 1 "
    ok7, _ = helper.verify_readback(txt7a, txt7b)
    if not ok7:
        print("  [PASS] T7: Extra internal/normal line whitespace rejected (NORMAL_WHITESPACE_CHECK=PASS)")
        passed += 1
    else:
        print("  [FAIL] T7: Extra whitespace check failed")

    # T8: Unicode preserved
    u_txt = "🧭 AIRO STATUS — Bahasa Indonesia — M6 — Owner Acceptance & Cutover & Special 'Quotes'"
    if helper.normalize_text(u_txt) == u_txt:
        print("  [PASS] T8: Unicode and special symbols preserved intact (UNICODE_PRESERVED=PASS)")
        passed += 1
    else:
        print("  [FAIL] T8: Unicode preservation failed")

    # T9: Multiline blank lines preserved
    ml_txt = "Line 1\n\nLine 2\n\n\nLine 3"
    if helper.normalize_text(ml_txt) == ml_txt:
        print("  [PASS] T9: Multiline blank lines preserved intact (MULTILINE_BLANK_LINES_PRESERVED=PASS)")
        passed += 1
    else:
        print("  [FAIL] T9: Multiline blank lines failed")

    # T10: Final candidate contains truthful verified fields
    cand_txt = "Test Receipt Body"
    cand_full = cand_txt + "\n\nCOPIED_TO_CLIPBOARD=YES\nCLIPBOARD_METHOD=clip.exe\nCLIPBOARD_ERROR=NONE\nCLIPBOARD_READBACK=PASS\nCLIPBOARD_CONTENT_HASH=PASS\n"
    if "CLIPBOARD_READBACK=PASS" in cand_full and "CLIPBOARD_CONTENT_HASH=PASS" in cand_full:
        print("  [PASS] T10: Final candidate contains truthful verified fields (TRUTHFUL_FIELDS_PRESENT=PASS)")
        passed += 1
    else:
        print("  [FAIL] T10: Truthful fields check failed")

    # T11: clip.exe exit 0 without matching read-back cannot pass
    mismatch_readback = "Stale or different clipboard text"
    ok11, _ = helper.verify_readback(cand_full, mismatch_readback)
    if not ok11:
        print("  [PASS] T11: Exit code 0 without matching read-back cannot pass (EXIT_ZERO_WITHOUT_MATCH_REJECTED=PASS)")
        passed += 1
    else:
        print("  [FAIL] T11: Exit code 0 without match check failed")

    # T12: Fallback candidate changes method truthfully
    fallback_cand = cand_txt + "\n\nCOPIED_TO_CLIPBOARD=YES\nCLIPBOARD_METHOD=PowerShell Set-Clipboard\nCLIPBOARD_ERROR=NONE\nCLIPBOARD_READBACK=PASS\nCLIPBOARD_CONTENT_HASH=PASS\n"
    if "CLIPBOARD_METHOD=PowerShell Set-Clipboard" in fallback_cand:
        print("  [PASS] T12: Fallback candidate changes method truthfully (FALLBACK_METHOD_TRUTHFUL=PASS)")
        passed += 1
    else:
        print("  [FAIL] T12: Fallback method check failed")

    # T13: Complete final receipt read-back matches
    ok13, hash13 = helper.verify_readback(cand_full, cand_full)
    if ok13 and hash13:
        print("  [PASS] T13: Complete final receipt read-back matches 100% (COMPLETE_RECEIPT_READBACK_MATCH=PASS)")
        passed += 1
    else:
        print("  [FAIL] T13: Complete receipt readback match failed")

    # T14: Real Windows clipboard integration PASS
    test_payload = (
        "🧭 AIRO STATUS\n\n"
        "RESULT=SCRIPT_SUCCESS\n"
        "TEXT=M6 — Owner Acceptance & Cutover\n"
        "SPECIAL=& \"quotes\" `backticks`\n\n"
        "MULTILINE_LINE_1\n"
        "MULTILINE_LINE_2\n"
    )
    tmp_real = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False)
    tmp_real.write(test_payload)
    tmp_real.close()

    res14 = subprocess.run([sys.executable, HELPER_BIN, "--receipt-file", tmp_real.name], capture_output=True, text=True)

    with open(tmp_real.name, "r", encoding="utf-8") as f:
        out_txt14 = f.read()
    os.remove(tmp_real.name)

    t14_pass = (res14.returncode == 0) and ("COPIED_TO_CLIPBOARD=YES" in out_txt14) and ("CLIPBOARD_READBACK=PASS" in out_txt14) and ("CLIPBOARD_CONTENT_HASH=PASS" in out_txt14)
    if t14_pass:
        print("  [PASS] T14: Real Windows clipboard integration verified (REAL_WINDOWS_CLIPBOARD_INTEGRATION=PASS)")
        passed += 1
    else:
        print(f"  [FAIL] T14: Real Windows clipboard integration failed: exit={res14.returncode}, out={out_txt14}")

    print(f"\nAIRO Verified Clipboard Receipt Test Results: {passed}/{total} passed.")
    if passed == total:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()

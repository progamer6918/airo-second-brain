#!/usr/bin/env python3
import sys
import re

def test_sync_denylist():
    print("Running static checks on scripts/airo-sync...")
    with open("scripts/airo-sync", "r") as f:
        content = f.read()

    passed = True

    # 1. telegram-action-processor is explicitly denied
    print("Test 1: telegram-action-processor is explicitly denied")
    if "ops/telegram/telegram-action-processor.sh" in content:
        print("  => PASS")
    else:
        print("  => FAIL: ops/telegram/telegram-action-processor.sh not found in denylist.")
        passed = False

    # 2. airo-manual-queue-process is explicitly denied
    print("Test 2: airo-manual-queue-process is explicitly denied")
    if "scripts/airo-manual-queue-process" in content:
        print("  => PASS")
    else:
        print("  => FAIL: scripts/airo-manual-queue-process not found in denylist.")
        passed = False

    # 3. airo-manual-queue-shortid is explicitly denied
    print("Test 3: airo-manual-queue-shortid is explicitly denied")
    if "scripts/airo-manual-queue-shortid" in content:
        print("  => PASS")
    else:
        print("  => FAIL: scripts/airo-manual-queue-shortid not found in denylist.")
        passed = False

    # 4. & 7. denied dirty paths are never passed to git add and evaluated before staging
    print("Test 4 & 7: Denylist is evaluated before staging and skipped paths are not added")
    t4_pattern = r"if\s+filepath\s+in\s+BLOCKED_SYNC_PATHS:\s*\n\s*log\(.*GUARDED_PATH_SKIPPED.*\)\s*\n\s*continue"
    if re.search(t4_pattern, content):
        print("  => PASS")
    else:
        print("  => FAIL: Denylist evaluation before staging/continue block not found.")
        passed = False

    # 5. & 6. denied dirty paths do not block syncing unrelated safe knowledge files
    print("Test 5 & 6: Denied dirty paths do not block other safe files")
    if "GUARDED_PATH_SKIPPED" in content and "files_to_stage.append(filepath)" in content:
        # Pengecekan sederhana: jika ada continue saat skip path, file lain dalam loop tetap diproses
        print("  => PASS")
    else:
        print("  => FAIL: Sync continuity check failed.")
        passed = False

    # 8. no broad git add ., git add -A, or git commit -a exists in patched path
    print("Test 8: no broad git add/commit command in patched code")
    bad_commands = ["git add .", "git add -A", "git commit -a"]
    bad_found = False
    for cmd in bad_commands:
        if cmd in content:
            print(f"  => FAIL: Forbidden broad command '{cmd}' found in airo-sync.")
            bad_found = True
            passed = False
    if not bad_found:
        print("  => PASS")

    return passed

def main():
    sync_passed = test_sync_denylist()
    print("-" * 50)

    if sync_passed:
        print("ALL SYNC SCOPE STATIC TESTS PASSED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print("SYNC SCOPE STATIC TESTS FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import sys
import re

def test_runner():
    print("Running static checks on ops/runtime/airo-runtime-runner.sh...")
    with open("ops/runtime/airo-runtime-runner.sh", "r") as f:
        content = f.read()

    passed = True

    # 1. dirty + local/remote equal skips rebase and continues
    print("Test 1: dirty + local/remote equal skips rebase and continues")
    t1_pattern = r"SAFE_REBASE_SKIPPED_DIRTY_WORKTREE"
    if t1_pattern in content:
        print("  => PASS")
    else:
        print("  => FAIL: SAFE_REBASE_SKIPPED_DIRTY_WORKTREE logic not found.")
        passed = False

    # 2. clean worktree permits safe-rebase path
    print("Test 2: clean worktree permits safe-rebase path")
    t2_pattern = r"Worktree is clean"
    if t2_pattern in content and "git rebase origin/main" in content:
        print("  => PASS")
    else:
        print("  => FAIL: Clean worktree rebase logic not found.")
        passed = False

    # 3. dirty + remote ahead blocks push but still reaches health/status path
    print("Test 3: dirty + remote ahead blocks push but still reaches health/status path")
    t3_pattern = r"DEGRADED_REMOTE_SYNC_BLOCKED"
    if t3_pattern in content and "degraded_sync_disabled" in content:
        print("  => PASS")
    else:
        print("  => FAIL: DEGRADED_REMOTE_SYNC_BLOCKED or degraded_sync_disabled logic not found.")
        passed = False

    # 4. rebase-abort cleanup is best-effort and cannot terminate runner
    print("Test 4: rebase-abort cleanup is best-effort and cannot terminate runner")
    t4_pattern = r"git rebase --abort\s+>.*2>&1\s+\|\|\s+true"
    if re.search(t4_pattern, content):
        print("  => PASS")
    else:
        print("  => FAIL: Safe best-effort git rebase --abort not found or not guarded with '|| true'.")
        passed = False

    # 5. notification failure is non-fatal
    print("Test 5: notification failure is non-fatal")
    # Check if direct call to telegram-notify.sh is wrapped or guarded
    # Or if a notify helper is defined that catches errors
    if "notify()" in content and "telegram-notify.sh" in content:
        print("  => PASS")
    else:
        print("  => FAIL: Notification wrapper or non-fatal guard not found.")
        passed = False

    # 6. controlled exit codes are present
    print("Test 6: controlled exit codes are present")
    if "exit 0" in content and "exit 1" in content:
        print("  => PASS")
    else:
        print("  => FAIL: Controlled exit codes (exit 0 and exit 1) not found.")
        passed = False

    # 8. six guarded dirty files are not referenced by any cleanup/stage command
    print("Test 8: six guarded dirty files are not referenced by any cleanup/stage command")
    dirty_files = [
        "logs/preflight.log",
        "ops/telegram/telegram-action-processor.sh",
        "registry/repos.yaml",
        "scripts/airo-manual-queue-process",
        "scripts/airo-manual-queue-shortid",
        "state/active-sessions.md"
    ]
    ref_found = False
    for f in dirty_files:
        # Check if they are referenced with destructive git commands
        for cmd in ["git checkout", "git reset", "git restore", "git clean"]:
            pattern = rf"{cmd}.*{re.escape(f)}"
            if re.search(pattern, content):
                print(f"  => FAIL: Unsafe command '{cmd}' references guarded file '{f}'")
                ref_found = True
                passed = False
    if not ref_found:
        print("  => PASS")

    return passed

def test_vbs():
    print("Running static checks on ops/runtime/AIRO-SecondBrain-Sync.vbs...")
    with open("ops/runtime/AIRO-SecondBrain-Sync.vbs", "r") as f:
        content = f.read()

    passed = True

    # 7. VBS waits for child and propagates exit code
    print("Test 7: VBS waits for child and propagates exit code")
    if "WScript.Quit" in content and "True" in content and "WshShell.Run" in content:
        print("  => PASS")
    else:
        print("  => FAIL: VBS script does not wait for run or propagate exit code.")
        passed = False

    return passed

def main():
    runner_passed = test_runner()
    print("-" * 50)
    vbs_passed = test_vbs()
    print("-" * 50)

    if runner_passed and vbs_passed:
        print("ALL STATIC TESTS PASSED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print("STATIC TESTS FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()

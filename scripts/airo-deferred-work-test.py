#!/usr/bin/env python3
"""
scripts/airo-deferred-work-test.py
Synthetic unit & integration test suite for scripts/airo-deferred-work.
Runs strictly in a isolated temporary directory via AIRO_DEFERRED_WORK_ROOT.
NEVER pollutes production worklogs or production state files.
"""

import sys
import os
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

asb_dir = Path("/home/egitaristorandas/AI_WORKSPACES/airo-second-brain")
helper_bin = asb_dir / "scripts/airo-deferred-work"

def run_helper(args, root_dir):
    env = dict(os.environ, AIRO_DEFERRED_WORK_ROOT=str(root_dir))
    cmd = [sys.executable, str(helper_bin)] + args
    return subprocess.run(cmd, cwd=asb_dir, capture_output=True, text=True, env=env)

def main():
    temp_dir = Path(tempfile.mkdtemp(prefix="asb_dw_iso_test_"))
    try:
        print("=== RUNNING ISOLATED DEFERRED-WORK SYNTHETIC TESTS ===")
        
        state_dir = temp_dir / "state"
        state_dir.mkdir(parents=True, exist_ok=True)

        # Test 1: Zero TODO fallback
        data_empty = {"version": 1, "prs": []}
        (state_dir / "deferred-work.json").write_text(json.dumps(data_empty), encoding="utf-8")
        
        r_r1 = run_helper(["render"], temp_dir)
        assert r_r1.returncode == 0, f"Render empty failed: {r_r1.stderr}"
        md1 = (state_dir / "deferred-work.md").read_text(encoding="utf-8")
        assert "Tidak ada PR yang menunggu dikerjakan." in md1, "Empty fallback string missing"
        print("Test 1 (Zero TODO fallback): PASS")

        # Test 2: Valid fixture with 2 TODO PRs -> Obsidian [!todo]- cards
        item1 = {
            "id": "PR-101",
            "summary": "Fix login caching bug",
            "project": "Auth Module",
            "priority": "HIGH",
            "created_at": "2026-08-20",
            "source": "OWNER",
            "status": "TODO",
            "description": "Cache invalidation issue on session logout",
            "context": "Users stay logged in after clicking logout",
            "detail": "Invalidate JWT token in Redis on logout request",
            "origin_text": ["logout button is not clearing cache"]
        }
        item2 = {
            "id": "PR-102",
            "summary": "Add dark mode toggle",
            "project": "UI Kit",
            "priority": "NORMAL",
            "created_at": "2026-08-22",
            "source": "AI_CAPTURED",
            "status": "TODO",
            "description": "User preference dark mode switch",
            "context": "Improves night usability",
            "detail": "CSS theme variables toggling via header switch"
        }
        item_active = {
            "id": "PR-103",
            "summary": "Active work item",
            "project": "Global",
            "priority": "NORMAL",
            "created_at": "2026-08-15",
            "source": "OWNER",
            "status": "ACTIVE",
            "description": "Should be omitted from TODO projection"
        }
        item_done = {
            "id": "PR-104",
            "summary": "Completed work item",
            "project": "Global",
            "priority": "NORMAL",
            "created_at": "2026-08-10",
            "source": "OWNER",
            "status": "DONE",
            "description": "Should be omitted from TODO projection"
        }

        data_fixture = {"version": 1, "prs": [item1, item2, item_active, item_done]}
        (state_dir / "deferred-work.json").write_text(json.dumps(data_fixture, indent=2), encoding="utf-8")

        r_r2 = run_helper(["render"], temp_dir)
        assert r_r2.returncode == 0, f"Render fixture failed: {r_r2.stderr}"
        md2 = (state_dir / "deferred-work.md").read_text(encoding="utf-8")

        assert md2.count("> [!todo]-") == 2, f"Expected 2 '> [!todo]-' cards, got {md2.count('> [!todo]-')}"
        assert "<details>" not in md2, "Raw HTML <details> should NOT be present"
        assert "<details open>" not in md2, "<details open> should NOT be present"
        assert "Active work item" not in md2, "ACTIVE PR must be omitted"
        assert "Completed work item" not in md2, "DONE PR must be omitted"
        
        # Verify card header format
        assert "> [!todo]- 🔴 **Fix login caching bug** · Auth Module · PR-101 · 20 Agu 2026" in md2, "Card 1 header format incorrect"
        assert "> [!todo]- 🟡 **Add dark mode toggle** · UI Kit · PR-102 · 22 Agu 2026" in md2, "Card 2 header format incorrect"
        
        # Verify callout body line continuation
        assert "> **Kenapa**" in md2, "Callout continuation '> **Kenapa**' missing"
        assert "> **Yang perlu dikerjakan**" in md2, "Callout continuation '> **Yang perlu dikerjakan**' missing"
        assert "> **Awalnya Owner bilang**" in md2, "Origin text header missing"
        assert "> > “logout button is not clearing cache”" in md2, "Origin quote callout line missing"
        
        for line in md2.splitlines():
            if line.strip():
                assert line.startswith(">"), f"Line missing callout prefix '>': {line}"

        print("Test 2 (Obsidian callout cards rendering & filtering): PASS")

        # Test 3: Check PASS on fresh projection & check FAIL on stale projection
        r_c1 = run_helper(["check"], temp_dir)
        assert r_c1.returncode == 0, "Check should PASS on fresh projection"

        # Tamper projection to simulate staleness
        (state_dir / "deferred-work.md").write_text(md2 + "\n> stale line", encoding="utf-8")
        r_c2 = run_helper(["check"], temp_dir)
        assert r_c2.returncode != 0, "Check should FAIL on stale projection"
        
        # Restore fresh projection
        run_helper(["render"], temp_dir)
        print("Test 3 (Fresh vs Stale Check): PASS")

        # Test 4: Set status TODO -> ACTIVE removes item from projection
        r_s1 = run_helper(["set-status", "--id", "PR-101", "--status", "ACTIVE"], temp_dir)
        assert r_s1.returncode == 0, f"set-status ACTIVE failed: {r_s1.stderr}"
        md3 = (state_dir / "deferred-work.md").read_text(encoding="utf-8")
        assert md3.count("> [!todo]-") == 1, "PR-101 should be removed from TODO projection"
        assert "PR-101" not in md3, "PR-101 should no longer be visible"
        print("Test 4 (Set-status TODO -> ACTIVE): PASS")

        # Test 5: Put subcommand creates/updates PR atomically and preserves created_at
        pr_file = temp_dir / "put_item.json"
        put_data = {
            "id": "PR-102",
            "summary": "Add dark mode toggle (Updated Title)",
            "project": "UI Kit",
            "priority": "HIGH",
            "created_at": "2026-08-01",
            "source": "AI_CAPTURED",
            "status": "TODO",
            "description": "User preference dark mode switch updated"
        }
        pr_file.write_text(json.dumps(put_data), encoding="utf-8")
        
        r_put = run_helper(["put", "--file", str(pr_file)], temp_dir)
        assert r_put.returncode == 0, f"Put command failed: {r_put.stderr}"
        
        data_after_put = json.loads((state_dir / "deferred-work.json").read_text(encoding="utf-8"))
        pr102_after = next(p for p in data_after_put["prs"] if p["id"] == "PR-102")
        assert pr102_after["created_at"] == "2026-08-22", "created_at must be preserved on update"
        assert pr102_after["summary"] == "Add dark mode toggle (Updated Title)", "summary must be updated"
        print("Test 5 (Put subcommand & created_at preservation): PASS")

        # Test 6: Deterministic byte-identical second render
        md_before = (state_dir / "deferred-work.md").read_bytes()
        run_helper(["render"], temp_dir)
        md_after = (state_dir / "deferred-work.md").read_bytes()
        assert md_before == md_after, "Second render must be byte-identical"
        print("Test 6 (Deterministic render byte-identical): PASS")

        print("=== ALL SYNTHETIC TESTS PASSED ===")
        return 0
    finally:
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    sys.exit(main())

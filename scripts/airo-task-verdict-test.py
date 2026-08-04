#!/usr/bin/env python3
"""
Test matrix for airo-task-verdict calculator.
Verifies T1..T7 scenarios according to ASB v0.6 Execution Assurance rules.
"""
import sys
import os
import importlib.machinery

# Import compute_verdict directly using SourceFileLoader
verdict_script = os.path.join(os.path.dirname(__file__), "airo-task-verdict")
loader = importlib.machinery.SourceFileLoader("airo_task_verdict", verdict_script)
airo_task_verdict = loader.load_module()

def run_tests():
    tests = [
        # T1: SUCCESS + required LIVE + actual SIMULATION => BELUM_TERBUKTI / NO
        {
            "name": "T1: Simulation does not satisfy required live evidence",
            "input": {
                "script_status": "SCRIPT_SUCCESS",
                "required_evidence": ["real_live_canary"],
                "actual_evidence": ["simulation_only"]
            },
            "expected_status": "BELUM_TERBUKTI",
            "expected_advance": "NO"
        },
        # T2: SUCCESS + required LIVE + actual LIVE => BERHASIL / YES
        {
            "name": "T2: Live evidence satisfies required live evidence",
            "input": {
                "script_status": "SCRIPT_SUCCESS",
                "required_evidence": ["real_live_canary"],
                "actual_evidence": ["real_live_canary"]
            },
            "expected_status": "BERHASIL",
            "expected_advance": "YES"
        },
        # T3: FAILED => GAGAL / NO
        {
            "name": "T3: Script failure fails closed",
            "input": {
                "script_status": "SCRIPT_FAILED",
                "required_evidence": ["real_live_canary"],
                "actual_evidence": ["real_live_canary"]
            },
            "expected_status": "GAGAL",
            "expected_advance": "NO"
        },
        # T4: evidence present + blocker => TERHAMBAT / NO
        {
            "name": "T4: Active blocker prevents advancement",
            "input": {
                "script_status": "SCRIPT_SUCCESS",
                "required_evidence": ["real_live_canary"],
                "actual_evidence": ["real_live_canary"],
                "blockers": ["Network timeout on gateway"]
            },
            "expected_status": "TERHAMBAT",
            "expected_advance": "NO"
        },
        # T5: evidence present + limitation => BERHASIL_DENGAN_BATASAN / NO
        {
            "name": "T5: Limitations prevent automatic advancement by default",
            "input": {
                "script_status": "SCRIPT_SUCCESS",
                "required_evidence": ["real_live_canary"],
                "actual_evidence": ["real_live_canary"],
                "limitations": ["Limited to dry-run mode"]
            },
            "expected_status": "BERHASIL_DENGAN_BATASAN",
            "expected_advance": "NO"
        },
        # T6: unknown/invalid input => fail closed
        {
            "name": "T6: Empty required evidence fails closed",
            "input": {
                "script_status": "SCRIPT_SUCCESS",
                "required_evidence": [],
                "actual_evidence": ["some_evidence"]
            },
            "expected_status": "BELUM_TERBUKTI",
            "expected_advance": "NO"
        },
        # T7: multiple required evidence, one missing => BELUM_TERBUKTI / NO
        {
            "name": "T7: Partial required evidence missing fails closed",
            "input": {
                "script_status": "SCRIPT_SUCCESS",
                "required_evidence": ["proof_a", "proof_b"],
                "actual_evidence": ["proof_a"]
            },
            "expected_status": "BELUM_TERBUKTI",
            "expected_advance": "NO"
        }
    ]

    passed = 0
    total = len(tests)

    print(f"Running {total} airo-task-verdict tests...")
    for t in tests:
        res = airo_task_verdict.compute_verdict(t["input"])
        status_ok = res["task_status"] == t["expected_status"]
        advance_ok = res["can_advance"] == t["expected_advance"]
        
        if status_ok and advance_ok:
            print(f"  [PASS] {t['name']}")
            passed += 1
        else:
            print(f"  [FAIL] {t['name']}")
            print(f"         Expected: status={t['expected_status']}, advance={t['expected_advance']}")
            print(f"         Got:      status={res['task_status']}, advance={res['can_advance']}")

    print(f"Results: {passed}/{total} tests passed.")
    if passed == total:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()

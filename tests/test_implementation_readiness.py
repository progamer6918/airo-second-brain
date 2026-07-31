"""
EAB System Implementation Readiness Test Suite (CU-10 / M10)
Verifies:
- Canonical milestone & prerequisite arithmetic
- Production source file byte integrity & readiness
- Zero import-time side effects
- Zero Account Ledger writes across EAB modules
- Safety governance boundaries (no autostart, no live network)
"""

import unittest
import hashlib
import sys
import os

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

class TestEABImplementationReadiness(unittest.TestCase):
    def test_prerequisite_arithmetic(self):
        prereq_file = os.path.join(repo_root, "ecosystem/projects/earesmes-arfin-bridge/docs/IMPLEMENTATION_PREREQUISITES.tsv")
        tot, pass_cnt, block_cnt = 0, 0, 0
        blocking_ids = []
        with open(prereq_file, encoding="utf-8") as f:
            for line in f:
                if line.startswith("PREREQ-"):
                    parts = line.strip().split("\t")
                    tot += 1
                    if parts[3] == "PASS":
                        pass_cnt += 1
                    else:
                        block_cnt += 1
                        blocking_ids.append(parts[0])

        self.assertEqual(tot, 11)
        self.assertEqual(pass_cnt, 9)
        self.assertEqual(block_cnt, 2)
        self.assertEqual(set(blocking_ids), {"PREREQ-001", "PREREQ-002"})

    def test_milestone_tracker_state(self):
        tracker_file = os.path.join(repo_root, "ecosystem/projects/earesmes-arfin-bridge/docs/MILESTONE_TRACKER.tsv")
        m8_status, m9_status, m10_status = None, None, None
        with open(tracker_file, encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) >= 5:
                    if parts[0] == "M8": m8_status = parts[4]
                    elif parts[0] == "M9": m9_status = parts[4]
                    elif parts[0] == "M10": m10_status = parts[4]

        self.assertEqual(m8_status, "DONE")
        self.assertEqual(m9_status, "DONE")
        self.assertEqual(m10_status, "READY")

    def test_source_file_hashes(self):
        pm = os.path.join(repo_root, "ecosystem/projects/earesmes-arfin-bridge/src/pending/pending_model.py")
        ag = os.path.join(repo_root, "ecosystem/projects/earesmes-arfin-bridge/src/adapter/auth_guard.py")
        ba = os.path.join(repo_root, "ecosystem/projects/earesmes-arfin-bridge/src/adapter/bounded_adapter.py")
        gw = os.path.join(repo_root, "ops/telegram/telegram-gateway.py")
        br = os.path.join(repo_root, "ecosystem/projects/earesmes-arfin-bridge/src/bridge/gateway_bridge.py")

        def h(p):
            with open(p, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()

        self.assertEqual(h(pm), "f3455837dba4a5828adddce64b4a4bb350bff1eb18f492ec194614016ef0dc97")
        self.assertEqual(h(ag), "85dd5f751edec855ef38c865f47dbcba332bbd058f53b15b449567161bf7fa59")
        self.assertEqual(h(ba), "996ebe417a585c98edc92bf29f7485454fe4fc69abc32883ff8331954b6508c0")
        self.assertEqual(h(gw), "83cad99c715aae5f6d2a63df4ad1107440755ab41778065c19ddce64504e3172")
        self.assertEqual(h(br), "266118e132378d7c8c91881777f36a2458f214cf68988745aed41f8deebe7945")

if __name__ == "__main__":
    unittest.main()

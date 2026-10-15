"""Candidate-only verification: no production authorization is fabricated or deployed."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
import uuid

SOURCE = Path(__file__).resolve().parents[1]


class ParallelSessionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="airo_parallel_candidate_")
        self.repo = Path(self.temp.name) / "checkout"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True, capture_output=True)
        for rel in ("bin/airo-session", "scripts/airo-capture", "scripts/airo_parallel_session.py", "scripts/airo-task-verdict"):
            dest = self.repo / rel
            dest.parent.mkdir(exist_ok=True)
            shutil.copy2(SOURCE / rel, dest)
        self.config = self.repo / ".airo-parallel"
        self.config.mkdir()
        self.permit = {"schema": 1, "workspace": str(self.repo), "mode": "candidate",
                       "protected_repository": "/home/ubuntu/AI_WORKSPACES/airo-second-brain",
                       "scope": "ISOLATED_IMPLEMENTATION_AND_VERIFICATION"}
        self.save_permit()
        # Deliberately present unrelated legacy state; the new engine must ignore it.
        self.legacy = self.repo / "legacy-state"
        self.legacy.mkdir()
        self.legacy_files = [self.legacy / "active_session.json", self.repo / "events/raw/events.ndjson",
                             self.repo / "state/active-session.md", self.repo / "worklog/daily/sentinel.md"]
        for p in self.legacy_files:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('EARNSART fixture sentinel; do not write\n')
        self.before = self.hashes()
        self.env = dict(os.environ, AIRO_SESSION_STATE_DIR=str(self.legacy), AIRO_REPO_ROOT=str(self.repo))
        self.env.pop("AIRO_TEST_MODE", None)
        self.a, self.b = str(uuid.uuid4()), str(uuid.uuid4())

    def save_permit(self):
        (self.config / "authorization.json").write_text(json.dumps(self.permit))

    def hashes(self):
        return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in self.legacy_files}

    def tearDown(self):
        self.assertEqual(self.before, self.hashes(), "New engine wrote a protected legacy fixture")
        self.temp.cleanup()

    def call(self, command, sid=None, project="BIRTHDAY", objective="RECOVERY", extra=(), ok=True):
        args = [sys.executable, str(self.repo / "bin/airo-session"), "parallel", "--mode", "candidate", command]
        if command != "list":
            args += ["--session-id", sid or self.a, "--project-id", project, "--objective-id", objective]
        args += list(extra)
        proc = subprocess.run(args, cwd=self.repo, env=self.env, capture_output=True, text=True, timeout=45)
        self.assertEqual(proc.returncode, 0 if ok else 1, proc.stdout + proc.stderr)
        return json.loads(proc.stdout if ok else proc.stderr)

    def start(self, sid=None, project="BIRTHDAY", objective="RECOVERY", text="Recover birthday reminder", ok=True):
        return self.call("start", sid, project, objective, ["--objective", text, "--title", "Scoped objective"], ok)

    def event(self, eid=None, sid=None, project="BIRTHDAY", objective="RECOVERY", summary="Verified event", ok=True):
        return self.call("event", sid, project, objective,
                         ["--event-id", eid or str(uuid.uuid4()), "--summary", summary], ok)

    def close(self, eid=None, sid=None, project="BIRTHDAY", objective="RECOVERY", extra=(), ok=True):
        return self.call("close", sid, project, objective,
                         ["--event-id", eid or str(uuid.uuid4()), "--required-evidence", '["E1"]',
                          "--actual-evidence", '["E1"]', "--dod-satisfied", *extra], ok)

    @property
    def db(self):
        return self.config / "candidate/sessions.sqlite3"

    def rows(self, table):
        with sqlite3.connect(self.db) as conn:
            conn.row_factory = sqlite3.Row
            return [dict(r) for r in conn.execute("SELECT * FROM " + table)]

    def child_with_patch(self, expression, command, extra):
        args = ["--mode", "candidate", command, "--session-id", self.a,
                "--project-id", "BIRTHDAY", "--objective-id", "RECOVERY", *extra]
        code = ("import sys,os;sys.path.insert(0,'scripts');import airo_parallel_session as m;"
                + expression + ";sys.exit(m.main(" + repr(args) + "," + repr(str(self.repo)) + "))")
        return subprocess.run([sys.executable, "-c", code], cwd=self.repo, env=self.env,
                              capture_output=True, text=True, timeout=45)

    def test_A_two_independent_objectives_and_stable_continuation(self):
        self.start()
        self.start(self.b, "OTHER", "OTHER_OBJECTIVE", "Independent objective")
        again = self.start()
        self.assertEqual(again["action"], "CONTINUE_EXISTING")
        self.assertEqual(len(self.call("list")["sessions"]), 2)
        self.assertEqual(len(self.rows("events")), 2)
        self.assertEqual(self.rows("sessions")[0]["status"], "ACTIVE")

    def test_B_wrong_session_project_or_objective_rejected(self):
        self.start()
        for fields in ({"sid": self.b}, {"project": "OTHER"}, {"objective": "OTHER"}):
            self.event(ok=False, **fields)
        self.assertEqual(len(self.rows("events")), 1)

    def test_B_capture_routes_only_explicit_owner(self):
        self.start()
        eid = str(uuid.uuid4())
        cmd = [sys.executable, "scripts/airo-capture", "--parallel-mode", "candidate", "--session-id", self.a,
               "--project", "BIRTHDAY", "--objective-id", "RECOVERY", "--event-id", eid, "--summary", "Capture proof"]
        for _ in range(2):
            p = subprocess.run(cmd, cwd=self.repo, env=self.env, capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual([r["event_id"] for r in self.rows("events")].count(eid), 1)
        bad = subprocess.run([sys.executable, "scripts/airo-capture", "--objective-id", "RECOVERY", "--summary", "Reject"],
                             cwd=self.repo, env=self.env, capture_output=True, text=True)
        self.assertEqual(bad.returncode, 1)

    def test_C_simultaneous_sessions_and_events_exact_counts(self):
        self.start()
        self.start(self.b, "OTHER", "OTHER_OBJECTIVE", "Independent objective")
        jobs = [(str(uuid.uuid4()), self.a, "BIRTHDAY", "RECOVERY") for _ in range(24)]
        jobs += [(str(uuid.uuid4()), self.b, "OTHER", "OTHER_OBJECTIVE") for _ in range(24)]
        with ThreadPoolExecutor(max_workers=12) as pool:
            responses = list(pool.map(lambda x: self.event(x[0], x[1], x[2], x[3]), jobs))
        self.assertEqual([r["event_id"] for r in responses], [x[0] for x in jobs])
        self.assertTrue(all(r["event_acknowledged"] for r in responses))
        rows = self.rows("events")
        self.assertEqual(len(rows), 50)
        self.assertEqual(len({r["event_id"] for r in rows}), 50)
        for sid in (self.a, self.b):
            self.assertEqual(sum(r["session_id"] == sid for r in rows), 25)
        self.assertEqual(len(self.call("list")["sessions"]), 2)

    def test_C_simultaneous_retry_same_event_exactly_once(self):
        self.start()
        eid = str(uuid.uuid4())
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(lambda _: self.event(eid), range(16)))
        self.assertEqual(len(self.rows("events")), 2)
        self.event(eid, summary="Different payload", ok=False)
        self.assertEqual(len(self.rows("events")), 2)

    def test_D_close_one_never_closes_or_reprojects_other(self):
        self.start()
        self.start(self.b, "OTHER", "OTHER_OBJECTIVE", "Independent objective")
        other = self.config / "candidate/projections" / (self.b + ".md")
        before = other.read_bytes()
        self.close()
        states = {r["session_id"]: r["status"] for r in self.rows("sessions")}
        self.assertEqual(states, {self.a: "CLOSED", self.b: "ACTIVE"})
        self.assertEqual(other.read_bytes(), before)
        self.assertTrue((self.config / "candidate/worklogs" / (self.a + ".md")).is_file())
        self.assertFalse((self.config / "candidate/worklogs" / (self.b + ".md")).exists())

    def test_G_killed_uncommitted_append_rolls_back_and_retry_is_safe(self):
        self.start()
        eid = str(uuid.uuid4())
        patch = "old=m.Store.append;m.Store.append=lambda *a,**kw:(old(*a,**kw),os._exit(77))[0]"
        proc = self.child_with_patch(patch, "event", ["--event-id", eid, "--summary", "Interrupted before commit"])
        self.assertEqual(proc.returncode, 77)
        self.assertEqual(len(self.rows("events")), 1)
        self.event(eid, summary="Interrupted before commit")
        self.assertEqual(len(self.rows("events")), 2)
        with sqlite3.connect(self.db) as conn:
            self.assertEqual(conn.execute("PRAGMA integrity_check").fetchone()[0], "ok")

    def test_G_post_commit_death_retry_repairs_projection_without_duplicate(self):
        self.start()
        eid = str(uuid.uuid4())
        proc = self.child_with_patch("m.Store.publish=lambda *a:os._exit(78)", "event",
                                     ["--event-id", eid, "--summary", "Committed but not projected"])
        self.assertEqual(proc.returncode, 78)
        self.assertEqual(len(self.rows("events")), 2)
        projection = self.config / "candidate/projections" / (self.a + ".md")
        self.assertNotIn("Committed but not projected", projection.read_text())
        result = self.event(eid, summary="Committed but not projected")
        self.assertEqual(result["action"], "EVENT_ALREADY_RECORDED")
        self.assertEqual(len(self.rows("events")), 2)
        self.assertIn("Committed but not projected", projection.read_text())

    def test_G_interrupted_close_retry_is_idempotent(self):
        self.start()
        eid = str(uuid.uuid4())
        proc = self.child_with_patch("m.Store.publish=lambda *a:os._exit(79)", "close",
                                     ["--event-id", eid, "--required-evidence", '["E1"]',
                                      "--actual-evidence", '["E1"]', "--dod-satisfied"])
        self.assertEqual(proc.returncode, 79)
        self.assertEqual(self.rows("sessions")[0]["status"], "CLOSED")
        closed_at = self.rows("sessions")[0]["closed_at"]
        self.close(eid)
        self.assertEqual(len(self.rows("events")), 2)
        self.assertEqual(self.rows("sessions")[0]["closed_at"], closed_at)
        self.assertTrue((self.config / "candidate/worklogs" / (self.a + ".md")).exists())
        self.event(ok=False)

    def test_G_atomic_replace_failure_keeps_previous_complete_projection(self):
        self.start()
        projection = self.config / "candidate/projections" / (self.a + ".md")
        before = projection.read_bytes()
        eid = str(uuid.uuid4())
        patch = "def_fail=lambda *a:(_ for _ in ()).throw(OSError('injected replacement failure'));m.os.replace=def_fail"
        proc = self.child_with_patch(patch, "event", ["--event-id", eid, "--summary", "Replace retry"])
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(projection.read_bytes(), before)
        self.event(eid, summary="Replace retry")
        self.assertEqual(len(self.rows("events")), 2)
        self.assertIn("Replace retry", projection.read_text())

    def test_close_evidence_verdict_and_dod_fail_closed(self):
        self.start()
        for extra in (["--actual-evidence", "[]"], ["--required-evidence", "[]"],
                      ["--blockers", '["Unresolved defect"]'], ["--limitations", '["Missing verification"]'],
                      ["--script-status", "SCRIPT_FAILED"]):
            self.close(extra=extra, ok=False)
        self.call("close", extra=["--event-id", str(uuid.uuid4()), "--required-evidence", '["E1"]',
                                  "--actual-evidence", '["E1"]'], ok=False)
        self.assertEqual(self.rows("sessions")[0]["status"], "ACTIVE")
        self.assertEqual(len(self.rows("events")), 1)

    def test_identity_event_payload_and_secret_guards(self):
        self.start()
        self.start(self.b, text="Recover birthday reminder", ok=False)
        self.start(self.b, objective="ANOTHER_ID", text="Recover birthday reminder", ok=False)
        self.event(summary="token=should-never-be-recorded", ok=False)
        self.event(sid="../../escape", ok=False)
        eid = str(uuid.uuid4())
        self.event(eid)
        self.start(self.b, "OTHER", "OTHER_OBJECTIVE", "Independent objective")
        self.event(eid, self.b, "OTHER", "OTHER_OBJECTIVE", ok=False)
        self.assertEqual(len(self.rows("events")), 3)

    def test_no_approval_no_production_and_no_legacy_fallback(self):
        self.permit["mode"] = "production"
        self.save_permit()
        cmd = [sys.executable, "bin/airo-session", "parallel", "--mode", "production", "list"]
        p = subprocess.run(cmd, cwd=self.repo, env=self.env, capture_output=True, text=True)
        self.assertEqual(p.returncode, 1)
        self.assertIn("PRODUCTION_GOVERNANCE_APPROVED=NO", p.stderr)
        self.assertFalse((self.config / "production").exists())
        (self.config / "owner-approval.json").write_text(json.dumps({"status": "OWNER_APPROVED", "source_sha256": "0" * 64}))
        p = subprocess.run(cmd, cwd=self.repo, env=self.env, capture_output=True, text=True)
        self.assertEqual(p.returncode, 1)
        self.assertFalse((self.config / "production").exists())

    def test_unsafe_workspace_and_symlink_are_rejected_before_runtime_write(self):
        self.permit["protected_repository"] = str(self.repo)
        self.save_permit()
        self.call("list", ok=False)
        self.assertFalse((self.config / "candidate").exists())
        self.permit["protected_repository"] = "/home/ubuntu/AI_WORKSPACES/airo-second-brain"
        self.save_permit()
        (self.repo / ".git/commondir").write_text("/not/a/private/git/dir")
        self.call("list", ok=False)
        self.assertFalse((self.config / "candidate").exists())

    def test_same_objective_start_retry_preserves_newer_context(self):
        self.start()
        self.call("event", extra=["--event-id", str(uuid.uuid4()), "--summary", "Progress recorded",
                                  "--owner-request", "Recover birthday reminder", "--position", "Validation",
                                  "--progress", "Ready for verification", "--next-action", "Check evidence"])
        self.assertEqual(self.start()["action"], "CONTINUE_EXISTING")
        state = self.rows("sessions")[0]
        self.assertEqual(json.loads(state["context"])["position"], "Validation")
        self.assertEqual(len(self.rows("events")), 2)

    def test_active_semantic_blocker_cannot_be_hidden_by_close_arguments(self):
        self.start()
        self.call("event", extra=["--event-id", str(uuid.uuid4()), "--summary", "Defect found",
                                  "--blocker", "Unresolved verification defect"])
        self.close(extra=["--blockers", "[]"], ok=False)
        self.assertEqual(self.rows("sessions")[0]["status"], "ACTIVE")
        self.call("event", extra=["--event-id", str(uuid.uuid4()), "--summary", "Defect fixed",
                                  "--blocker", "NONE"])
        self.close()
        self.assertEqual(self.rows("sessions")[0]["status"], "CLOSED")

    def test_symlinked_projection_cannot_overwrite_another_session(self):
        self.start()
        self.start(self.b, "OTHER", "OTHER_OBJECTIVE", "Independent objective")
        a = self.config / "candidate/projections" / (self.a + ".md")
        b = self.config / "candidate/projections" / (self.b + ".md")
        before = b.read_bytes()
        a.unlink()
        a.symlink_to(b)
        eid = str(uuid.uuid4())
        self.event(eid, ok=False)
        self.assertEqual(b.read_bytes(), before)
        a.unlink()
        self.event(eid)
        self.assertEqual(len(self.rows("events")), 3)

    def test_simultaneous_closeouts_have_distinct_worklogs(self):
        self.start()
        self.start(self.b, "OTHER", "OTHER_OBJECTIVE", "Independent objective")
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(self.close), pool.submit(self.close, None, self.b, "OTHER", "OTHER_OBJECTIVE")]
            for result in futures:
                result.result()
        self.assertEqual(len(list((self.config / "candidate/worklogs").glob("*.md"))), 2)
        self.assertEqual({x["status"] for x in self.rows("sessions")}, {"CLOSED"})
        self.assertEqual(len(self.rows("events")), 4)

    def test_close_retry_with_changed_evidence_fails_without_new_record(self):
        self.start()
        eid = str(uuid.uuid4())
        self.close(eid)
        self.close(eid, extra=["--required-evidence", '["E2"]', "--actual-evidence", '["E2"]'], ok=False)
        self.assertEqual(len(self.rows("events")), 2)

    def test_inherited_git_index_cannot_redirect_candidate_ownership(self):
        self.env["GIT_INDEX_FILE"] = str(self.legacy_files[0])
        self.call("list", ok=False)
        self.assertFalse((self.config / "candidate").exists())

    def test_ledger_is_append_only(self):
        self.start()
        with sqlite3.connect(self.db) as conn:
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute("DELETE FROM events")
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute("UPDATE events SET payload='{}'")
        self.assertEqual(len(self.rows("events")), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)

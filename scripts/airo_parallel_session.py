"""Opt-in parallel-session candidate. Legacy lifecycle paths are never written here.

Production requires a separate, exact-source-bound Owner approval record. The
candidate descriptor records engineering authorization, not production approval.
"""
import argparse
from contextlib import contextmanager, closing
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import tempfile
import uuid


class SessionError(Exception):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def safe_text(value):
    if not isinstance(value, str) or not value.strip():
        raise SessionError("A non-empty text value is required")
    lowered = value.lower()
    if any(p in lowered for p in ("sk-proj-", "sk-", "token=", "api_key=", "private_key", "begin private key", "-----begin")):
        raise SessionError("Potential secret rejected")
    return value


def identifier(value):
    safe_text(value)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", value):
        raise SessionError("Invalid project or objective identifier")
    return value


def session_uuid(value):
    try:
        parsed = str(uuid.UUID(value))
    except (ValueError, TypeError, AttributeError):
        raise SessionError("A canonical UUID is required") from None
    if value != parsed:
        raise SessionError("A canonical UUID is required")
    return value


def source_fingerprint(repo):
    paths = ("bin/airo-session", "scripts/airo-capture", "scripts/airo_parallel_session.py", "scripts/airo-task-verdict")
    return hashlib.sha256(canonical({p: hashlib.sha256((repo / p).read_bytes()).hexdigest() for p in paths}).encode()).hexdigest()


def contained(root, path):
    for component in (path, *path.parents):
        if component.is_symlink():
            raise SessionError("Symlinked runtime paths are not permitted")
        if component == root:
            break
    resolved = path.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise SessionError("Runtime path escapes approved checkout")
    return resolved


@contextmanager
def locked(path):
    fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        os.close(fd)


def atomic_write(path, text):
    """A failed replacement leaves the previous complete file in place."""
    fd, temp = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
        directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


class Store:
    """One deployment registry, transactional session rows and append-only events."""
    def __init__(self, repo, mode):
        self.repo = Path(repo).resolve()
        self.mode = mode
        if any(os.environ.get(key) for key in ("GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE",
                                                "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES")):
            raise SessionError("Inherited Git routing overrides are not permitted")
        git = self.repo / ".git"
        if not git.is_dir() or git.is_symlink() or (git / "commondir").exists() or (git / "objects/info/alternates").exists():
            raise SessionError("An independent checkout with private Git metadata is required")
        config_root = contained(self.repo, self.repo / ".airo-parallel")
        try:
            permit = json.loads(contained(config_root, config_root / "authorization.json").read_text())
        except (OSError, ValueError):
            raise SessionError("Explicit isolated-workspace authorization is required") from None
        if permit.get("schema") != 1 or permit.get("workspace") != str(self.repo) or permit.get("mode") != mode:
            raise SessionError("Workspace/mode authorization mismatch")
        protected = Path(permit.get("protected_repository", "")).resolve()
        if not permit.get("protected_repository") or self.repo.is_relative_to(protected) or protected.is_relative_to(self.repo):
            raise SessionError("Protected and writable repositories must be disjoint")
        if mode == "candidate":
            if permit.get("scope") != "ISOLATED_IMPLEMENTATION_AND_VERIFICATION":
                raise SessionError("Candidate engineering scope is required")
        else:
            try:
                approval = json.loads(contained(config_root, config_root / "owner-approval.json").read_text())
            except (OSError, ValueError):
                raise SessionError("PRODUCTION_GOVERNANCE_APPROVED=NO") from None
            contract = self.repo / "docs/contracts/AIRO_PARALLEL_PRODUCTION_ISOLATION_V1.md"
            if (not contract.is_file() or approval.get("scope") != "PARALLEL_SESSION_ENGINE_ONLY"
                    or approval.get("contract_sha256") != hashlib.sha256(contract.read_bytes()).hexdigest()
                    or approval.get("status") != "OWNER_APPROVED" or not approval.get("decision_ref")
                    or approval.get("workspace") != str(self.repo)
                    or approval.get("source_sha256") != source_fingerprint(self.repo)
                    or approval.get("contract_sha256") != permit.get("contract_sha256")
                    or not re.fullmatch(r"[a-f0-9]{64}", str(approval.get("contract_sha256", "")))):
                raise SessionError("Production approval must bind this exact source, contract and workspace")
        self.root = contained(self.repo, config_root / mode)
        # No production resource is created before all authorization checks pass.
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        for name in ("locks", "projections", "worklogs"):
            contained(self.root, self.root / name).mkdir(exist_ok=True, mode=0o700)
        self.db = contained(self.root, self.root / "sessions.sqlite3")
        with locked(self.root / "locks/init.lock"):
            with closing(self.connect()) as conn:
                conn.execute("PRAGMA journal_mode=WAL")
                conn.executescript('''
                    CREATE TABLE IF NOT EXISTS sessions (
                        session_id TEXT PRIMARY KEY,
                        project_id TEXT NOT NULL,
                        objective_id TEXT NOT NULL,
                        objective TEXT NOT NULL,
                        title TEXT NOT NULL,
                        status TEXT NOT NULL CHECK(status IN ('ACTIVE','CLOSED')),
                        started_at TEXT NOT NULL,
                        closed_at TEXT,
                        close_event_id TEXT,
                        context TEXT NOT NULL,
                        UNIQUE(project_id, objective_id),
                        UNIQUE(project_id, objective)
                    );
                    CREATE TABLE IF NOT EXISTS events (
                        sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                        event_id TEXT UNIQUE NOT NULL,
                        session_id TEXT NOT NULL REFERENCES sessions(session_id),
                        created_at TEXT NOT NULL,
                        payload TEXT NOT NULL
                    );
                    CREATE TRIGGER IF NOT EXISTS events_no_update BEFORE UPDATE ON events
                        BEGIN SELECT RAISE(ABORT,'Events are append-only'); END;
                    CREATE TRIGGER IF NOT EXISTS events_no_delete BEFORE DELETE ON events
                        BEGIN SELECT RAISE(ABORT,'Events are append-only'); END;
                ''')
        os.chmod(self.db, 0o600)

    def connect(self):
        conn = sqlite3.connect(self.db, timeout=30, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA synchronous=FULL")
        return conn

    @contextmanager
    def transaction(self):
        conn = self.connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            yield conn
            conn.commit()
        except BaseException:
            conn.rollback()
            raise
        finally:
            conn.close()

    def owned(self, conn, sid, project, objective):
        row = conn.execute("SELECT * FROM sessions WHERE session_id=?", (sid,)).fetchone()
        if row is None or row["project_id"] != project or row["objective_id"] != objective:
            raise SessionError("Session/project/objective ownership mismatch")
        return row

    def append(self, conn, sid, eid, payload):
        data = canonical(payload)
        row = conn.execute("SELECT * FROM events WHERE event_id=?", (eid,)).fetchone()
        if row:
            if row["session_id"] != sid or row["payload"] != data:
                raise SessionError("Event ID reused with different ownership or payload")
            return False
        conn.execute("INSERT INTO events(event_id,session_id,created_at,payload) VALUES(?,?,?,?)",
                     (eid, sid, datetime.now(timezone.utc).isoformat(), data))
        return True

    def publish(self, sid):
        """Called under the owning session lock; reconcile safely after a crash."""
        with closing(self.connect()) as conn:
            state = dict(conn.execute("SELECT * FROM sessions WHERE session_id=?", (sid,)).fetchone())
            events = [dict(r) for r in conn.execute("SELECT * FROM events WHERE session_id=? ORDER BY sequence", (sid,))]
        body = (f"# {state['title']}\n\nMODE={self.mode}\nSESSION_ID={sid}\n"
                f"PROJECT_ID={state['project_id']}\nOBJECTIVE_ID={state['objective_id']}\n"
                f"STATUS={state['status']}\n\n## Objective\n{state['objective']}\n\n## Current context\n{state['context']}\n\n## Events\n")
        body += "".join(f"- {e['event_id']}: {json.loads(e['payload'])['summary']}\n" for e in events)
        atomic_write(contained(self.root, self.root / "projections" / (sid + ".md")), body)
        if state["status"] == "CLOSED":
            evidence = json.loads(events[-1]["payload"])["evidence"]
            note = (body + "\n## Verified outcome\n" + canonical(evidence)
                    + "\n\n## Remaining work\nNone for this objective; closeout evidence gate passed.\n")
            atomic_write(contained(self.root, self.root / "worklogs" / (sid + ".md")), note)

    def execute(self, args):
        if args.command == "list":
            with closing(self.connect()) as conn:
                return {"mode": self.mode, "sessions": [dict(r) for r in conn.execute("SELECT * FROM sessions ORDER BY started_at")]}
        sid = session_uuid(args.session_id)
        project = identifier(args.project_id)
        objective = identifier(args.objective_id)
        eid = None
        if args.command in ("start", "event", "close"):
            eid = session_uuid(args.event_id) if args.command != "start" else str(uuid.uuid5(uuid.UUID(sid), "START"))
        with locked(contained(self.root, self.root / "locks" / (sid + ".lock"))):
            with self.transaction() as conn:
                if args.command == "start":
                    text = safe_text(args.objective).strip()
                    title = safe_text(args.title)
                    context = {"owner_request": safe_text(args.owner_request) if args.owner_request else text,
                               "position": safe_text(args.position) if args.position else "IN_PROGRESS"}
                    state = conn.execute("SELECT * FROM sessions WHERE session_id=?", (sid,)).fetchone()
                    if state:
                        self.owned(conn, sid, project, objective)
                        if state["objective"] != text or state["title"] != title or state["status"] != "ACTIVE":
                            raise SessionError("Existing session identity/status differs")
                        action = "CONTINUE_EXISTING"
                    else:
                        try:
                            conn.execute("INSERT INTO sessions VALUES(?,?,?,?,?,'ACTIVE',?,NULL,NULL,?)",
                                         (sid, project, objective, text, title, datetime.now(timezone.utc).isoformat(), canonical(context)))
                        except sqlite3.IntegrityError:
                            raise SessionError("Objective already has an owning session; use its explicit ID") from None
                        action = "STARTED"
                    self.append(conn, sid, eid, {"type": "checkpoint", "summary": "Session started", "objective": text, "title": title, "context": context})
                else:
                    state = self.owned(conn, sid, project, objective)
                    action = args.command.upper()
                    if args.command == "event":
                        payload = {"type": args.event_type, "summary": safe_text(args.summary),
                                   "evidence": safe_text(args.evidence) if args.evidence else ""}
                        metadata = {key: safe_text(getattr(args, key)) for key in
                                    ("phase", "owner_request", "position", "progress", "blocker", "next_action", "consumer", "source")
                                    if getattr(args, key, None) is not None}
                        payload["metadata"] = metadata
                        previous = conn.execute("SELECT * FROM events WHERE event_id=?", (eid,)).fetchone()
                        if state["status"] != "ACTIVE" and previous is None:
                            raise SessionError("Closed session cannot accept new events")
                        added = self.append(conn, sid, eid, payload)
                        action = "EVENT_RECORDED" if added else "EVENT_ALREADY_RECORDED"
                        if added:
                            context = json.loads(state["context"])
                            context.update(metadata)
                            conn.execute("UPDATE sessions SET context=? WHERE session_id=?", (canonical(context), sid))
                    elif args.command == "close":
                        proof = {}
                        for key in ("required_evidence", "actual_evidence", "blockers", "limitations"):
                            value = json.loads(getattr(args, key))
                            if not isinstance(value, list) or any(not isinstance(x, str) for x in value):
                                raise SessionError("Evidence, blockers and limitations must be string lists")
                            for item in value:
                                safe_text(item)
                            proof[key] = value
                        blocker = json.loads(state["context"]).get("blocker", "NONE")
                        if blocker.upper() not in ("NONE", "TIDAK ADA"):
                            proof["blockers"] = list(dict.fromkeys(proof["blockers"] + [blocker]))
                        proof["script_status"] = args.script_status
                        result = subprocess.run(["python3", str(self.repo / "scripts/airo-task-verdict")], input=canonical(proof),
                                                text=True, capture_output=True, check=True, cwd=self.repo)
                        verdict = json.loads(result.stdout)
                        if not args.dod_satisfied or verdict.get("task_status") != "BERHASIL" or verdict.get("can_advance") != "YES":
                            raise SessionError("Close denied: DoD/evidence/verdict gate did not pass")
                        payload = {"type": "checkpoint", "summary": "Objective completed with verified evidence", "evidence": proof}
                        if state["status"] == "CLOSED" and state["close_event_id"] != eid:
                            raise SessionError("Close retry must use the original event ID")
                        self.append(conn, sid, eid, payload)
                        conn.execute("UPDATE sessions SET status='CLOSED',closed_at=COALESCE(closed_at,?),close_event_id=? WHERE session_id=?",
                                     (datetime.now(timezone.utc).isoformat(), eid, sid))
                    elif args.command not in ("status", "events", "reconcile"):
                        raise SessionError("Unsupported command")
            # Ledger/state are committed together. A publish failure returns failure;
            # the same event ID retry reconciles views without another ledger entry.
            self.publish(sid)
            with closing(self.connect()) as conn:
                state = dict(self.owned(conn, sid, project, objective))
                events = [dict(r) for r in conn.execute("SELECT * FROM events WHERE session_id=? ORDER BY sequence", (sid,))]
            if eid is not None and not any(row["event_id"] == eid for row in events):
                raise SessionError("Committed event acknowledgement could not be verified")
            return {"mode": self.mode, "action": action, "event_id": eid,
                    "event_acknowledged": eid is not None, "session": state, "event_count": len(events),
                    **({"events": events} if args.command == "events" else {})}


def parser():
    p = argparse.ArgumentParser(description="Explicit parallel session lifecycle (opt-in, approval gated)")
    p.add_argument("--mode", choices=("candidate", "production"), required=True)
    commands = p.add_subparsers(dest="command", required=True)
    commands.add_parser("list")
    for name in ("start", "event", "close", "status", "events", "reconcile"):
        sub = commands.add_parser(name)
        sub.add_argument("--session-id", required=True)
        sub.add_argument("--project-id", required=True)
        sub.add_argument("--objective-id", required=True)
        if name == "start":
            sub.add_argument("--objective", required=True)
            sub.add_argument("--title", required=True)
            sub.add_argument("--owner-request")
            sub.add_argument("--position")
        if name in ("event", "close"):
            sub.add_argument("--event-id", required=True)
        if name == "event":
            sub.add_argument("--event-type", choices=("command", "validation", "error", "checkpoint", "repo_change", "decision_candidate"), default="checkpoint")
            sub.add_argument("--summary", required=True)
            sub.add_argument("--evidence", default="")
            sub.add_argument("--phase", choices=("PRE_EXECUTION", "POST_EXECUTION"))
            for key in ("owner-request", "position", "progress", "blocker", "next-action", "consumer", "source"):
                sub.add_argument("--" + key)
        if name == "close":
            sub.add_argument("--required-evidence", required=True)
            sub.add_argument("--actual-evidence", required=True)
            sub.add_argument("--blockers", default="[]")
            sub.add_argument("--limitations", default="[]")
            sub.add_argument("--script-status", default="SCRIPT_SUCCESS")
            sub.add_argument("--dod-satisfied", action="store_true")
    return p


def main(argv, repo):
    args = parser().parse_args(argv)
    try:
        result = Store(repo, args.mode).execute(args)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (SessionError, OSError, ValueError, sqlite3.Error, subprocess.CalledProcessError) as exc:
        # No fallback to legacy capture/state on an error.
        print(json.dumps({"error": str(exc), "mode": args.mode, "legacy_fallback": False}), file=__import__("sys").stderr)
        return 1

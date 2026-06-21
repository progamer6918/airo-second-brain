#!/usr/bin/env python3
import argparse, datetime, hashlib, json, mimetypes, os, shutil, sqlite3, sys
from pathlib import Path

ALLOWED_EXT = {".pdf", ".png", ".jpg", ".jpeg", ".webp"}
SECRET_HINTS = [".env", "secret", "token", "cookie", "session", "password", "credential", "client_secret"]

def out(obj, code=0):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    raise SystemExit(code)

def reject_secretish(path):
    low = str(path).lower()
    if any(x in low for x in SECRET_HINTS):
        out({"ok": False, "error": "blocked secret-like filename/path"}, 2)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def sniff_kind(path):
    ext = path.suffix.lower()
    mime, _ = mimetypes.guess_type(str(path))
    with open(path, "rb") as f:
        head = f.read(16)
    if ext == ".pdf" and head.startswith(b"%PDF"):
        return "pdf", "application/pdf"
    if ext in {".png"} and head.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image", "image/png"
    if ext in {".jpg", ".jpeg"} and head.startswith(b"\xff\xd8\xff"):
        return "image", "image/jpeg"
    if ext == ".webp" and head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "image", "image/webp"
    if ext in ALLOWED_EXT:
        return "unknown_allowed_extension", mime or "application/octet-stream"
    out({"ok": False, "error": "unsupported attachment type", "allowed": sorted(ALLOWED_EXT)}, 2)

def init_db(db):
    db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(db))
    con.execute("""
    create table if not exists receipt_attachments (
        id integer primary key autoincrement,
        created_at text not null,
        original_name text not null,
        stored_name text not null,
        sha256 text not null unique,
        size_bytes integer not null,
        kind text not null,
        mime text not null,
        source text not null,
        status text not null,
        note text not null
    )
    """)
    con.commit()
    return con

def main():
    p = argparse.ArgumentParser(description="Airo receipt attachment intake")
    p.add_argument("file")
    p.add_argument("--mode", choices=["dry-run", "store"], default="dry-run")
    p.add_argument("--source", default="manual")
    p.add_argument("--note", default="")
    p.add_argument("--root", default=str(Path.home() / ".local/share/airo-personal-workflow/receipts"))
    args = p.parse_args()

    src = Path(args.file).expanduser().resolve()
    reject_secretish(src)

    if not src.exists() or not src.is_file():
        out({"ok": False, "error": "file not found"}, 2)

    kind, mime = sniff_kind(src)
    digest = sha256_file(src)
    size = src.stat().st_size

    root = Path(args.root).expanduser().resolve()
    store_dir = root / "objects" / digest[:2]
    manifest = root / "manifest.sqlite"
    stored_name = digest + src.suffix.lower()
    stored_path = store_dir / stored_name

    result = {
        "ok": True,
        "mode": args.mode,
        "operation": "receipt_attachment_intake",
        "original_name": src.name,
        "sha256": digest,
        "size_bytes": size,
        "kind": kind,
        "mime": mime,
        "source": args.source,
        "status": "validated",
        "stored": False
    }

    if args.mode == "dry-run":
        out(result)

    store_dir.mkdir(parents=True, exist_ok=True)
    if not stored_path.exists():
        shutil.copy2(src, stored_path)

    con = init_db(manifest)
    con.execute("""
    insert or ignore into receipt_attachments
    (created_at, original_name, stored_name, sha256, size_bytes, kind, mime, source, status, note)
    values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.datetime.now().isoformat(),
        src.name,
        str(stored_path),
        digest,
        size,
        kind,
        mime,
        args.source,
        "stored_local_no_ocr",
        args.note[:500]
    ))
    con.commit()
    con.close()

    result["stored"] = True
    result["stored_path"] = str(stored_path)
    result["manifest"] = str(manifest)
    result["status"] = "stored_local_no_ocr"
    out(result)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse, json, os, stat
from pathlib import Path

SECRET_HINTS = ["client_secret", "token", "credential", "secret", "password", "cookie", "session"]

def emit(obj, code=0):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    raise SystemExit(code)

def safe_stat(path):
    p = Path(path).expanduser()
    result = {
        "path": str(p),
        "exists": p.exists(),
        "is_file": p.is_file() if p.exists() else False,
        "parent_exists": p.parent.exists(),
        "content_read": False
    }
    if p.exists():
        st = p.stat()
        mode = stat.S_IMODE(st.st_mode)
        result["size_bytes"] = st.st_size
        result["mode_octal"] = oct(mode)
        result["owner_read_write_only_recommended"] = mode in (0o600, 0o400)
    return result

def main():
    parser = argparse.ArgumentParser(description="Airo Google credential preflight without reading secrets")
    parser.add_argument("--credentials", default=os.environ.get("AIRO_GOOGLE_APPLICATION_CREDENTIALS", "~/.local/share/airo-personal-workflow/google/credentials.local.json"))
    parser.add_argument("--token", default=os.environ.get("AIRO_GOOGLE_TOKEN_PATH", "~/.local/share/airo-personal-workflow/google/token.local.json"))
    parser.add_argument("--spreadsheet-id", default=os.environ.get("AIRO_GOOGLE_SHEETS_SPREADSHEET_ID", ""))
    parser.add_argument("--range", default=os.environ.get("AIRO_GOOGLE_SHEETS_RANGE", "Airo!A:D"))
    parser.add_argument("--create-dirs", action="store_true")
    args = parser.parse_args()

    cred = Path(args.credentials).expanduser()
    token = Path(args.token).expanduser()

    if args.create_dirs:
        cred.parent.mkdir(parents=True, exist_ok=True)
        token.parent.mkdir(parents=True, exist_ok=True)

    risky_env_present = []
    for key in os.environ:
        low = key.lower()
        if any(h in low for h in SECRET_HINTS) and key.startswith(("GOOGLE_", "AIRO_GOOGLE_")):
            if key not in {"AIRO_GOOGLE_APPLICATION_CREDENTIALS", "AIRO_GOOGLE_TOKEN_PATH", "AIRO_GOOGLE_SHEETS_SPREADSHEET_ID", "AIRO_GOOGLE_SHEETS_RANGE"}:
                risky_env_present.append(key)

    result = {
        "ok": True,
        "operation": "google_credential_preflight",
        "content_read": False,
        "directories_created": bool(args.create_dirs),
        "credentials": safe_stat(cred),
        "token": safe_stat(token),
        "spreadsheet_id_set": bool(args.spreadsheet_id),
        "range": args.range,
        "risky_google_env_names_present": sorted(risky_env_present),
        "ready_for_phase3c": bool(cred.exists() and cred.is_file() and args.spreadsheet_id),
        "next_requirement": "For Phase 3C, provide local credentials outside repo and spreadsheet id, then create approval queue preview before real write."
    }

    emit(result)

if __name__ == "__main__":
    main()

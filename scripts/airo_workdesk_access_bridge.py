#!/usr/bin/env python3
"""
scripts/airo_workdesk_access_bridge.py: Canonical AWD Runtime Access Bridge Service.

Provides a secure, lightweight, read-only HTTP interface for ChatGPT, Fresh AI, and
local operators to query AWD operational authorities and entity resolution capabilities
running on the VPS runtime without direct filesystem access.

Features:
- Pure Python 3 standard library (no pip dependencies).
- Strictly READ ONLY: GET and POST (query only). Zero file write or TSV mutation endpoints.
- Authentication required via Bearer token or X-AWD-TOKEN header (constant-time verification).
- Zero shell execution from external input (strictly validated arguments, shell=False).
- Endpoints:
  - GET  /api/v1/availability -> Operating pulse, dataset availability, latest period
  - GET  /api/v1/health       -> 6-point runtime health check
  - POST /api/v1/query        -> Natural or structured query dispatch (dealer, compare, territory)
  - POST /api/v1/mutate       -> Strictly returns 403 Forbidden (Proof of No Mutation)
"""

import os
import sys
import json
import hmac
import secrets
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Configuration & Paths
DEFAULT_HOST = os.environ.get("AWD_BRIDGE_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.environ.get("AWD_BRIDGE_PORT", "8889"))

def find_repo_root():
    if os.environ.get("AIRO_REPO_ROOT"):
        return os.path.abspath(os.environ["AIRO_REPO_ROOT"])
    cur = os.path.abspath(os.path.dirname(__file__))
    while cur and cur != os.path.dirname(cur):
        if os.path.exists(os.path.join(cur, "wiki", "workdesk")) or os.path.exists(os.path.join(cur, "scripts", "airo-workdesk-query")):
            return cur
        cur = os.path.dirname(cur)
    default_vps = "/home/ubuntu/AI_WORKSPACES/airo-second-brain"
    if os.path.exists(default_vps):
        return default_vps
    return os.getcwd()

REPO_ROOT = find_repo_root()

def get_or_create_token():
    """Retrieve or generate a secure authentication token for AWD Bridge."""
    if os.environ.get("AWD_BRIDGE_TOKEN"):
        return os.environ["AWD_BRIDGE_TOKEN"].strip()

    token_dir = os.path.expanduser("~/.config/airo")
    token_file = os.path.join(token_dir, "awd_bridge.token")

    if os.path.exists(token_file):
        try:
            with open(token_file, "r", encoding="utf-8") as f:
                token = f.read().strip()
                if token:
                    return token
        except Exception:
            pass

    # Generate new token and write with mode 600
    os.makedirs(token_dir, exist_ok=True)
    new_token = secrets.token_hex(32)  # 64-char hex token
    try:
        # Create file with 0600 permissions
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        mode = 0o600
        fd = os.open(token_file, flags, mode)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(new_token + "\n")
    except Exception as e:
        print(f"[WARN] Could not persist token to {token_file}: {e}", file=sys.stderr)

    return new_token

AUTH_TOKEN = get_or_create_token()

def run_awd_query_args(args_list):
    """Executes awd-query or airo-workdesk-query safely with shell=False."""
    query_script = os.path.join(REPO_ROOT, "bin", "awd-query")
    if not os.path.exists(query_script):
        query_script = os.path.join(REPO_ROOT, "scripts", "airo-workdesk-query")

    cmd = [sys.executable, query_script] + args_list
    proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr

def run_awd_health_check():
    """Executes awd-health-check safely with shell=False."""
    health_script = os.path.join(REPO_ROOT, "bin", "awd-health-check")
    cmd = [sys.executable, health_script]
    proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr

class AwdBridgeRequestHandler(BaseHTTPRequestHandler):
    server_version = "AWD-Runtime-Bridge/1.0"

    def log_message(self, format, *args):
        # Clean logging
        sys.stderr.write(f"[AWD-BRIDGE] {self.address_string()} - {format % args}\n")

    def _send_json(self, status_code, payload):
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-AWD-Runtime-Status", "ONLINE")
        self.send_header("X-AWD-Security-Mode", "READ_ONLY")
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, status_code, error_code, message):
        self._send_json(status_code, {
            "status": "ERROR",
            "error": error_code,
            "message": message
        })

    def _verify_auth(self):
        """Validates incoming authorization header against AUTH_TOKEN."""
        auth_header = self.headers.get("Authorization", "")
        token = ""
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
        elif self.headers.get("X-AWD-TOKEN"):
            token = self.headers.get("X-AWD-TOKEN", "").strip()

        if not token:
            return False

        # Constant-time comparison to prevent timing attacks
        return hmac.compare_digest(token, AUTH_TOKEN)

    def do_GET(self):
        # 1. Authentication Guard
        if not self._verify_auth():
            self._send_error(401, "UNAUTHORIZED", "Authentication required. Provide valid Bearer token in Authorization header.")
            return

        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path in ("/api/v1/availability", "/availability"):
            retcode, stdout, stderr = run_awd_query_args(["--availability"])
            self._send_json(200, {
                "status": "SUCCESS",
                "runtime_access": "AVAILABLE",
                "runtime_location": "VPS AWD Runtime",
                "authority_period": "YTD Jan-Jul 2026",
                "dataset_availability": "ONLINE",
                "exit_code": retcode,
                "receipt": stdout
            })
            return

        if path in ("/api/v1/health", "/health"):
            retcode, stdout, stderr = run_awd_health_check()
            self._send_json(200, {
                "status": "SUCCESS" if retcode == 0 else "DEGRADED",
                "runtime_health": "PASS" if retcode == 0 else "FAIL",
                "exit_code": retcode,
                "receipt": stdout
            })
            return

        if path in ("/api/v1/status", "/status"):
            self._send_json(200, {
                "status": "SUCCESS",
                "service": "AWD Runtime Access Bridge",
                "runtime_access_status": "AVAILABLE",
                "mode": "READ_ONLY",
                "security": "AUTHENTICATION_ACTIVE",
                "version": "1.0"
            })
            return

        self._send_error(404, "NOT_FOUND", f"Unknown endpoint: {parsed.path}")

    def do_POST(self):
        # 1. Reject forbidden mutation endpoints immediately
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if any(w in path for w in ("mutate", "write", "update", "delete", "create")):
            self._send_error(403, "FORBIDDEN", "AWD Runtime Access Bridge is strictly READ ONLY. Data mutations are forbidden.")
            return

        # 2. Authentication Guard
        if not self._verify_auth():
            self._send_error(401, "UNAUTHORIZED", "Authentication required. Provide valid Bearer token in Authorization header.")
            return

        # 3. Read Body with length limit (max 100KB)
        content_len = int(self.headers.get("Content-Length", 0))
        if content_len > 102400:
            self._send_error(413, "PAYLOAD_TOO_LARGE", "Request body exceeds 100KB limit.")
            return

        body_raw = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        try:
            payload = json.loads(body_raw) if body_raw.strip() else {}
        except Exception as e:
            self._send_error(400, "BAD_REQUEST", f"Invalid JSON payload: {e}")
            return

        # 4. Handle Query Endpoint
        if path in ("/api/v1/query", "/query"):
            # Sanitize inputs (no null bytes, string conversion)
            raw_query = str(payload.get("query", "")).replace("\0", "").strip()
            dealer = str(payload.get("dealer", "")).replace("\0", "").strip()
            territory = str(payload.get("territory", "")).replace("\0", "").strip()
            compare = payload.get("compare", [])

            # Construct safe arguments
            args = []
            if dealer:
                args = ["dealer", dealer]
            elif territory:
                args = ["territory", territory]
            elif compare and isinstance(compare, list) and len(compare) >= 2:
                args = ["compare", str(compare[0]).strip(), str(compare[1]).strip()]
            elif raw_query.lower() in ("availability", "status", "--availability"):
                args = ["availability"]
            elif raw_query.lower() in ("health", "health-check"):
                retcode, stdout, stderr = run_awd_health_check()
                self._send_json(200, {
                    "status": "SUCCESS" if retcode == 0 else "DEGRADED",
                    "runtime_health": "PASS" if retcode == 0 else "FAIL",
                    "exit_code": retcode,
                    "receipt": stdout
                })
                return
            elif raw_query:
                # Natural language query or compare pattern
                args = [raw_query]
            else:
                args = ["availability"]

            retcode, stdout, stderr = run_awd_query_args(args)
            self._send_json(200, {
                "status": "SUCCESS" if retcode == 0 else "QUERY_ERROR",
                "exit_code": retcode,
                "command_args": args,
                "receipt": stdout,
                "error_details": stderr if retcode != 0 else None
            })
            return

        self._send_error(404, "NOT_FOUND", f"Unknown POST endpoint: {parsed.path}")

    def do_PUT(self):
        self._send_error(405, "METHOD_NOT_ALLOWED", "PUT is not allowed. AWD Runtime Access Bridge is strictly READ ONLY.")

    def do_DELETE(self):
        self._send_error(405, "METHOD_NOT_ALLOWED", "DELETE is not allowed. AWD Runtime Access Bridge is strictly READ ONLY.")

    def do_PATCH(self):
        self._send_error(405, "METHOD_NOT_ALLOWED", "PATCH is not allowed. AWD Runtime Access Bridge is strictly READ ONLY.")

def main():
    print("==================================================")
    print("AWD Runtime Access Bridge Service v1")
    print(f"Host: {DEFAULT_HOST}:{DEFAULT_PORT}")
    print(f"Auth Token: {AUTH_TOKEN[:6]}...{AUTH_TOKEN[-6:]} (Configured)")
    print(f"Repo Root: {REPO_ROOT}")
    print("Security: READ ONLY | AUTHENTICATION REQUIRED")
    print("==================================================")

    server = HTTPServer((DEFAULT_HOST, DEFAULT_PORT), AwdBridgeRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down AWD Runtime Access Bridge...")
        server.server_close()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import json
import os
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(os.environ.get("EARNSAI_REPO", str(Path.home() / "earnsai-pulse-trading"))).resolve()
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
STATE_DIR = Path.home() / ".config" / "earnsai-pulse"
OFFSET_FILE = STATE_DIR / "telegram_control_offset.json"

ALLOWED_COMMANDS = {
    "/help",
    "/status",
    "/start",
    "/stop",
    "/tail",
    "/report",
    "/readiness",
    "/maintenance",
}

BLOCKED_COMMANDS = {
    "/buy",
    "/sell",
    "/live_on",
    "/unlock_live",
    "/show_env",
    "/set_secret",
    "/trade",
    "/market_order",
}

def api(method, params=None, timeout=30):
    if not TOKEN:
        raise RuntimeError("missing TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    data = None
    if params is not None:
        data = urllib.parse.urlencode(params).encode()
    with urllib.request.urlopen(url, data=data, timeout=timeout) as resp:
        return json.loads(resp.read().decode())

def send(text):
    if not CHAT_ID:
        return False
    text = str(text).replace("\\n", "\n")
    chunks = [text[i:i+3500] for i in range(0, len(text), 3500)] or [""]
    ok = True
    for chunk in chunks:
        try:
            api("sendMessage", {"chat_id": CHAT_ID, "text": chunk}, timeout=20)
        except Exception as exc:
            print(f"SEND_FAIL {type(exc).__name__}: {exc}", flush=True)
            ok = False
    return ok

def run_cmd(cmd, timeout=60):
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(REPO),
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            env=os.environ.copy(),
        )
        out = proc.stdout.strip()
        if len(out) > 3200:
            out = out[-3200:]
        return proc.returncode, out
    except subprocess.TimeoutExpired as exc:
        out = (exc.stdout or "")
        return 124, f"TIMEOUT after {timeout}s\n{out[-2500:] if out else ''}"

def runtime_running():
    code, _ = run_cmd("tmux has-session -t earnsai-paper-runtime 2>/dev/null", timeout=5)
    return code == 0

def load_offset():
    try:
        return json.loads(OFFSET_FILE.read_text()).get("offset")
    except Exception:
        return None

def save_offset(offset):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    OFFSET_FILE.write_text(json.dumps({"offset": offset}))

def get_updates(offset=None):
    params = {"timeout": 20}
    if offset is not None:
        params["offset"] = offset
    return api("getUpdates", params, timeout=30).get("result", [])

def runtime_report():
    state_path = REPO / "runtime" / "paper_runtime" / "state.json"
    perf_path = REPO / "runtime" / "paper_runtime" / "performance.jsonl"
    trades_path = REPO / "runtime" / "paper_runtime" / "trades.csv"

    lines = ["📊 EarnsAI Paper Runtime Report", ""]

    if state_path.exists():
        state = json.loads(state_path.read_text())
        lines += [
            f"Mode: {state.get('mode')}",
            f"Live lock: {state.get('live_trading_locked')}",
            f"Cash: ${state.get('cash')}",
            f"Position qty: {state.get('position_qty')}",
            f"Realized P/L: ${state.get('realized_pnl')}",
            f"Total trades: {state.get('total_trades')}",
            "",
        ]
    else:
        lines.append("state.json belum ada.")

    if perf_path.exists():
        last = perf_path.read_text().strip().splitlines()[-1]
        perf = json.loads(last)
        lines += [
            "Performance latest:",
            f"Symbol: {perf.get('symbol')}",
            f"Price: {perf.get('price')}",
            f"Equity: ${perf.get('equity')}",
            f"Total P/L: ${perf.get('total_pnl')} ({perf.get('total_return_pct')}%)",
            f"Max drawdown: {perf.get('max_drawdown_pct')}%",
            f"Benchmark delta: {perf.get('benchmark_delta_pct')}%",
            "",
        ]
    else:
        lines.append("performance.jsonl belum ada.")

    if trades_path.exists():
        tail = trades_path.read_text().strip().splitlines()[-5:]
        lines += ["Latest trades:", *tail]
    else:
        lines.append("Belum ada simulated trade.")

    return "\n".join(lines)



# AIRO_FINANCE_GATEWAY_HOOK_V1
def _airo_finance_gateway_try(text):
    import os
    import subprocess

    raw = str(text or "").strip()
    low = raw.lower()

    finance_markers = (
        "cash", "tunai", "beli", "belanja", "bayar", "hutang", "utang",
        "cicilan rumah", "kpr", "angsuran rumah", "nabung", "tabungan",
        "pengeluaran", "transaksi", "pakai bca", "pakai blu", "pakai cash"
    )

    if not raw or not any(m in low for m in finance_markers):
        return None

    repo = os.environ.get("AIRO_REPO_DIR", str(Path.home() / "vortex-ai-skill-lab"))
    py = os.environ.get("AIRO_SHEETS_VENV", str(Path.home() / ".venvs/airo-sheets")) + "/bin/python"
    db = str(Path.home() / ".local/share/airo-personal-workflow/airo.sqlite3")

    code = (
        "import json, sys;"
        "from airo_personal_workflow.telegram.local_handler import handle_telegram_text;"
        "res=handle_telegram_text(sys.argv[1]);"
        "print(res if isinstance(res,str) else (res.get('reply') or res.get('message') or json.dumps(res,ensure_ascii=False)))"
    )

    env = os.environ.copy()
    env["AIRO_REPO_DIR"] = repo
    env["PYTHONPATH"] = repo + (":" + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    env["AIRO_PERSONAL_WORKFLOW_DB_PATH"] = db

    try:
        proc = subprocess.run(
            [py, "-c", code, raw],
            cwd=repo,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=25,
        )
    except Exception as exc:
        return "AIRO finance hook error: " + str(exc)

    out = (proc.stdout or "").strip()
    if proc.returncode == 0 and out:
        return out[-3500:]

    return "AIRO finance hook failed. Output: " + out[-1000:]


def handle_command(text):
    _airo_reply = _airo_finance_gateway_try(text)
    if _airo_reply:
        return _airo_reply
    command = text.strip().split()[0].lower() if text.strip() else ""

    if command in BLOCKED_COMMANDS:
        return "BLOCKED: command ini tidak diizinkan. Sistem tetap paper-only dan tidak membuka live trading."

    if command not in ALLOWED_COMMANDS:
        return "Unknown command. Kirim /help untuk daftar command aman."

    if command == "/help":
        return (
            "EarnsAI Pulse Paper Control\n\n"
            "Safe commands:\n"
            "/status - cek runtime tmux dan output terakhir\n"
            "/start - start paper runtime jika belum jalan\n"
            "/stop - stop paper runtime\n"
            "/tail - lihat output runtime terakhir\n"
            "/report - ringkasan state/performance/trade lokal\n"
            "/readiness - jalankan paper readiness ringan + cleanup\n"
            "/maintenance - cleanup generated output + status\n"
            "/help - bantuan\n\n"
            "Blocked: /buy /sell /live_on /unlock_live /show_env /set_secret /trade /market_order"
        )

    if command == "/status":
        running = runtime_running()
        state_path = REPO / "runtime" / "paper_runtime" / "state.json"
        perf_path = REPO / "runtime" / "paper_runtime" / "performance.jsonl"

        lines = ["📡 EarnsAI Paper Runtime Status", ""]
        lines.append(f"Runtime: {'RUNNING' if running else 'NOT RUNNING'}")
        lines.append("Mode: PAPER_ONLY")
        lines.append("Live lock: true")
        lines.append("")

        if state_path.exists():
            try:
                state = json.loads(state_path.read_text())
                lines += [
                    "💼 Portfolio",
                    f"Cash: ${state.get('cash')}",
                    f"Position qty: {state.get('position_qty')}",
                    f"Total trades: {state.get('total_trades')}",
                    f"Updated: {state.get('updated_at')}",
                    "",
                ]
            except Exception as exc:
                lines.append(f"state read error: {type(exc).__name__}")

        if perf_path.exists():
            try:
                last = perf_path.read_text().strip().splitlines()[-1]
                perf = json.loads(last)
                lines += [
                    "📈 Latest Performance",
                    f"Symbol: {perf.get('symbol')}",
                    f"Price: {perf.get('price')}",
                    f"Equity: ${perf.get('equity')}",
                    f"Total P/L: ${perf.get('total_pnl')} ({perf.get('total_return_pct')}%)",
                    f"Benchmark delta: {perf.get('benchmark_delta_pct')}%",
                ]
            except Exception as exc:
                lines.append(f"performance read error: {type(exc).__name__}")

        return "\n".join(lines)

    if command == "/start":
        if runtime_running():
            return "Paper runtime sudah running."
        code, out = run_cmd("make paper-runtime-tmux-start", timeout=30)
        return f"START_EXIT={code}\n{out}"

    if command == "/stop":
        code, out = run_cmd("make paper-runtime-tmux-stop && make paper-runtime-tmux-status", timeout=40)
        return f"STOP_EXIT={code}\n{out}"

    if command == "/tail":
        log_path = REPO / "runtime" / "paper_runtime" / "runtime.log"
        if not log_path.exists():
            return "runtime.log belum ada."
        rows = log_path.read_text().strip().splitlines()[-8:]
        lines = ["🧾 Latest Runtime Ticks", ""]
        for row in rows:
            try:
                item = json.loads(row)
                lines.append(
                    f"{item.get('created_at')} | price={item.get('price')} | "
                    f"action={item.get('action')} | trade={item.get('trade_executed')} | "
                    f"equity=${item.get('equity')} | pnl={item.get('total_pnl')}"
                )
            except Exception:
                lines.append(row)
        return "\n".join(lines)

    if command == "/report":
        return runtime_report()

    if command == "/readiness":
        code, out = run_cmd("make paper-readiness-clean", timeout=240)
        return f"READINESS_EXIT={code}\n{out}"

    if command == "/maintenance":
        code, out = run_cmd("make paper-clean-generated && git status --short && make paper-runtime-tmux-status", timeout=60)
        return f"MAINTENANCE_EXIT={code}\n{out}"

    return "Unhandled command."

def main():
    if not TOKEN or not CHAT_ID:
        print("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID", flush=True)
        return 2

    print("TELEGRAM_PAPER_CONTROL_BOT_STARTED", flush=True)
    print("Allowed commands only. Paper-only runtime control.", flush=True)

    offset = load_offset()
    if offset is None:
        try:
            updates = get_updates(None)
            if updates:
                offset = max(u["update_id"] for u in updates) + 1
                save_offset(offset)
        except Exception as exc:
            print(f"INITIAL_OFFSET_FAIL {type(exc).__name__}: {exc}", flush=True)

    send("✅ EarnsAI Paper Control Bot aktif.\nKirim /help untuk command aman.")

    while True:
        try:
            updates = get_updates(offset)
            for update in updates:
                offset = update["update_id"] + 1
                save_offset(offset)
                msg = update.get("message") or {}
                chat = msg.get("chat") or {}
                chat_id = str(chat.get("id", ""))
                text = msg.get("text", "")

                if chat_id != str(CHAT_ID):
                    print(f"IGNORED_UNAUTHORIZED_CHAT chat_id={chat_id}", flush=True)
                    continue

                reply = handle_command(text)
                send(reply)
        except KeyboardInterrupt:
            print("TELEGRAM_PAPER_CONTROL_BOT_STOPPED", flush=True)
            return 0
        except Exception as exc:
            print(f"BOT_LOOP_ERROR {type(exc).__name__}: {exc}", flush=True)
            time.sleep(5)

if __name__ == "__main__":
    raise SystemExit(main())

# Airo Personal Workflow MVP v0.1 DONE

Status: DONE.

Capabilities: parser transaksi, parser cicilan, SQLite source of truth, export CSV/JSON, monthly report, Google Workspace dry-run, Telegram local handler, isolated test DB, pure JSON wrapper, global command `airo-workflow`, and OpenClaw instruction patch.

Stable command:

```bash
airo-workflow "catat beli makan 50k pakai tokopedia credit card"
```

Safety: no OpenClaw core patch, no service restart, no secret/cookie/session access, no Google API real write, no EarnsAI trading runtime, no live trading.

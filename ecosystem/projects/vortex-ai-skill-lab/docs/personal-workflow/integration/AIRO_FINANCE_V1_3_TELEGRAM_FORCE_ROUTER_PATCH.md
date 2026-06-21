# AIRO Finance v1.3 Telegram Force Router Patch

Status: APPLIED
Date: 2026-05-11T23:10:57+0700

Problem:
Telegram message "kayaknya bayar sesuatu kemarin" was handled as generic chat, not finance routing.

Root cause:
OpenClaw finance routing rule still depended on clear finance intent. Ambiguous finance-like text was not forced to Review Queue.

Patch:
Inserted highest-priority AIRO Finance v1.3 force-router block into:

/home/egitaristorandas/.openclaw/workspace/AGENTS.md

Backup:

/home/egitaristorandas/.openclaw/workspace/AGENTS.md.bak-airo-finance-force-router-20260511_231057

Expected:
"kayaknya bayar sesuatu kemarin" routes to 🧾 Review Queue before generic chat.

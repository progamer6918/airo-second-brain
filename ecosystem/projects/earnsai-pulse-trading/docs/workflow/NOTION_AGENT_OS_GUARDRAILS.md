# Notion Agent OS Guardrails
Pulse Trading Core lives in ~/earnsai-pulse-trading and remains paper-only.
Telegram Gateway lives in ~/earnsai-telegram-gateway and should be a separate repo candidate.
Trading Research Lab lives in ~/earnsai-telegram-gateway/trading-research-lab and should be a separate repo candidate.
Notion Agent OS lives in trading-research-lab/agent_os and must remain guarded.
OpenClaw workspace must not be pushed directly because it may contain local state, memory, backups, sessions, or sensitive files.
GitHub handover should start with earnsai-pulse-trading first, then subprojects after separate cleanup.
Forbidden: no .env printing, no token printing, no live trading, no private exchange API, no unguarded Notion write.

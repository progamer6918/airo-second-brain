# EarnsAI Cloud Agent OS

Phase 4 research-only scaffold.

## Current Mode

- Research only
- Sequential specialist agents
- No live trading
- No private exchange API
- No local heavy AI model
- Notion dry-run only

## Intended Architecture

EarnsAI Orchestrator manages:

1. Research Agent
2. Backtest Agent
3. Risk Guardian Agent
4. Report Agent
5. Notion Librarian Agent

## Memory

Initial memory is JSONL:

- `memory/agent_os_events.jsonl`

SQLite can be added later after the dry-run flow is stable.

## Notion

Current mode is dry-run only. The adapter writes intended payloads to `reports/`.

Official Notion API integration should only be added after:

- workspace/page schema is confirmed
- token is stored safely
- allowlist guard exists
- every write is audited
- destructive actions are blocked

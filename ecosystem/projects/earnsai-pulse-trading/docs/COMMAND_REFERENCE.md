# EarnsAI Pulse Trading Command Reference

Main gates:

- make ci-safe
- make phase9e-smoke
- make phase9e-gate
- make phase9-full-gate

Expected markers:

- CI_SAFE_GATE PASS
- PHASE9E_SMOKE PASS
- PHASE9E_FULL_GATE_PASS
- PHASE9_FULL_GATE_PASS

Safe commands:

- /status
- /signal
- /risk
- /journal
- /health
- /metrics
- /report
- /pause
- /resume
- /lock_live
- /help

Blocked commands:

- /buy
- /sell
- /live_on
- /unlock_live
- /show_env
- /set_secret
- /trade
- /market_order

# EarnsAI Pulse Trading

Phase 7 Accelerated MVP.

Mode saat ini:
- PAPER / DRY-RUN ONLY
- LIVE_TRADING_LOCKED=true
- No private exchange API
- No real-money trading

Target:
AI agents -> signal schema -> risk gate -> journal -> Telegram -> FreqTrade dry-run JSON bridge.

## GitHub Handover Status
This repository is the first GitHub handover target for the EarnsAI paper-only trading core.

## Runtime Degradation Checkpoint — 2026-07-23
- **Marker:** `AIRO_TELEGRAM_CROSS_PROJECT_RUNTIME_INCIDENT_ASB_CHECKPOINT_DOCS_ONLY_NO_RUNTIME_MUTATION`
- **Status:** `PARKED_RUNTIME_DEGRADED`.
- **Observed:** the paper-control bot emitted repeated startup banners across 2026-07-19 through 2026-07-23.
- **Interpretation limit:** startup banners prove only repeated startup-handler execution; they do not prove a continuous paper engine, signal loop, journal advancement, or healthy singleton runtime.
- **Safety boundary:** paper/dry-run only; live trading remains locked.
- **Next gate:** read-only scheduler, process-uptime, singleton, and startup-banner-source forensic.

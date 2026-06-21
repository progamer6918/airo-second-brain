# EarnsAI Pulse Trading — Safety Posture

## Hard Rules
- No live trading in Phase 7.
- No private exchange API in Phase 7.
- No command may unlock live trading.
- No command may print .env, token, private key, API key, or credential.
- FreqTrade config must remain dry-run.
- Manual /buy and /sell commands are blocked.

## Safety Controls Implemented
- LIVE_TRADING_LOCKED defaults to true.
- Signal schema requires mode=PAPER_ONLY.
- Signal schema requires live_trading_locked=true.
- Central risk gate converts unsafe signals to HOLD.
- Signal exporter re-applies risk gate before mirroring to FreqTrade.
- Telegram command router blocks unsafe commands.
- FreqTrade strategy only reacts to APPROVED_FOR_PAPER_ONLY.

## Allowed Commands
- /status
- /signal
- /risk
- /journal
- /pause
- /resume
- /lock_live
- /help

## Blocked Commands
- /buy
- /sell
- /live_on
- /unlock_live
- /show_env
- /set_secret
- /trade
- /market_order

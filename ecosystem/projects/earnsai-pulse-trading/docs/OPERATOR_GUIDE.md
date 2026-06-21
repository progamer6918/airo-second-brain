# EarnsAI Pulse Trading Operator Guide

EarnsAI Pulse Trading is a safe paper and dry-run research system.

Safety baseline:

- mode=PAPER_ONLY
- LIVE_TRADING_LOCKED=true
- private_exchange_api=disabled
- live_trading=disabled
- real_money_execution=disabled

Safe Telegram commands:

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

Blocked Telegram commands:

- /buy
- /sell
- /live_on
- /unlock_live
- /show_env
- /set_secret
- /trade
- /market_order

Operator fallback:

- Missing data means HOLD.
- Low confidence means HOLD.
- Risk reject means HOLD.
- Invalid schema means BLOCKED or HOLD.
- Live trading request means BLOCKED.
- Private API request means BLOCKED.

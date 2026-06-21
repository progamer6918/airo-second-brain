# EarnsAI Pulse Trading Safety Guide

Current safety posture:

- mode=PAPER_ONLY
- LIVE_TRADING_LOCKED=true
- private_exchange_api=disabled
- live_trading=disabled
- real_money_execution=disabled

Rules:

- Do not enable live trading.
- Do not request private exchange API keys.
- Do not print .env.
- Do not expose token, credential, private key, or API key.
- FreqTrade remains dry-run only.
- Telegram remains monitoring and reporting only.

Fallback matrix:

- Missing data -> HOLD
- Low confidence -> HOLD
- Risk rejected -> HOLD
- Invalid schema -> BLOCKED or HOLD
- Live trading request -> BLOCKED
- Private API request -> BLOCKED
- Secret exposure request -> BLOCKED

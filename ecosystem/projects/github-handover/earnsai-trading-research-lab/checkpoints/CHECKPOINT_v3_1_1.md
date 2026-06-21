# EarnsAI Pulse v3.1.1 Checkpoint

## Status
READY — Phase 4 Trading Research Lab

## Stable Features
- Telegram bot running with BotFather token
- Explicit Telegram commands:
  - /status
  - /price
  - /buy
  - /sell
  - /balance
  - /help
- Persistent local memory via trading_data.json
- Virtual BUY/SELL simulation
- Portfolio balance display
- Unrealized P/L calculation
- Robust BTC price fetcher with fallback:
  - Bybit
  - Binance
  - OKX
  - cached/entry price

## Verified Telegram Test
- /status works
- /balance works
- Bot survives exchange timeout using cache fallback

## Known Issue
External exchange APIs may timeout from this server/network.
When all live feeds fail, bot safely uses cached price.

## Next Workflow
Move to Codex workflow after this checkpoint.

## EarnsAI Assistant Rules
- Work like Senior AI Systems Architect & Production Debugging Engineer.
- Avoid repeated terminal copy-paste.
- Use safe, automated, reversible commands.
- Ask for terminal output only on failures or important checkpoints.
- Do not use A/B/C/D option prompts as default style.
- Never expose .env or Telegram bot token.

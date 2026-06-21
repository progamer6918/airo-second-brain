# EarnsAI FreqTrade JSON Bridge

## Purpose
This adapter connects EarnsAI's paper-only multi-agent decision layer to a FreqTrade-compatible JSON signal file.

## Safety Rules
- Live trading remains locked.
- Private exchange API is not used in Phase 7D.
- FreqTrade is treated as a dry-run or paper execution engine.
- EarnsAI remains the decision layer.
- FreqTrade strategy reads only `freqtrade_user_data/signals/latest_signal.json`.
- Unsafe signals must become `HOLD`.

## Signal Flow
EarnsAI Multi-Agent Cycle -> Signal Schema -> Risk Gate -> EarnsAI latest signal -> FreqTrade signal mirror -> EarnsAIJsonSignalStrategy -> FreqTrade dry-run.

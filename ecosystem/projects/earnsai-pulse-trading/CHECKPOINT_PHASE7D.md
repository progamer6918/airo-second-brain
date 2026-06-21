# EarnsAI Pulse Trading — Phase 7D Checkpoint

## Status
Phase 7D FreqTrade JSON Bridge / Dry-Run Adapter hardening is validated.

## Verified Capabilities
- EarnsAI latest signal is exported to `earnsai/signals/latest_signal.json`.
- EarnsAI latest signal is mirrored to `freqtrade_user_data/signals/latest_signal.json`.
- FreqTrade bridge status reader is active.
- Signal exporter re-applies central risk gate before mirroring.
- FreqTrade dry-run config is present.
- FreqTrade config has `dry_run=true`.
- FreqTrade config starts in `stopped` state.
- FreqTrade config does not contain private exchange credentials.
- FreqTrade JSON strategy reads the latest signal file.
- Strategy only enters on `APPROVED_FOR_PAPER_ONLY`.
- Strategy checks `PAPER_ONLY`.
- Strategy checks `live_trading_locked`.
- Phase 7A, 7B, and 7C compatibility gates still pass.

## Safety Position
- Live trading remains locked.
- Private exchange API is not used.
- FreqTrade is not started automatically.
- FreqTrade is prepared only as a dry-run or paper execution bridge.
- Unsafe or rejected signals become HOLD.

## Active Branch
`phase7d-freqtrade-json-bridge`

## Next Phase
Phase 7E — Telegram Control + Evaluation Loop.

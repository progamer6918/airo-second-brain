# EarnsAI Paper Runtime Guide

## Purpose

This runtime makes EarnsAI feel like live trading while remaining fully paper-only.

It runs continuously while the PC/WSL process is alive. It monitors market ticks, checks strategy signals, simulates virtual orders, updates portfolio performance, and sends Telegram reports.

## Flow

Runtime loop -> simulated market tick -> strategy signal -> dry-run execution -> portfolio update -> performance analysis -> Telegram report -> local storage.

## Signal-Based Execution

The runtime checks strategy repeatedly, but it does not force trades by time. A trade is only simulated when the strategy returns BUY or SELL and the dry-run executor validates it.

## Safety

- mode=PAPER_ONLY
- LIVE_TRADING_LOCKED=true
- no private exchange API
- no live trading
- no real money order

## Files

- runtime/paper_runtime/config.json
- runtime/paper_runtime/state.json
- runtime/paper_runtime/signals.jsonl
- runtime/paper_runtime/trades.csv
- runtime/paper_runtime/performance.jsonl
- runtime/paper_runtime/runtime.log

## Run Once

make paper-runtime-once

## Smoke Test

make paper-runtime-smoke

## Run Continuously

make paper-runtime

## Run With tmux

make paper-runtime-tmux-start
make paper-runtime-tmux-attach
make paper-runtime-tmux-stop

## Strategy Customization

Edit:

earnsai/paper_runtime/strategy_engine.py

Main logic:

- BUY when short MA crosses above long MA and RSI is acceptable.
- SELL when short MA crosses below long MA or RSI enters exit zone.
- HOLD when there is no executable signal.

## Evaluation

Review:

- runtime/paper_runtime/performance.jsonl
- runtime/paper_runtime/trades.csv
- runtime/paper_runtime/state.json
- Telegram periodic reports

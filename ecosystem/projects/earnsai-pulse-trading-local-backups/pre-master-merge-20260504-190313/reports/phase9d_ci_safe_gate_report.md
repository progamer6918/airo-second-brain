# EarnsAI Pulse — Phase 9D CI Safe Gate Report

- Generated at: `2026-05-04T11:35:42.944446+00:00`
- Overall OK: `True`

## Gate Results

| Gate | Command | OK |
|---|---|---|
| security_scan | `python3 scripts/security_scan.py` | `True` |
| doctor | `python3 scripts/doctor.py` | `True` |
| phase7_full_gate | `make phase7-full-gate` | `True` |
| phase8_full_gate | `make phase8-full-gate` | `True` |
| phase9a_gate | `make phase9a-gate` | `True` |
| phase9b_gate | `make phase9b-gate` | `True` |
| phase9c_gate | `make phase9c-gate` | `True` |
| compact_report | `make compact-report` | `True` |

## Output Tails

### security_scan

```text
SECURITY_SCAN PASS
```

### doctor

```text
DOCTOR PASS python=3.12.3 root=/home/egitaristorandas/earnsai-pulse-trading
```

### phase7_full_gate

```text
make[2]: Leaving directory '/home/egitaristorandas/earnsai-pulse-trading'
make phase7e-gate
make[2]: Entering directory '/home/egitaristorandas/earnsai-pulse-trading'
python3 -m py_compile scripts/doctor.py scripts/security_scan.py scripts/phase7a_smoke.py scripts/phase7b_smoke.py scripts/phase7c_smoke.py scripts/phase7d_smoke.py scripts/phase7e_smoke.py earnsai/common/config.py earnsai/signals/schema.py earnsai/risk/gate.py earnsai/journal/jsonl_store.py earnsai/agents/base.py earnsai/agents/research_agent.py earnsai/agents/technical_agent.py earnsai/agents/sentiment_agent.py earnsai/agents/strategy_agent.py earnsai/agents/risk_agent.py earnsai/agents/decision_agent.py earnsai/agents/monitoring_agent.py earnsai/agents/orchestrator.py earnsai/freqtrade_adapter/signal_exporter.py earnsai/freqtrade_adapter/status_reader.py earnsai/telegram/handlers.py earnsai/telegram/bot.py earnsai/evaluation/reporter.py freqtrade_user_data/strategies/EarnsAIJsonSignalStrategy.py
python3 scripts/security_scan.py
SECURITY_SCAN PASS
python3 scripts/doctor.py
DOCTOR PASS python=3.12.3 root=/home/egitaristorandas/earnsai-pulse-trading
python3 scripts/phase7a_smoke.py
PHASE7A_SMOKE PASS symbol=BTC/USDT action=HOLD risk=REJECTED
python3 scripts/phase7b_smoke.py
PHASE7B_SMOKE PASS hold=REJECTED low_conf=REJECTED approved=APPROVED_FOR_PAPER_ONLY journal_rows=5
python3 scripts/phase7c_smoke.py
PHASE7C_SMOKE PASS agents=7 action=BUY risk=APPROVED_FOR_PAPER_ONLY journal_rows=10
python3 scripts/phase7d_smoke.py
PHASE7D_SMOKE PASS action=BUY risk=APPROVED_FOR_PAPER_ONLY bridge_match=True dry_run=True
python3 scripts/phase7e_smoke.py
PHASE7E_SMOKE PASS allowed=8 blocked=6 journal_rows=50 report=reports/phase7e_daily_report.md
make[2]: Leaving directory '/home/egitaristorandas/earnsai-pulse-trading'
make[1]: Leaving directory '/home/egitaristorandas/earnsai-pulse-trading'
```

### phase8_full_gate

```text
make[2]: Entering directory '/home/egitaristorandas/earnsai-pulse-trading'
python3 -c "from earnsai.evaluation.journal_analytics import write_all_journal_analytics; print(write_all_journal_analytics())"
{'ok': True, 'json_path': 'reports/phase8b_journal_analytics.json', 'markdown_path': 'reports/phase8b_journal_analytics.md', 'total_rows': 500, 'rates_pct': {'approved_paper_pct': 72.2, 'rejected_pct': 27.8, 'blocked_pct': 0.0, 'hold_pct': 27.8, 'buy_pct': 50.2, 'sell_pct': 22.0}}
make[2]: Leaving directory '/home/egitaristorandas/earnsai-pulse-trading'
make fixture-report
make[2]: Entering directory '/home/egitaristorandas/earnsai-pulse-trading'
python3 -c "from earnsai.evaluation.fixture_runner import write_all_fixture_reports; print(write_all_fixture_reports())"
{'ok': True, 'json_path': 'reports/phase8c_fixture_report.json', 'markdown_path': 'reports/phase8c_fixture_report.md', 'summary': {'total': 4, 'passed': 4, 'failed': 0, 'final_actions': {'bullish': 'BUY', 'bearish': 'SELL', 'flat': 'HOLD', 'volatile': 'BUY'}, 'risk_statuses': {'bullish': 'APPROVED_FOR_PAPER_ONLY', 'bearish': 'APPROVED_FOR_PAPER_ONLY', 'flat': 'REJECTED', 'volatile': 'APPROVED_FOR_PAPER_ONLY'}}}
make[2]: Leaving directory '/home/egitaristorandas/earnsai-pulse-trading'
make backtest-adapter-report
make[2]: Entering directory '/home/egitaristorandas/earnsai-pulse-trading'
python3 -c "from earnsai.backtest.adapter import write_all_backtest_adapter_reports; print(write_all_backtest_adapter_reports())"
{'ok': True, 'json_path': 'reports/phase8d_backtest_adapter_plan.json', 'markdown_path': 'reports/phase8d_backtest_adapter_plan.md', 'summary': {'plan_valid': True, 'total_scenarios': 4, 'passed': 4, 'failed': 0}}
make[2]: Leaving directory '/home/egitaristorandas/earnsai-pulse-trading'
make stability-report
make[2]: Entering directory '/home/egitaristorandas/earnsai-pulse-trading'
python3 -c "from earnsai.evaluation.stability import write_stability_report; print(write_stability_report())"
{'ok': True, 'path': 'reports/phase8f_stability_report.md', 'report': {'ok': True, 'checks': {'unknown_command_blocked': {'ok': True, 'response': {'ok': False, 'command': '/definitely_unknown_command', 'blocked': True, 'message': 'Unknown or unsafe command. Use /help.'}}, 'trading_commands_blocked': {'ok': True, 'results': {'/buy': {'ok_false': True, 'blocked_true': True, 'message': 'BLOCKED: /buy is not allowed. Paper/dry-run monitoring only.'}, '/sell': {'ok_false': True, 'blocked_true': True, 'message': 'BLOCKED: /sell is not allowed. Paper/dry-run monitoring only.'}, '/live_on': {'ok_false': True, 'blocked_true': True, 'message': 'BLOCKED: /live_on is not allowed. Paper/dry-run monitoring only.'}, '/unlock_live': {'ok_false': True, 'blocked_true': True, 'message': 'BLOCKED: /unlock_live is not allowed. Paper/dry-run monitoring only.'}, '/show_env': {'ok_false': True, 'blocked_true': True, 'message': 'BLOCKED: /show_env is not allowed. Paper/dry-run monitoring only.'}, '/set_secret': {'ok_false': True, 'blocked_true': True, 'message': 'BLOCKED: /set_secret is not allowed. Paper/dry-run monitoring only.'}, '/trade': {'ok_false': True, 'blocked_true': True, 'message': 'BLOCKED: /trade is not allowed. Paper/dry-run monitoring only.'}, '/market_order': {'ok_false': True, 'blocked_true': True, 'message': 'BLOCKED: /market_order is not allowed. Paper/dry-run monitoring only.'}}}, 'missing_freqtrade_signal_fallback': {'ok': True, 'fallback': {'exists': False, 'path': 'freqtrade_user_data/signals/latest_signal.json', 'action': 'HOLD', 'risk_status': 'BLOCKED', 'mode': 'PAPER_ONLY', 'live_trading_locked': True}}, 'bridge_recovers_after_hold_signal': {'ok': True, 'status': {'mode': 'PAPER_ONLY', 'live_trading_locked': True, 'latest_signal_exists': True, 'freqtrade_signal_exists': True, 'journal_exists': True, 'latest_signal_id': 'feb9f9d4-8ba3-4f0a-8b99-2887f6bc8fa9', 'freqtrade_signal_id': 'feb9f9d4-8ba3-4f0a-8b99-2887f6bc8fa9', 'signals_match': True, 'latest_action': 'HOLD', 'freqtrade_action': 'HOLD', 'latest_risk_status': 'REJECTED', 'freqtrade_risk_status': 'REJECTED'}}, 'corrupted_temp_signal_detection': {'ok': True, 'path': 'runtime/corrupted_signal_test.json', 'parsed': False}}}}
make[2]: Leaving directory '/home/egitaristorandas/earnsai-pulse-trading'
make[1]: Leaving directory '/home/egitaristorandas/earnsai-pulse-trading'
```

### phase9a_gate

```text
make[1]: Entering directory '/home/egitaristorandas/earnsai-pulse-trading'
python3 -m py_compile scripts/doctor.py scripts/security_scan.py scripts/phase9a_smoke.py earnsai/data/provider.py earnsai/data/local_fixture_provider.py earnsai/data/provider_runner.py
python3 scripts/security_scan.py
SECURITY_SCAN PASS
python3 scripts/doctor.py
DOCTOR PASS python=3.12.3 root=/home/egitaristorandas/earnsai-pulse-trading
python3 scripts/phase9a_smoke.py
PHASE9A_SMOKE PASS scenarios=4 bullish=BUY bearish=SELL flat=HOLD volatile=BUY
make[1]: Leaving directory '/home/egitaristorandas/earnsai-pulse-trading'
```

### phase9b_gate

```text
make[1]: Entering directory '/home/egitaristorandas/earnsai-pulse-trading'
python3 -m py_compile scripts/doctor.py scripts/security_scan.py scripts/phase9a_smoke.py scripts/phase9b_smoke.py earnsai/data/provider.py earnsai/data/local_fixture_provider.py earnsai/data/provider_runner.py earnsai/evaluation/journal_control.py
python3 scripts/security_scan.py
SECURITY_SCAN PASS
python3 scripts/doctor.py
DOCTOR PASS python=3.12.3 root=/home/egitaristorandas/earnsai-pulse-trading
python3 scripts/phase9a_smoke.py
PHASE9A_SMOKE PASS scenarios=4 bullish=BUY bearish=SELL flat=HOLD volatile=BUY
python3 scripts/phase9b_smoke.py
PHASE9B_SMOKE PASS main_before=8116 main_after=8116 isolated_rows=2 report=reports/phase9b_journal_noise_report.md
make[1]: Leaving directory '/home/egitaristorandas/earnsai-pulse-trading'
```

### phase9c_gate

```text
make[1]: Entering directory '/home/egitaristorandas/earnsai-pulse-trading'
python3 -m py_compile scripts/doctor.py scripts/security_scan.py scripts/phase9a_smoke.py scripts/phase9b_smoke.py scripts/phase9c_smoke.py earnsai/data/provider.py earnsai/data/local_fixture_provider.py earnsai/data/provider_runner.py earnsai/evaluation/journal_control.py earnsai/evaluation/compact_report.py
python3 scripts/security_scan.py
SECURITY_SCAN PASS
python3 scripts/doctor.py
DOCTOR PASS python=3.12.3 root=/home/egitaristorandas/earnsai-pulse-trading
python3 scripts/phase9a_smoke.py
PHASE9A_SMOKE PASS scenarios=4 bullish=BUY bearish=SELL flat=HOLD volatile=BUY
python3 scripts/phase9b_smoke.py
PHASE9B_SMOKE PASS main_before=8120 main_after=8120 isolated_rows=2 report=reports/phase9b_journal_noise_report.md
python3 scripts/phase9c_smoke.py
PHASE9C_SMOKE PASS safety_ok=True latest=HOLD risk=REJECTED json=reports/phase9c_compact_report.json md=reports/phase9c_compact_report.md
make[1]: Leaving directory '/home/egitaristorandas/earnsai-pulse-trading'
```

### compact_report

```text
make[1]: Entering directory '/home/egitaristorandas/earnsai-pulse-trading'
python3 -c "from earnsai.evaluation.compact_report import write_all_compact_reports; print(write_all_compact_reports())"
{'ok': True, 'json_path': 'reports/phase9c_compact_report.json', 'markdown_path': 'reports/phase9c_compact_report.md', 'safety_ok': True, 'latest_action': 'HOLD', 'latest_risk_status': 'REJECTED'}
make[1]: Leaving directory '/home/egitaristorandas/earnsai-pulse-trading'
```

## Safety
- CI safe gate does not enable live trading.
- CI safe gate does not use private exchange API.
- CI safe gate validates paper/dry-run safety posture.
- CI safe gate is local-only.

phase7a-smoke:
	python3 scripts/phase7a_smoke.py

security-scan:
	python3 scripts/security_scan.py

show-signal:
	cat earnsai/signals/latest_signal.json

show-journal:
	tail -n 5 logs/signals.jsonl

doctor:
	python3 scripts/doctor.py

phase7a-gate:
	python3 -m py_compile scripts/doctor.py scripts/security_scan.py scripts/phase7a_smoke.py earnsai/common/config.py earnsai/signals/schema.py earnsai/risk/gate.py earnsai/journal/jsonl_store.py earnsai/agents/orchestrator.py
	python3 scripts/security_scan.py
	python3 scripts/doctor.py
	python3 scripts/phase7a_smoke.py

phase7b-smoke:
	python3 scripts/phase7b_smoke.py

phase7b-gate:
	python3 -m py_compile scripts/doctor.py scripts/security_scan.py scripts/phase7a_smoke.py scripts/phase7b_smoke.py earnsai/common/config.py earnsai/signals/schema.py earnsai/risk/gate.py earnsai/journal/jsonl_store.py earnsai/agents/orchestrator.py
	python3 scripts/security_scan.py
	python3 scripts/doctor.py
	python3 scripts/phase7a_smoke.py
	python3 scripts/phase7b_smoke.py

phase7c-smoke:
	python3 scripts/phase7c_smoke.py

phase7c-gate:
	python3 -m py_compile scripts/doctor.py scripts/security_scan.py scripts/phase7a_smoke.py scripts/phase7b_smoke.py scripts/phase7c_smoke.py earnsai/common/config.py earnsai/signals/schema.py earnsai/risk/gate.py earnsai/journal/jsonl_store.py earnsai/agents/base.py earnsai/agents/research_agent.py earnsai/agents/technical_agent.py earnsai/agents/sentiment_agent.py earnsai/agents/strategy_agent.py earnsai/agents/risk_agent.py earnsai/agents/decision_agent.py earnsai/agents/monitoring_agent.py earnsai/agents/orchestrator.py
	python3 scripts/security_scan.py
	python3 scripts/doctor.py
	python3 scripts/phase7a_smoke.py
	python3 scripts/phase7b_smoke.py
	python3 scripts/phase7c_smoke.py

phase7d-smoke:
	python3 scripts/phase7d_smoke.py

bridge-status:
	python3 -c "from earnsai.freqtrade_adapter.status_reader import print_bridge_status; print_bridge_status()"

phase7d-gate:
	python3 -m py_compile scripts/doctor.py scripts/security_scan.py scripts/phase7a_smoke.py scripts/phase7b_smoke.py scripts/phase7c_smoke.py scripts/phase7d_smoke.py earnsai/common/config.py earnsai/signals/schema.py earnsai/risk/gate.py earnsai/journal/jsonl_store.py earnsai/agents/base.py earnsai/agents/research_agent.py earnsai/agents/technical_agent.py earnsai/agents/sentiment_agent.py earnsai/agents/strategy_agent.py earnsai/agents/risk_agent.py earnsai/agents/decision_agent.py earnsai/agents/monitoring_agent.py earnsai/agents/orchestrator.py earnsai/freqtrade_adapter/signal_exporter.py earnsai/freqtrade_adapter/status_reader.py freqtrade_user_data/strategies/EarnsAIJsonSignalStrategy.py
	python3 scripts/security_scan.py
	python3 scripts/doctor.py
	python3 scripts/phase7a_smoke.py
	python3 scripts/phase7b_smoke.py
	python3 scripts/phase7c_smoke.py
	python3 scripts/phase7d_smoke.py

phase7e-smoke:
	python3 scripts/phase7e_smoke.py

telegram-dry-run:
	python3 -m earnsai.telegram.bot

daily-report:
	python3 -c "from earnsai.evaluation.reporter import generate_markdown_report; print(generate_markdown_report())"

phase7e-gate:
	python3 -m py_compile scripts/doctor.py scripts/security_scan.py scripts/phase7a_smoke.py scripts/phase7b_smoke.py scripts/phase7c_smoke.py scripts/phase7d_smoke.py scripts/phase7e_smoke.py earnsai/common/config.py earnsai/signals/schema.py earnsai/risk/gate.py earnsai/journal/jsonl_store.py earnsai/agents/base.py earnsai/agents/research_agent.py earnsai/agents/technical_agent.py earnsai/agents/sentiment_agent.py earnsai/agents/strategy_agent.py earnsai/agents/risk_agent.py earnsai/agents/decision_agent.py earnsai/agents/monitoring_agent.py earnsai/agents/orchestrator.py earnsai/freqtrade_adapter/signal_exporter.py earnsai/freqtrade_adapter/status_reader.py earnsai/telegram/handlers.py earnsai/telegram/bot.py earnsai/evaluation/reporter.py freqtrade_user_data/strategies/EarnsAIJsonSignalStrategy.py
	python3 scripts/security_scan.py
	python3 scripts/doctor.py
	python3 scripts/phase7a_smoke.py
	python3 scripts/phase7b_smoke.py
	python3 scripts/phase7c_smoke.py
	python3 scripts/phase7d_smoke.py
	python3 scripts/phase7e_smoke.py

phase7-full-gate:
	make phase7a-gate
	make phase7b-gate
	make phase7c-gate
	make phase7d-gate
	make phase7e-gate

phase8a-smoke:
	python3 scripts/phase8a_smoke.py

metrics-report:
	python3 -c "from earnsai.evaluation.metrics import write_metrics_report; print(write_metrics_report())"

phase8a-gate:
	python3 -m py_compile scripts/doctor.py scripts/security_scan.py scripts/phase8a_smoke.py earnsai/evaluation/metrics.py
	python3 scripts/security_scan.py
	python3 scripts/doctor.py
	python3 scripts/phase8a_smoke.py

phase8b-smoke:
	python3 scripts/phase8b_smoke.py

journal-analytics:
	python3 -c "from earnsai.evaluation.journal_analytics import write_all_journal_analytics; print(write_all_journal_analytics())"

phase8b-gate:
	python3 -m py_compile scripts/doctor.py scripts/security_scan.py scripts/phase8a_smoke.py scripts/phase8b_smoke.py earnsai/evaluation/metrics.py earnsai/evaluation/journal_analytics.py
	python3 scripts/security_scan.py
	python3 scripts/doctor.py
	python3 scripts/phase8a_smoke.py
	python3 scripts/phase8b_smoke.py

phase8c-smoke:
	python3 scripts/phase8c_smoke.py

fixture-report:
	python3 -c "from earnsai.evaluation.fixture_runner import write_all_fixture_reports; print(write_all_fixture_reports())"

phase8c-gate:
	python3 -m py_compile scripts/doctor.py scripts/security_scan.py scripts/phase8a_smoke.py scripts/phase8b_smoke.py scripts/phase8c_smoke.py earnsai/evaluation/metrics.py earnsai/evaluation/journal_analytics.py earnsai/data/fixtures.py earnsai/evaluation/fixture_runner.py
	python3 scripts/security_scan.py
	python3 scripts/doctor.py
	python3 scripts/phase8a_smoke.py
	python3 scripts/phase8b_smoke.py
	python3 scripts/phase8c_smoke.py

phase8d-smoke:
	python3 scripts/phase8d_smoke.py

backtest-adapter-report:
	python3 -c "from earnsai.backtest.adapter import write_all_backtest_adapter_reports; print(write_all_backtest_adapter_reports())"

phase8d-gate:
	python3 -m py_compile scripts/doctor.py scripts/security_scan.py scripts/phase8a_smoke.py scripts/phase8b_smoke.py scripts/phase8c_smoke.py scripts/phase8d_smoke.py earnsai/evaluation/metrics.py earnsai/evaluation/journal_analytics.py earnsai/data/fixtures.py earnsai/evaluation/fixture_runner.py earnsai/backtest/adapter.py
	python3 scripts/security_scan.py
	python3 scripts/doctor.py
	python3 scripts/phase8a_smoke.py
	python3 scripts/phase8b_smoke.py
	python3 scripts/phase8c_smoke.py
	python3 scripts/phase8d_smoke.py

phase8e-smoke:
	python3 scripts/phase8e_smoke.py

phase8e-gate:
	python3 -m py_compile scripts/doctor.py scripts/security_scan.py scripts/phase8a_smoke.py scripts/phase8b_smoke.py scripts/phase8c_smoke.py scripts/phase8d_smoke.py scripts/phase8e_smoke.py earnsai/evaluation/metrics.py earnsai/evaluation/journal_analytics.py earnsai/data/fixtures.py earnsai/evaluation/fixture_runner.py earnsai/backtest/adapter.py earnsai/telegram/report_commands.py earnsai/telegram/handlers.py earnsai/telegram/bot.py
	python3 scripts/security_scan.py
	python3 scripts/doctor.py
	python3 scripts/phase8a_smoke.py
	python3 scripts/phase8b_smoke.py
	python3 scripts/phase8c_smoke.py
	python3 scripts/phase8d_smoke.py
	python3 scripts/phase8e_smoke.py

telegram-report-smoke:
	python3 -m earnsai.telegram.bot

phase8f-smoke:
	python3 scripts/phase8f_smoke.py

stability-report:
	python3 -c "from earnsai.evaluation.stability import write_stability_report; print(write_stability_report())"

phase8f-gate:
	python3 -m py_compile scripts/doctor.py scripts/security_scan.py scripts/phase8a_smoke.py scripts/phase8b_smoke.py scripts/phase8c_smoke.py scripts/phase8d_smoke.py scripts/phase8e_smoke.py scripts/phase8f_smoke.py earnsai/evaluation/metrics.py earnsai/evaluation/journal_analytics.py earnsai/data/fixtures.py earnsai/evaluation/fixture_runner.py earnsai/backtest/adapter.py earnsai/telegram/report_commands.py earnsai/telegram/handlers.py earnsai/telegram/bot.py earnsai/evaluation/stability.py
	python3 scripts/security_scan.py
	python3 scripts/doctor.py
	python3 scripts/phase8a_smoke.py
	python3 scripts/phase8b_smoke.py
	python3 scripts/phase8c_smoke.py
	python3 scripts/phase8d_smoke.py
	python3 scripts/phase8e_smoke.py
	python3 scripts/phase8f_smoke.py

phase8-full-gate:
	make phase7-full-gate
	make phase8a-gate
	make phase8b-gate
	make phase8c-gate
	make phase8d-gate
	make phase8e-gate
	make phase8f-gate
	make telegram-report-smoke
	make metrics-report
	make journal-analytics
	make fixture-report
	make backtest-adapter-report
	make stability-report

phase9a-smoke:
	python3 scripts/phase9a_smoke.py

phase9a-gate:
	python3 -m py_compile scripts/doctor.py scripts/security_scan.py scripts/phase9a_smoke.py earnsai/data/provider.py earnsai/data/local_fixture_provider.py earnsai/data/provider_runner.py
	python3 scripts/security_scan.py
	python3 scripts/doctor.py
	python3 scripts/phase9a_smoke.py

phase9b-smoke:
	python3 scripts/phase9b_smoke.py

journal-noise-report:
	python3 -c "from earnsai.evaluation.journal_control import write_journal_noise_report; print(write_journal_noise_report())"

phase9b-gate:
	python3 -m py_compile scripts/doctor.py scripts/security_scan.py scripts/phase9a_smoke.py scripts/phase9b_smoke.py earnsai/data/provider.py earnsai/data/local_fixture_provider.py earnsai/data/provider_runner.py earnsai/evaluation/journal_control.py
	python3 scripts/security_scan.py
	python3 scripts/doctor.py
	python3 scripts/phase9a_smoke.py
	python3 scripts/phase9b_smoke.py

phase9c-smoke:
	python3 scripts/phase9c_smoke.py

compact-report:
	python3 -c "from earnsai.evaluation.compact_report import write_all_compact_reports; print(write_all_compact_reports())"

phase9c-gate:
	python3 -m py_compile scripts/doctor.py scripts/security_scan.py scripts/phase9a_smoke.py scripts/phase9b_smoke.py scripts/phase9c_smoke.py earnsai/data/provider.py earnsai/data/local_fixture_provider.py earnsai/data/provider_runner.py earnsai/evaluation/journal_control.py earnsai/evaluation/compact_report.py
	python3 scripts/security_scan.py
	python3 scripts/doctor.py
	python3 scripts/phase9a_smoke.py
	python3 scripts/phase9b_smoke.py
	python3 scripts/phase9c_smoke.py

ci-safe:
	python3 scripts/ci_safe_gate.py

phase9d-smoke:
	python3 scripts/phase9d_smoke.py

phase9d-gate:
	python3 -m py_compile scripts/ci_safe_gate.py scripts/phase9d_smoke.py
	python3 scripts/security_scan.py
	python3 scripts/doctor.py
	python3 scripts/phase9d_smoke.py

.PHONY: phase9e-smoke
phase9e-smoke:
	python3 scripts/phase9e_smoke.py

.PHONY: phase9e-gate
phase9e-gate: ci-safe phase9e-smoke
	@echo "PHASE9E_FULL_GATE_PASS"

.PHONY: phase9-full-gate
phase9-full-gate: ci-safe phase9a-gate phase9b-gate phase9c-gate phase9d-gate phase9e-gate
	@echo "PHASE9_FULL_GATE_PASS"

.PHONY: paper-runtime-smoke
paper-runtime-smoke:
	python3 scripts/paper_runtime_smoke.py

.PHONY: paper-runtime-once
paper-runtime-once:
	python3 -m earnsai.paper_runtime.runtime --config runtime/paper_runtime/config.json --once

.PHONY: paper-runtime
paper-runtime:
	python3 -m earnsai.paper_runtime.runtime --config runtime/paper_runtime/config.json

.PHONY: paper-runtime-tmux-start
paper-runtime-tmux-start:
	@echo "=== Start EarnsAI paper runtime tmux session ==="
	@if tmux has-session -t earnsai-paper-runtime 2>/dev/null; then \
		echo "ERROR: tmux session earnsai-paper-runtime already exists. Use make paper-runtime-tmux-status or make paper-runtime-tmux-stop first."; \
		exit 1; \
	fi
	tmux new-session -d -s earnsai-paper-runtime 'cd ~/earnsai-pulse-trading && python3 -m earnsai.paper_runtime.runtime --config runtime/paper_runtime/config.json'
	@echo "PAPER_RUNTIME_TMUX_STARTED"

.PHONY: paper-runtime-tmux-status
paper-runtime-tmux-status:
	@echo "=== EarnsAI paper runtime tmux status ==="
	@if tmux has-session -t earnsai-paper-runtime 2>/dev/null; then \
		echo "PAPER_RUNTIME_TMUX_RUNNING"; \
		tmux capture-pane -t earnsai-paper-runtime -p | tail -30; \
	else \
		echo "PAPER_RUNTIME_TMUX_NOT_RUNNING"; \
	fi

.PHONY: paper-runtime-tmux-tail
paper-runtime-tmux-tail:
	@echo "=== EarnsAI paper runtime tmux tail ==="
	@tmux capture-pane -t earnsai-paper-runtime -p | tail -80

.PHONY: paper-runtime-tmux-attach
paper-runtime-tmux-attach:
	tmux attach -t earnsai-paper-runtime

.PHONY: paper-runtime-tmux-stop
paper-runtime-tmux-stop:
	@echo "=== Stop EarnsAI paper runtime tmux session ==="
	@if tmux has-session -t earnsai-paper-runtime 2>/dev/null; then \
		tmux send-keys -t earnsai-paper-runtime C-c || true; \
		sleep 2; \
		if tmux has-session -t earnsai-paper-runtime 2>/dev/null; then \
			tmux kill-session -t earnsai-paper-runtime || true; \
		fi; \
		echo "PAPER_RUNTIME_TMUX_STOPPED"; \
	else \
		echo "PAPER_RUNTIME_TMUX_NOT_RUNNING"; \
	fi

# Phase 9E newbie-friendly paper operator targets
.PHONY: paper-status paper-report paper-readiness paper-readiness-full

paper-status:
	@echo "=== EarnsAI Paper Status ==="
	@python3 -c "from earnsai.freqtrade_adapter.status_reader import print_bridge_status; print_bridge_status()"

paper-report:
	@echo "=== EarnsAI Paper Reports ==="
	@echo ""
	@echo "--- Compact Report ---"
	@if [ -f reports/phase9c_compact_report.md ]; then cat reports/phase9c_compact_report.md; else echo "reports/phase9c_compact_report.md not found"; fi
	@echo ""
	@echo "--- CI Safe Gate Report ---"
	@if [ -f reports/phase9d_ci_safe_gate_report.md ]; then cat reports/phase9d_ci_safe_gate_report.md; else echo "reports/phase9d_ci_safe_gate_report.md not found"; fi

paper-readiness:
	@echo "=== EarnsAI Fast Paper-Only Dry-Run Readiness ==="
	@echo "Safety: no live trading, no real-money execution, no private exchange API."
	@$(MAKE) phase9e-gate
	@$(MAKE) paper-status
	@echo "PAPER_DRY_RUN_FAST_READINESS_PASS"

paper-readiness-full:
	@echo "=== EarnsAI Full Paper-Only Dry-Run Readiness ==="
	@echo "This is heavier and may regenerate tracked report/signal outputs."
	@echo "Safety: no live trading, no real-money execution, no private exchange API."
	@$(MAKE) phase9-full-gate
	@$(MAKE) paper-status
	@echo "PAPER_DRY_RUN_FULL_READINESS_PASS"

# Phase 9E generated-output cleanup targets
.PHONY: paper-clean-generated paper-readiness-clean

paper-clean-generated:
	@echo "=== Clean generated paper/readiness outputs ==="
	@git restore -- \
		earnsai/signals/latest_signal.json \
		freqtrade_user_data/signals/latest_signal.json \
		reports/phase8a_metrics_report.md \
		reports/phase8b_journal_analytics.json \
		reports/phase8b_journal_analytics.md \
		reports/phase8c_fixture_report.json \
		reports/phase9c_compact_report.json \
		reports/phase9c_compact_report.md \
		reports/phase9d_ci_safe_gate_report.md 2>/dev/null || true
	@rm -f reports/phase9e_smooth_dry_run_readiness_*.log
	@rm -f reports/phase9e_smooth_dry_run_readiness_*.md
	@echo "Generated output cleanup done."
	@git status --short

paper-readiness-clean:
	@echo "=== Paper readiness with cleanup reminder ==="
	@$(MAKE) paper-readiness
	@echo ""
	@echo "=== Cleaning generated outputs after readiness ==="
	@$(MAKE) paper-clean-generated
	@echo "PAPER_READINESS_CLEAN_DONE"


# Phase 9F Telegram control and WSL autostart targets
.PHONY: paper-control-tmux-start paper-control-tmux-status paper-control-tmux-tail paper-control-tmux-stop paper-autostart-now

paper-control-tmux-start:
	@bash scripts/start_paper_control_bot_safe.sh

paper-control-tmux-status:
	@echo "=== EarnsAI paper control bot tmux status ==="
	@if tmux has-session -t earnsai-paper-control 2>/dev/null; then \
		echo "PAPER_CONTROL_TMUX_RUNNING"; \
		tmux capture-pane -t earnsai-paper-control -p | tail -30; \
	else \
		echo "PAPER_CONTROL_TMUX_NOT_RUNNING"; \
	fi

paper-control-tmux-tail:
	@echo "=== EarnsAI paper control bot tmux tail ==="
	@tmux capture-pane -t earnsai-paper-control -p | tail -80

paper-control-tmux-stop:
	@echo "=== Stop EarnsAI paper control bot tmux session ==="
	@if tmux has-session -t earnsai-paper-control 2>/dev/null; then \
		tmux send-keys -t earnsai-paper-control C-c || true; \
		sleep 2; \
		if tmux has-session -t earnsai-paper-control 2>/dev/null; then \
			tmux kill-session -t earnsai-paper-control || true; \
		fi; \
		echo "PAPER_CONTROL_TMUX_STOPPED"; \
	else \
		echo "PAPER_CONTROL_TMUX_NOT_RUNNING"; \
	fi

paper-autostart-now:
	@bash scripts/autostart_wsl_safe.sh


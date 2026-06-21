.RECIPEPREFIX := >

.PHONY: status diagnose backup check smoke run logs checkpoint help

help:
> @echo "EarnsAI Dev Command Layer v0.1"
> @echo ""
> @echo "Available commands:"
> @echo "  make status      - show safe project status"
> @echo "  make diagnose    - run status + check"
> @echo "  make backup      - create safe source snapshot"
> @echo "  make check       - run compile/type/lint checks when available"
> @echo "  make smoke       - run smoke script when available"
> @echo "  make run         - run dev/start script when available"
> @echo "  make logs        - show redacted recent logs"
> @echo "  make checkpoint  - append local checkpoint note"

status:
> @bash scripts/dev/status.sh

diagnose:
> @bash scripts/dev/status.sh
> @bash scripts/dev/check.sh

backup:
> @bash scripts/dev/backup.sh

check:
> @bash scripts/dev/check.sh

smoke:
> @bash scripts/dev/smoke.sh

run:
> @bash scripts/dev/run.sh

logs:
> @bash scripts/dev/logs.sh

checkpoint:
> @bash scripts/dev/checkpoint.sh

.PHONY: verify-v319
verify-v319:
> @bash scripts/dev/verify-v319.sh

.PHONY: diff-v319
diff-v319:
> @bash scripts/dev/diff-v319.sh

.PHONY: research-status
research-status:
> @bash scripts/dev/research-status.sh

.PHONY: research-report
research-report:
> @bash scripts/dev/research-report.sh

.PHONY: analyze-paper
analyze-paper:
> @bash scripts/dev/analyze-paper.sh

.PHONY: inspect-backtest
inspect-backtest:
> @bash scripts/dev/inspect-backtest.sh

.PHONY: summarize-datasets
summarize-datasets:
> @bash scripts/dev/summarize-datasets.sh

.PHONY: lab-index
lab-index:
> @bash scripts/dev/lab-index.sh

.PHONY: lab-health
lab-health:
> @bash scripts/dev/lab-health.sh

.PHONY: lab-refresh
lab-refresh:
> @echo "== EarnsAI Phase 4 Lab Refresh =="
> @echo "Flow: backup -> lab-health -> lab-latest -> checkpoint"
> @echo "Mode: local/read-only verification bundle"
> @$(MAKE) backup
> @$(MAKE) lab-health
> @$(MAKE) lab-latest
> @$(MAKE) checkpoint
> @echo ""
> @echo "Lab refresh result: PASSED"

.PHONY: daily verify commands
daily:
> @$(MAKE) lab-refresh

verify:
> @$(MAKE) lab-health

commands:
> @echo "EarnsAI Dev Command Layer"
> @echo ""
> @echo "Daily:"
> @echo "  make daily          - backup -> lab-health -> checkpoint"
> @echo "  make lab-refresh    - same as daily"
> @echo ""
> @echo "Core guards:"
> @echo "  make verify-v319    - verify active bot against v3.1.9 milestone"
> @echo "  make diff-v319      - compare active bot with verified checkpoint"
> @echo "  make verify         - run full lab-health bundle"
> @echo ""
> @echo "Research Lab:"
> @echo "  make research-status"
> @echo "  make research-report"
> @echo "  make analyze-paper"
> @echo "  make inspect-backtest"
> @echo "  make summarize-datasets"
> @echo "  make lab-index"
> @echo "  make lab-health"
> @echo "  make lab-latest      - show latest report paths and summary"
> @echo "  make reports-archive - move old generated reports into .dev-archives"
> @echo "  make command-audit   - audit Makefile targets and dev scripts"
> @echo "  make phase4-status   - show executive Phase 4 status"
> @echo ""
> @echo "Safety:"
> @echo "  make backup"
> @echo "  make check"
> @echo "  make smoke"
> @echo "  make checkpoint"

.PHONY: lab-latest
lab-latest:
> @bash scripts/dev/lab-latest.sh

.PHONY: reports-archive
reports-archive:
> @bash scripts/dev/reports-archive.sh

.PHONY: state-doctor
state-doctor:
> @bash scripts/dev/state-doctor.sh

.PHONY: command-audit
command-audit:
> @bash scripts/dev/command-audit.sh

.PHONY: phase4-status
phase4-status:
> @bash scripts/dev/phase4-status.sh

.PHONY: carryover
carryover:
> @bash scripts/dev/carryover.sh

# === EarnsAI DevCtl Targets BEGIN ===
.PHONY: phase4 doctor agent-scan security-doctor
phase4:
> python3 scripts/devctl.py phase4

doctor:
> python3 scripts/devctl.py doctor

agent-scan:
> python3 scripts/devctl.py scan

security-doctor:
> python3 scripts/devctl.py security
# === EarnsAI DevCtl Targets END ===

# === EarnsAI AgentOS Targets BEGIN ===
.PHONY: agent-os-plan agent-os-smoke notion-dry-run
agent-os-plan:
> python3 scripts/agent_os_ctl.py plan

agent-os-smoke:
> python3 scripts/agent_os_ctl.py smoke

notion-dry-run:
> python3 scripts/agent_os_ctl.py notion-dry-run
# === EarnsAI AgentOS Targets END ===

# === EarnsAI Notion Schema Targets BEGIN ===
.PHONY: notion-schema notion-guard-check agent-os-next
notion-schema:
> python3 scripts/notion_schema_ctl.py schema

notion-guard-check:
> python3 scripts/notion_schema_ctl.py guard-check

agent-os-next:
> make phase4
> make agent-os-plan
> make agent-os-smoke
> make notion-dry-run
> make notion-schema
> make notion-guard-check
# === EarnsAI Notion Schema Targets END ===

# === EarnsAI Notion Env Targets BEGIN ===
.PHONY: notion-setup-guide notion-env-template notion-env-check notion-id-map notion-preflight
notion-setup-guide:
> cat agent_os/notion/workspace_setup.md

notion-env-template:
> cat .env.notion.template

notion-env-check:
> python3 scripts/notion_env_ctl.py env-check

notion-id-map:
> python3 scripts/notion_env_ctl.py id-map

notion-preflight:
> make phase4
> make notion-schema
> make notion-guard-check
> python3 scripts/notion_env_ctl.py preflight
# === EarnsAI Notion Env Targets END ===

# === EarnsAI Notion Minimal Targets BEGIN ===
.PHONY: notion-read-check notion-append-dry-run notion-minimal-gate
notion-read-check:
> python3 scripts/notion_minimal_ctl.py read-check

notion-append-dry-run:
> python3 scripts/notion_minimal_ctl.py append-dry-run

notion-minimal-gate:
> make phase4
> make notion-preflight
> make notion-read-check
> make notion-append-dry-run
# === EarnsAI Notion Minimal Targets END ===

# === EarnsAI Notion Guarded Write Targets BEGIN ===
.PHONY: notion-append-guarded notion-write-gate
notion-append-guarded:
> make phase4
> make notion-minimal-gate
> python3 scripts/notion_write_ctl.py append-once --approved-once

notion-write-gate:
> make notion-append-guarded
# === EarnsAI Notion Guarded Write Targets END ===

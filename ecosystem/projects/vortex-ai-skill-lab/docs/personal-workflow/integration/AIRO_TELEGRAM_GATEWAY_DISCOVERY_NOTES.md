# AIRO Telegram Gateway Discovery Notes

Generated: 2026-05-09 13:29:27 UTC

Status:
READ-ONLY DISCOVERY SNAPSHOT

## Purpose

Capture tracked, non-secret repo signals relevant to Option A single-front-door routing.

This file does not contain tokens, secrets, .env contents, runtime state, or browser/session data.

## Tracked Candidate Files

- airo_personal_workflow/README.md
- airo_personal_workflow/__init__.py
- airo_personal_workflow/adapters/__init__.py
- airo_personal_workflow/adapters/google/__init__.py
- airo_personal_workflow/adapters/google/calendar_adapter.py
- airo_personal_workflow/adapters/google/docs_adapter.py
- airo_personal_workflow/adapters/google/drive_adapter.py
- airo_personal_workflow/adapters/google/sheets_adapter.py
- airo_personal_workflow/adapters/google/workspace_dry_run.py
- airo_personal_workflow/cli.py
- airo_personal_workflow/core/__init__.py
- airo_personal_workflow/core/config.py
- airo_personal_workflow/db/__init__.py
- airo_personal_workflow/db/init_db.py
- airo_personal_workflow/db/repository.py
- airo_personal_workflow/db/schema.sql
- airo_personal_workflow/exports/exporter.py
- airo_personal_workflow/gateway.py
- airo_personal_workflow/intents/__init__.py
- airo_personal_workflow/intents/parser.py
- airo_personal_workflow/policies/policy.yaml
- airo_personal_workflow/reports/__init__.py
- airo_personal_workflow/reports/monthly.py
- airo_personal_workflow/telegram/__init__.py
- airo_personal_workflow/telegram/local_handler.py
- config/personal-workflow/google.local.example.json
- docs/personal-workflow/AIRO_CHAT_RULES.md
- docs/personal-workflow/AIRO_CONTINUITY_PACK.md
- docs/personal-workflow/AIRO_NEW_CHAT_BOOTSTRAP_TEMPLATE.md
- docs/personal-workflow/AIRO_PERSONAL_WORKFLOW_MVP_V0_1_DONE.md
- docs/personal-workflow/AIRO_PROJECT_INDEX.md
- docs/personal-workflow/PROJECT_PROGRESS_LOG.md
- docs/personal-workflow/README.md
- docs/personal-workflow/architecture/TARGET_ARCHITECTURE.md
- docs/personal-workflow/data-model/DATA_MODEL.md
- docs/personal-workflow/decisions/DECISION_LOG.md
- docs/personal-workflow/google-workspace/GOOGLE_WORKSPACE_PLAN.md
- docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_2_HANDOFF.md
- docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_3_HANDOFF.md
- docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_4_HANDOFF.md
- docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_5_HANDOFF.md
- docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_6_HANDOFF.md
- docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_7_HANDOFF.md
- docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_8_HANDOFF.md
- docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_V0_1_HANDOFF.md
- docs/personal-workflow/integration/AIRO_INTEGRATION_CONTRACT.md
- docs/personal-workflow/integration/AIRO_TELEGRAM_NOTION_OPENCLAW_COLLISION_GUARDRAIL.md
- docs/personal-workflow/integration/PHASE_1M_OPENCLAW_GLOBAL_COMMAND.md
- docs/personal-workflow/integration/PHASE_1N_RUNTIME_VISIBILITY_CHECK.md
- docs/personal-workflow/integration/PHASE_1N_SYSTEMD_JSON_VISIBILITY_FIX.md
- docs/personal-workflow/phase-2/AIRO_PHASE_2A_HEALTH_CHECK.md
- docs/personal-workflow/phase-2/AIRO_PHASE_2B1_OPENCLAW_ROUTING_PATCH_PROPOSAL.md
- docs/personal-workflow/phase-2/AIRO_PHASE_2B2_OPENCLAW_ROUTING_PATCH_APPLY_LOG.md
- docs/personal-workflow/phase-2/AIRO_PHASE_2B_ROUTING_CONTRACT.md
- docs/personal-workflow/phase-2/AIRO_PHASE_2C_SQLITE_RECONCILE.md
- docs/personal-workflow/phase-2/AIRO_PHASE_2E_GOOGLE_SHEETS_APPROVAL_GATE.md
- docs/personal-workflow/phase-2/AIRO_PHASE_2F_ATTACHMENT_INTAKE.md
- docs/personal-workflow/phase-2/AIRO_PHASE_2G_LOCAL_DASHBOARD_APPROVAL_QUEUE.md
- docs/personal-workflow/phase-3/AIRO_PHASE_3A_STABILIZATION.md
- docs/personal-workflow/phase-3/AIRO_PHASE_3C_FIRST_GOOGLE_SHEETS_WRITE.md
- docs/personal-workflow/phase-3/AIRO_PHASE_3D_APPROVAL_QUEUE_INTEGRATION.md
- docs/personal-workflow/phase-3/AIRO_PHASE_3E_RECEIPT_TO_TRANSACTION_REVIEW.md
- docs/personal-workflow/phase-3/AIRO_PHASE_3F_LOCAL_DASHBOARD_USABILITY.md
- docs/personal-workflow/phase-3/AIRO_PHASE_3_ROADMAP.md
- docs/personal-workflow/phase-4/AIRO_PHASE_4A_STABILIZATION_COMMAND_INVENTORY.md
- docs/personal-workflow/phase-4/AIRO_PHASE_4B_UNIFIED_LOCAL_COMMAND_WRAPPER.md
- docs/personal-workflow/phase-4/AIRO_PHASE_4C_APPROVAL_QUEUE_EXECUTOR.md
- docs/personal-workflow/phase-4/AIRO_PHASE_4D_GOOGLE_SHEETS_SYNC_RELIABILITY.md
- docs/personal-workflow/phase-4/AIRO_PHASE_4E_DASHBOARD_OPERATIONS_VIEW.md
- docs/personal-workflow/phase-4/AIRO_PHASE_4F_OPENCLAW_QUEUE_FIRST_INSTRUCTION_UPDATE.md
- docs/personal-workflow/phase-4/AIRO_PHASE_4_ROADMAP.md
- docs/personal-workflow/phase-5/AIRO_PHASE_5A_LIVE_STATE_REVIEW.md
- docs/personal-workflow/phase-5/AIRO_PHASE_5B_APPROVED_GOOGLE_SHEETS_QUEUE_EXECUTION.md
- docs/personal-workflow/phase-5/AIRO_PHASE_5C_RECEIPT_TRANSACTION_PROPOSAL.md
- docs/personal-workflow/phase-5/AIRO_PHASE_5D_APPROVED_TRANSACTION_WRITE_EXECUTOR.md
- docs/personal-workflow/phase-5/AIRO_PHASE_5E_DASHBOARD_DAILY_OPS_POLISH.md
- docs/personal-workflow/phase-5/AIRO_PHASE_5F_GOOGLE_API_FALLBACK_STRATEGY.md
- docs/personal-workflow/phase-5/AIRO_PHASE_5_ROADMAP.md
- docs/personal-workflow/phase-6/AIRO_PHASE_6A_SEAMLESS_READINESS_REVIEW.md
- docs/personal-workflow/phase-6/AIRO_PHASE_6B_LOCAL_INTENT_ROUTER.md
- docs/personal-workflow/phase-6/AIRO_PHASE_6C_APPROVAL_REVIEW_CLI.md
- docs/personal-workflow/phase-6/AIRO_PHASE_6D_EXECUTOR_COMMAND_RECOMMENDATION.md
- docs/personal-workflow/phase-6/AIRO_PHASE_6E_DASHBOARD_NEXT_ACTION_UPGRADE.md
- docs/personal-workflow/phase-6/AIRO_PHASE_6F_OPENCLAW_UNIFIED_ROUTER_INSTRUCTION_UPDATE.md
- docs/personal-workflow/phase-6/AIRO_PHASE_6_ROADMAP.md
- docs/personal-workflow/phase-7/AIRO_PHASE_7A_DAILY_LOOP_READINESS_REVIEW.md
- docs/personal-workflow/phase-7/AIRO_PHASE_7B_UNIFIED_DAILY_COMMAND.md
- docs/personal-workflow/phase-7/AIRO_PHASE_7C_ROUTER_PREVIEW_INTEGRATION.md
- docs/personal-workflow/phase-7/AIRO_PHASE_7D_APPROVAL_REVIEW_UX_POLISH.md
- docs/personal-workflow/phase-7/AIRO_PHASE_7E_DASHBOARD_DAILY_COMMAND_ALIGNMENT.md
- docs/personal-workflow/phase-7/AIRO_PHASE_7_ROADMAP.md
- docs/personal-workflow/phase-8/AIRO_PHASE_8A_FINAL_SYSTEM_AUDIT.md
- docs/personal-workflow/phase-8/AIRO_PHASE_8B_BACKUP_RESTORE_GUIDE.md
- docs/personal-workflow/phase-8/AIRO_PHASE_8C_FINAL_SMOKE_TEST_SUITE.md
- docs/personal-workflow/phase-8/AIRO_PHASE_8D_FINAL_SOURCE_OF_TRUTH_REFRESH.md
- docs/personal-workflow/phase-8/AIRO_PHASE_8E_FINAL_HANDOFF_STABLE_RELEASE_TAG.md
- docs/personal-workflow/phase-8/AIRO_PHASE_8_ROADMAP.md
- docs/personal-workflow/runbooks/PHASE_1B_IMPORT_FIX.md
- docs/personal-workflow/runbooks/PHASE_1B_LOCAL_MVP.md
- docs/personal-workflow/runbooks/PHASE_1C_DB_CLI.md
- docs/personal-workflow/runbooks/PHASE_1D_EXPORT_LAYER.md
- docs/personal-workflow/runbooks/PHASE_1H_TEST_DB_ISOLATION.md
- docs/personal-workflow/runbooks/PHASE_1I_AIRO_GATEWAY.md
- docs/personal-workflow/safety/POLICY.md
- playbooks/github-handover-workflow.md
- scripts/airo_gateway_smoke.py
- scripts/airo_personal_workflow_call.sh
- scripts/personal-workflow/airo_action_gate.py
- scripts/personal-workflow/airo_approval_queue.py
- scripts/personal-workflow/airo_approval_review.py
- scripts/personal-workflow/airo_daily.py
- scripts/personal-workflow/airo_dashboard_daily_alignment.py
- scripts/personal-workflow/airo_executor_recommend.py
- scripts/personal-workflow/airo_final_smoke.py
- scripts/personal-workflow/airo_google_fallback.py
- scripts/personal-workflow/airo_google_sheets_writer.py
- scripts/personal-workflow/airo_intent_router.py
- scripts/personal-workflow/airo_local_dashboard.py
- scripts/personal-workflow/airo_ops_dashboard.py
- scripts/personal-workflow/airo_queue_executor.py
- scripts/personal-workflow/airo_receipt_intake.py
- scripts/personal-workflow/airo_receipt_review.py
- scripts/personal-workflow/airo_sheets_sync.py
- scripts/personal-workflow/airo_transaction_executor.py
- scripts/personal-workflow/airo_transaction_proposal.py
- scripts/personal-workflow/airoctl.py
- scripts/personal_workflow_db_smoke.py
- scripts/personal_workflow_export_smoke.py
- scripts/personal_workflow_google_dry_run.py
- scripts/personal_workflow_smoke.py
- scripts/personal_workflow_telegram_smoke.py

## Key Findings

- NEXT_ACTION.md identifies Bubu as the Telegram capture gateway for Notion Life OS.
- airo_personal_workflow/gateway.py routes local text to the Airo Personal Workflow Telegram local handler.
- airo_personal_workflow/telegram/local_handler.py exposes handle_telegram_text(text: str).
- scripts/personal_workflow_telegram_smoke.py verifies the local Telegram-style handler with a temporary test DB.
- No tracked Airo Personal Workflow live Telegram polling/webhook runner has been confirmed from prior audits.

## Next Discovery Need

Find the actual live Telegram gateway implementation that currently posts to Notion Life / Recent Captures.

Do not inspect token values, .env files, browser profiles, cookies, session files, or credentials during that discovery.

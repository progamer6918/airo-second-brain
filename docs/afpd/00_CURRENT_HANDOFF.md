# 00_CURRENT_HANDOFF.md

## Current Verified State
- **Apps Script Production Version**: 375
- **Source Code SHA-256**: `dde3e8cec69ef45d33e7e54a6a4e16ee07084a3016f73c7b02d6d169eee4947d`
- **Latest Known Deployment ID**: `AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA`
- **Latest Known Deployment Fingerprint**: `497865e5f3c2345b`

## Gmail Poller Window
- **Active Ingestion Business Window**: 09:00 - 00:59 WIB (Asia/Jakarta)
- **Inactive Cooldown Window**: 01:00 - 08:59 WIB (Asia/Jakarta)
- **Timezone Note**: Manifest timezone in `appsscript.json` is `Asia/Bangkok` while the script runs in `Asia/Jakarta`.

## Webhook Intake
- **Telegram Webhook Route**: Runs independently from poller, active 24/7.

## Repository State
- **Pre-existing Dirty Files**:
  - `.obsidian/app.json`
  - `.obsidian/appearance.json`
  - `.obsidian/core-plugins.json`
  - `ecosystem/projects/vortex-ai-skill-lab/apps-script-live/AIRO_Finance_Multitab_Final_v1.js` (matches v375 baseline hash)
  - `state/system-health.md`

## Current Phase and Next Gate
- **Current Phase**: AFPD Phase 3 — Traceable Content Migration
- **Next Gate**: Owner Approval for AFPD Activation and old paths deprecation.

## Gate P1 Handoff — Manual Approval Staging Repair

- **Recorded at**: 2026-07-13 19:06:42 WIB
- **Repository authority parent**: `308a7086154dbaed9c141daad04a43ba3179056b`
- **Integrated source commit**: `22caa64774977fdedcd5ae8555e3c805b20feac8`
- **Integrated source SHA-256**: `aca69b3750ce63ce2015ce416880d9b225e704166f8b030a9783623056a93b52`
- **Stable patch ID**: `1d3c4a7f0a88efc4ccce2bb22fa3d0351e3baea5`
- **Incident**: `AFPD-INC-009`
- **Repository repair status**: INTEGRATED
- **Production deployment status**: NOT DEPLOYED
- **Production runtime proof**: NOT PERFORMED
- **Workbook readback**: NOT PERFORMED
- **AFPD status**: PROPOSED_NOT_CANONICAL
- **Canonical activation**: PENDING_OWNER_APPROVAL
- **Next gate**: Owner-authorized Gate P2 deployment, Telegram runtime proof, approval commit proof, and workbook readback.
- **Do not mark incident resolved** until all Gate P2 production evidence passes.

## Gate P1.1 Handoff — self-test contract aligned

- **Recorded at**: 2026-07-13 19:17:45 WIB
- **Marker**: `AIRO_ARFIN_SELFTEST_CONTRACT_REPAIR_P1_1`
- **Integrated source commit**: `36bb37c228999efedaeb3ee305e03354f54cbf1a`
- **Source SHA-256**: `dcfc2ac0a88aadc3ee4f1b41d0ec5f3b35818eb6d388663bccb8bc7626af8f1b`
- **Built-in outgoing confirmation self-test**: PASS
- **Runtime staging implementation**: unchanged
- **Repository status**: ready for Gate P2 pre-deployment checks
- **Apps Script deployment**: NOT PERFORMED
- **Production runtime proof**: NOT PERFORMED
- **Incident**: `AFPD-INC-009` remains `REPAIR_INTEGRATED_NOT_DEPLOYED`
- **AFPD status**: `PROPOSED_NOT_CANONICAL`
- **Next gate**: Resume Owner-authorized Gate P2 deployment and runtime proof.

- 2026-07-19: Repaired Gate P1.2 self-test harness dependency alignment (`AIRO_ARFIN_SELFTEST_HARNESS_REPAIR_P1_2`). Self-test pass rate: 17/17.

## Gate P2 Rollback Confirmation
- **AFPD-INC-009**: DEPLOYMENT_ATTEMPTED_RUNTIME_PROOF_FAILED_ROLLBACK_CONFIRMED
- **APPS_SCRIPT_DEPLOYMENT**: ATTEMPTED_VERSION_378_ROLLED_BACK_TO_377
- **RUNTIME_PROOF**: FAIL
- **ROLLBACK_STATUS**: CONFIRMED_TO_VERSION_377
- **NEXT_SAFE_GATE**: GATE_P2_RUNTIME_FAILURE_ROOT_CAUSE_ANALYSIS_NO_DEPLOY
- **Marker**: `AIRO_ARFIN_GATE_P2_ROLLBACK_STATUS_AND_FAILURE_EVIDENCE`

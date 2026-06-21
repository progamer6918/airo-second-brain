# AIRO Finance — Alert Engine ADMIN_CHAT_ID Self-Register Patch

Date: 2026-05-31 WIB
Document type: Patch record
Phase: Phase 5B-3c — ADMIN_CHAT_ID self-register/readback
Status: DEPLOYED / AWAITING TELEGRAM LIVE SMOKE

## Deployment Info

- **Deployment ID**: `AKfycbyw5J5RWMoe9Vz2FDRwRInxt3J7VBGF5uWHOTKoKPNDYzgK83wqdrXU7zVP_Db0oOvCFQ`
- **Apps Script Version**: `@201`
- **Date/Time**: 2026-05-31 15:22 WIB


## Scope

This patch adds Telegram admin commands for controlled `ADMIN_CHAT_ID` management:

- `admin alerts set admin chat`
- `admin alerts admin chat status`

## Intended behavior

- `admin alerts set admin chat` stores the current Telegram chat ID into Script Properties as `ADMIN_CHAT_ID`.
- `admin alerts admin chat status` reads back whether `ADMIN_CHAT_ID` is configured and returns a masked chat ID.
- Manual `admin alerts live run once` passes the request chat ID into the live handler so controlled manual testing can target the current chat.
- Scheduled live trigger still falls back to Script Property `ADMIN_CHAT_ID`.
- Live switch remains unchanged.
- No trigger is created or deleted.
- No Gmail/email path is touched.
- No sheet tab is shown/hidden/deleted.
- No live enable is performed by this patch.

## Source files

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs`
- `tests/personal-workflow/test_airo_sprint6b_admin_chat_id_self_register_contract.py`

## Static validation

Target tests must pass before deploy:

    python3 -m pytest tests/personal-workflow/test_airo_sprint6b_admin_chat_id_self_register_contract.py tests/personal-workflow/test_airo_sprint6b_live_run_once_contract.py tests/personal-workflow/test_airo_sprint6b_guarded_live_control_layer_contract.py tests/personal-workflow/test_airo_sprint6b_live_heartbeat_observability_contract.py -q

## Live smoke after deploy

Telegram commands:

    admin alerts admin chat status
    admin alerts set admin chat
    admin alerts admin chat status
    admin alerts live status
    admin alerts live run once

Expected safe state:

- `ADMIN_CHAT_ID` configured and masked in status.
- Live switch remains `FALSE`.
- Final run once in OFF mode sends `0`.
- Trigger count unchanged.
- Gmail/email untouched.

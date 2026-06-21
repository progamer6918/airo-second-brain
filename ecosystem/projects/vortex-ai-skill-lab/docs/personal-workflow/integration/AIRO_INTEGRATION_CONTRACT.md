# Airo Personal Workflow Integration Contract

## Purpose

This document defines how OpenClaw/Airo should call the Airo Personal Workflow MVP safely.

## Stable Wrapper

```bash
scripts/airo_personal_workflow_call.sh "catat beli makan 50k pakai tokopedia credit card"
Dry-run Mode
AIRO_WORKFLOW_MODE=dry-run scripts/airo_personal_workflow_call.sh "bayar cicilan rumah 2500000"

Dry-run mode uses a temporary SQLite database and does not modify the main local database.

Real Mode
scripts/airo_personal_workflow_call.sh "catat beli makan 50k pakai tokopedia credit card"

Real mode writes to the configured SQLite source of truth.

JSON Output Contract

The wrapper must return pure JSON on stdout.

Required fields:

ok
intent
action
data
message
Safety Boundary

The gateway does not:

use OAuth
call Google API
upload to Google Drive
write Google Sheets
create Google Docs
create Google Calendar events
access Gmail
read browser cookies
read tokens
read passwords
access EarnsAI trading runtime
Supported Intents
record_transaction
record_installment_payment
check_installment
monthly_report
OpenClaw/Airo Integration Rule

OpenClaw/Airo should:

call the wrapper as a subprocess
parse stdout as JSON
send message back to Telegram or dashboard
log intent, action, and ok
never expose local DB path or internal logs to the user

# Phase 1N OpenClaw Runtime Visibility Check

## Goal

Validate that the global `airo-workflow` command is visible from normal shell and systemd user runtime context.

## Expected Command

```bash
airo-workflow "catat beli makan 50k pakai tokopedia credit card"
Dry-run Test
AIRO_WORKFLOW_MODE=dry-run airo-workflow "bayar cicilan rumah 2500000"
Integration Status

If this check passes, OpenClaw/Airo can call airo-workflow as an external command without patching OpenClaw core.

Safety

This phase does not:

restart OpenClaw
patch OpenClaw npm package
read secrets
read cookies
use Google OAuth
call Google API
touch EarnsAI runtime

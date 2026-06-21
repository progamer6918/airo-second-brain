
Phase 1M OpenClaw Global Command Integration
Goal

Expose Airo Personal Workflow MVP to OpenClaw/Airo through a stable command available in PATH.

Installed Command
airo-workflow "catat beli makan 50k pakai tokopedia credit card"
Architecture

OpenClaw/Airo
-> airo-workflow
-> ~/vortex-ai-skill-lab/scripts/airo_personal_workflow_call.sh
-> python3 -m airo_personal_workflow.gateway
-> pure JSON response

Why This Path

The OpenClaw gateway service PATH already includes ~/.local/bin, so this command can be discovered without patching the OpenClaw npm package or restarting the service.

Safety

This phase does not:

patch OpenClaw core
restart OpenClaw service
read secret files
read browser cookies
modify browser profile
touch EarnsAI runtime
use Google OAuth
call Google API
Smoke Test
AIRO_WORKFLOW_MODE=dry-run airo-workflow "bayar cicilan rumah 2500000" | python3 -m json.tool


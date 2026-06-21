# GitHub Handover Plan
Primary repo: earnsai-pulse-trading.
Purpose: make GitHub the online source of truth while WSL remains the development environment.
First push target should be earnsai-pulse-trading only.
Subprojects such as trading-research-lab and telegram-gateway should become separate repo candidates after cleanup.
OpenClaw workspace, backups, sessions, generated outputs, memory, and secret-bearing files must not be pushed directly.
Initial GitHub Action should only run python3 scripts/ci_safe_gate.py.
No GitHub secrets are required for the first CI workflow.
Remote setup and push require explicit approval after local safety gate passes.

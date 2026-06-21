# Phase 1I Airo Gateway Entry Point

## Goal

Expose Airo Personal Workflow as a simple command-line gateway that can be called by OpenClaw/Airo.

## Command

```bash
python3 -m airo_personal_workflow.gateway "catat beli makan 50k pakai tokopedia credit card" --pretty
Capabilities
record transaction
record installment payment
check installment
create monthly summary response
return JSON output
Safety
no OAuth
no Google API write
no Drive upload
no Gmail access
no token or cookie access
Integration Idea

OpenClaw/Airo can call this module as a local subprocess and send the JSON result back to Telegram or dashboard.

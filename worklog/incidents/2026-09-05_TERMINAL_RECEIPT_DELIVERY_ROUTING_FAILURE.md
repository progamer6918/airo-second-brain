# Incident Report: Terminal Receipt Delivery Routing Failure

Date: 2026-09-05

## Summary

Owner-facing terminal receipt auto-copy workflow was incorrectly treated as a clipboard infrastructure failure.

Investigation proved that clipboard transport infrastructure was already implemented and functional.

## Symptoms

- Owner expected automatic copy after terminal execution.
- Commands still required manual copy from terminal output.
- Repeated investigation focused on clipboard helper and transport layer.

## Root Cause

Execution path bypassed the canonical receipt delivery gateway.

Incorrect flow:

command
-> tee
-> terminal output
-> manual copy

Correct flow:

command
-> receipt capture
-> airo-vps-exec
-> airo-remote-clipboard
-> OSC52 Termius bridge
-> clipboard paste

## Validation Evidence

Transport canary passed:

AIRO_CLIPBOARD_CANARY=PASS
SOURCE=VPS_TERMIUS

Verified components:

- AIRO_TERMINAL_RECEIPT_DELIVERY_CONTRACT exists
- scripts/airo-clipboard-receipt exists
- scripts/airo-remote-clipboard exists
- Termius OSC52 clipboard transport works

## Prevention Rules

1. Owner-facing execution MUST use receipt gateway.
2. Do not bypass wrapper using raw tee delivery.
3. Before modifying clipboard infrastructure, verify:
   - contract exists
   - helper exists
   - transport canary status
4. Clipboard transport failure and execution routing failure must be diagnosed separately.

## Classification

INCIDENT_TYPE=WORKFLOW_ROUTING_ERROR

INFRASTRUCTURE_STATUS=PASS

FIX_REQUIRED=ENFORCE_RECEIPT_GATEWAY_USAGE

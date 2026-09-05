# AIRO Terminal Receipt Delivery Contract

AUTO_COPY_REQUIRED=true
PRIMARY_METHOD=OSC52
MANUAL_COPY=DISALLOWED
OSC52_SEND_SUCCESS_DOES_NOT_REQUIRE_READBACK=true
RECEIPT_FLOW=COMMAND -> RECEIPT -> CLIPBOARD -> PASTE

## Cross-Device Receipt Delivery Routing Policy

AIRO MUST select receipt delivery adapter based on execution environment.

Routing:

- LOCAL WSL:
  `airo-clipboard-receipt`

- VPS SSH / Termius:
  `airo-remote-clipboard` via OSC52

- Antigravity:
  AGY execution gateway receipt flow

Rules:

1. Terminal stdout MUST NOT be considered owner-facing delivery.
2. Owner-facing execution output MUST use canonical receipt flow.
3. Clipboard transport status is separate from task completion verdict.
4. Device switching MUST NOT change the evidence contract.


# Device Clipboard Adapter Registry

Purpose: let a fresh AI session on ANY device skip re-diagnosis and go
straight to the correct, already-verified auto-copy method.

Rule for AI: read this file before giving any owner-facing command that
needs output copied to clipboard. If the current device is listed below
with `VERIFIED=YES`, use its adapter directly — do not re-investigate,
do not ask the Owner which method to use, do not re-litigate whether
readback is required (see BOOT.md OSC52 exception).

If the current device is NOT listed, or the environment doesn't match
what's recorded (different terminal app, different OS), run one
environment probe, then add a new entry here after it's confirmed
working once.

---

## Termius (VPS session)

- `DEVICE_LABEL`: Termius (VPS session, ubuntu@VM-0-9-ubuntu)
- `ENVIRONMENT`: SSH session via Termius app into VPS, no tmux
- `ADAPTER`: `scripts/airo-remote-clipboard` (OSC52 direct write, non-tmux path)
- `VERIFIED`: YES
- `VERIFIED_DATE`: 2026-09-05
- `EXPECTED_RECEIPT_FIELDS`:
  - `COPIED_TO_CLIPBOARD=YES`
  - `CLIPBOARD_METHOD=OSC52_ST` or `OSC52_BEL`
  - `CLIPBOARD_READBACK=NOT_AVAILABLE` (this is SUCCESS, not failure — see BOOT.md)
  - `CLIPBOARD_CONTENT_HASH=NOT_AVAILABLE` (this is SUCCESS, not failure — see BOOT.md)
- `EVIDENCE`: Owner manually confirmed paste succeeded with live test text
  ("test dari AIRO 1788591656") using a raw OSC52 write command, no tmux,
  outside the wrapper script. Wrapper script (`airo-remote-clipboard`)
  reaches the same OSC52 write path and was patched on 2026-09-05 to stop
  requiring readback on this path.
- `NOTE`: Up to ~6 seconds of wait per command is expected (two internal
  OSC52 query timeouts that will never be answered) — this is latency,
  not a failure signal.

---

## (template — copy this block for a newly-verified device)

## <Device Label>

- `DEVICE_LABEL`:
- `ENVIRONMENT`:
- `ADAPTER`:
- `VERIFIED`: NO
- `VERIFIED_DATE`:
- `EXPECTED_RECEIPT_FIELDS`:
- `EVIDENCE`:
- `NOTE`:

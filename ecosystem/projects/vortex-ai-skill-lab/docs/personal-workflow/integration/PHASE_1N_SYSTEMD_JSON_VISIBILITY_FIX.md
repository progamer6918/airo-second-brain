# Phase 1N Systemd JSON Visibility Fix

## Goal

Validate that `airo-workflow` can run from a systemd user runtime context and produce pure JSON output.

## Result

The first systemd-run pipe test mixed systemd status text with JSON output, causing JSON parsing to fail.

The corrected validation writes command output to a temporary JSON file and parses that file.

## Integration Impact

OpenClaw service can use `airo-workflow` as a command available in PATH.

## Safety

This validation does not:
- restart OpenClaw
- patch OpenClaw core
- read secrets
- access cookies
- call Google API
- touch EarnsAI runtime

# AIRO Telegram Persistence NameError Hotfix v1.0

Status: patched.

## Bug

`persist_transaction()` called missing helpers:

- `extract_payload_value`
- `resolve_account`

Telegram commands such as `nabung 5000 ke blu` and `nabung 5rb ke blu` failed with NameError.

## Fix

The missing helpers were defined and persistence now applies AIRO Finance Language Contract v1.0.

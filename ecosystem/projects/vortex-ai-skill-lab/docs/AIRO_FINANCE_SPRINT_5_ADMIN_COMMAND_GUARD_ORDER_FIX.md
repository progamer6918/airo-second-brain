# AIRO Finance - Sprint 5 Admin Command Guard Order Fix

Date: 2026-05-26
Sprint: Sprint 5 - Dashboard Analytics
Status: ACTIVE - ORDER FIX BEFORE CLEANUP

## Why

The doPost hard guard correctly prevents `admin audit sprint5 reconciliation` from being parsed as Rp5.

However, the generic unknown `admin` safe reject must not run before known admin commands such as smoke/find commands.

## Fix

Order in doPost must be:

1. Sprint 5 reconciliation hard guard.
2. Existing known special admin command handler.
3. Unknown admin safe reject.
4. Finance parsing.

This preserves safety while keeping existing admin tooling usable for controlled cleanup.

## Cleanup target after deploy

Three Review Queue rows were created from failed route attempts:

admin audit sprint5 reconciliation

They were parsed as Rp5.

Do not approve them.

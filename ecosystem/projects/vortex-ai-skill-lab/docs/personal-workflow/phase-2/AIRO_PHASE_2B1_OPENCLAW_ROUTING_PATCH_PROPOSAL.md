# AIRO Personal Workflow Phase 2B.1 OpenClaw Routing Patch Proposal

Generated: 2026-05-08T20:06:31+07:00  
Repository: progamer6918/vortex-ai-skill-lab  
Branch: main  
Base commit: fb54446  

## Purpose

This document proposes a safe OpenClaw/Airo instruction patch for routing personal finance messages to `airo-workflow`.

This milestone is proposal-only. It does not modify OpenClaw runtime files, does not restart services, does not access browser profiles, and does not use real Google Workspace access.

## Current Routing Target

```bash
airo-workflow "<user message>"
```

For smoke testing:

```bash
AIRO_WORKFLOW_MODE=dry-run airo-workflow "<user message>"
```

## Proposed Instruction Block

The following block may be added to the OpenClaw/Airo workspace instruction file after explicit approval.

Target file:

```text
~/.openclaw/workspace/AGENTS.md
```

Proposed block:

```markdown
## Airo Personal Workflow Routing

When the user asks to record or review personal finance activity, route the message to the global command:

```bash
airo-workflow "<original user message>"
```

Use this route only for clear personal finance workflow intents, including:

- Recording a personal transaction
- Recording a credit card expense
- Recording an installment payment
- Checking installment payment progress
- Showing this month's personal finance summary
- Exporting or preparing local personal finance records through existing Airo Personal Workflow commands

Examples that should route:

```text
catat beli makan 50k pakai tokopedia credit card
bayar cicilan rumah 2500000
cek cicilan rumah sudah bayar ke berapa
ringkasan bulan ini
catat pengeluaran bensin 150 ribu pakai cash
catat beli kopi 25000 pakai kartu kredit
```

Do not route automatically when the user asks for:

- Secrets, tokens, cookies, sessions, passwords, or .env files
- Browser profile access
- Real Google OAuth
- Real Gmail, Drive, Sheets, Docs, or Calendar writes
- OpenClaw core patching
- OpenClaw service restart
- EarnsAI trading runtime access
- Live trading
- Hard deletion of finance records
- Bank login, payment execution, or real money transfer

Before any real Google Workspace write, existing SQLite mutation, systemd restart, OpenClaw runtime patch, or deletion, ask for explicit approval.

For safe testing, use:

```bash
AIRO_WORKFLOW_MODE=dry-run airo-workflow "<original user message>"
```

The command output should be treated as successful only when it returns exit code zero and valid JSON.
```

## Proposed Patch Method

After approval, apply the instruction block using a script that:

1. Creates a timestamped backup of `~/.openclaw/workspace/AGENTS.md`
2. Appends the block only if a matching heading does not already exist
3. Does not read secrets
4. Does not touch browser profiles
5. Does not restart any service

## Validation Checklist

After applying the patch, validate with:

```bash
grep -n "Airo Personal Workflow Routing" ~/.openclaw/workspace/AGENTS.md
AIRO_WORKFLOW_MODE=dry-run airo-workflow "catat beli makan 50k pakai tokopedia credit card"
```

Do not restart `openclaw-gateway.service` unless explicitly approved.

## Proposal Health Check

```
PASS - Inside git repository
PASS - Current branch is main
PASS - Phase 2B routing contract exists
PASS - Global command airo-workflow is available
PASS - OpenClaw AGENTS.md exists
PASS - OpenClaw AGENTS.md already references airo-workflow
PASS - Sample routed dry-run command returns valid JSON
```

## Decision Gate

This proposal is ready for approval if:

- Phase 2B routing contract exists
- `airo-workflow` is available
- The proposed block preserves all safety boundaries
- The sample dry-run command returns valid JSON
- No runtime or service patch has been applied yet

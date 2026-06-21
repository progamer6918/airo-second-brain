# AIRO Personal Workflow Phase 2B Routing Contract

Generated: 2026-05-08T20:05:18+07:00  
Repository: progamer6918/vortex-ai-skill-lab  
Branch: main  
Base commit: aaae9be  

## Purpose

Phase 2B defines the safe routing contract for OpenClaw/Airo personal finance messages.

This milestone does not patch OpenClaw core, does not restart services, does not access browser profiles, and does not use real Google Workspace access.

The goal is to make the routing rule explicit before any runtime integration.

## Route Target

Personal finance messages should be routed to:

```bash
airo-workflow "<user message>"
```

For safe testing, use:

```bash
AIRO_WORKFLOW_MODE=dry-run airo-workflow "<user message>"
```

## Allowed Routing Intents

OpenClaw/Airo may route a user message to `airo-workflow` when the message clearly asks to perform one of these actions:

1. Record a personal transaction
2. Record a credit card expense
3. Record an installment payment
4. Check installment payment progress
5. Generate or show this month's personal finance summary
6. Export or prepare local finance records through existing Airo Personal Workflow commands

## Example Messages That Should Route

```text
catat beli makan 50k pakai tokopedia credit card
bayar cicilan rumah 2500000
cek cicilan rumah sudah bayar ke berapa
ringkasan bulan ini
catat pengeluaran bensin 150 ribu pakai cash
catat beli kopi 25000 pakai kartu kredit
```

## Messages That Must Not Route Automatically

Messages must not be routed to `airo-workflow` when they request:

- Access to secrets, tokens, cookies, sessions, passwords, or .env files
- Browser profile access
- Real Google OAuth
- Real Gmail, Drive, Sheets, Docs, or Calendar writes
- OpenClaw core patching
- OpenClaw service restart
- EarnsAI trading runtime access
- Live trading
- Hard deletion of finance records
- Bank login, payment execution, or real money transfer

## Approval Required

The following actions require explicit approval before execution:

- Any real Google Workspace write
- Any reconciliation or mutation of existing main SQLite records
- Any OpenClaw runtime routing patch
- Any systemd service restart
- Any data deletion, even if the data looks like test data

## Output Contract

`airo-workflow` should continue returning pure JSON for OpenClaw/Airo compatibility.

The caller should treat the command as successful only when:

- Exit code is zero
- Output is valid JSON
- JSON contains a recognizable status/result structure
- No prohibited boundary is crossed

## Dry-Run Smoke Test

```
PASS - Inside git repository
PASS - Current branch is main
PASS - Global command airo-workflow is available
PASS - Expense capture intent routes to airo-workflow and returns valid JSON
PASS - Installment payment intent routes to airo-workflow and returns valid JSON
PASS - Installment status intent routes to airo-workflow and returns valid JSON
PASS - Monthly summary intent routes to airo-workflow and returns valid JSON
```

## Phase 2B Decision Gate

Phase 2B contract is PASS if:

- `airo-workflow` is visible
- dry-run route examples return valid JSON
- routing rules are documented
- safety boundaries are documented
- no OpenClaw core/runtime patch is performed yet

## Next Safe Step

After this contract is committed, the next safe milestone is to create an OpenClaw/Airo routing patch proposal.

That patch should be reviewed before applying it to any live OpenClaw instruction or runtime file.

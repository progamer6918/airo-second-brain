# AIRO Finance Live Ops Rules

This document is the persistent operating rulebook for AIRO Finance live work.

## Source of truth order

1. Terminal output from the user's WSL/repo.
2. GitHub/repo files and commit history.
3. Live Telegram and Google Sheet proof pasted by the user.
4. Chat memory is not source of truth.

If a fact is not proven by terminal output, repo files, or live proof, do not invent it. Ask for a snapshot.

## Full roadmap

- Sprint 0A — Telegram Clarification Closure
- Sprint 0B — Email Ambiguity Research & Bridge Design
- Sprint 1 — Account Ledger Hardening
- Sprint 2 — Domain Tabs Maturation
- Sprint 3 — Cash Ledger Removal
- Sprint 4 — Finance Events v1
- Sprint 5 — Dashboard / Analytics
- Sprint 6 — Dashboard Final Command Center
- Sprint 6B — Proactive Telegram Alert Engine v1
- Sprint 7 — Email Ingestion v1

## Production route

Production Telegram route must remain:

Telegram -> Cloudflare Worker async_ack -> Apps Script production deployment -> Google Sheet

Never set Telegram webhook directly to Apps Script for production unless explicitly approved for emergency diagnostic.

## Deployment strategy

Preferred strategy going forward:

- Use a fixed production Apps Script deployment target.
- Update that production deployment in-place for normal patches.
- Do not change Cloudflare Worker APPS_SCRIPT_URL for every patch.

Changing Cloudflare Worker APPS_SCRIPT_URL is allowed only when:

- The user explicitly approves it.
- It is part of rollback or emergency recovery.
- The current production target is proven stale or broken.
- Before/after, impact, and rollback plan have been explained.

## Before any patch or deploy

The assistant or agent must explain and get user approval for:

- Problem being fixed.
- Why the fix matters.
- Exact scope.
- Before/after behavior.
- Risk.
- Rollback plan.
- Whether the patch touches production route, Apps Script, Worker, Telegram, or Google Sheet.

Do not give long command blocks before the user approves the plan.

## Patch rules

Allowed:

- Small targeted patches.
- One active blocker at a time.
- Read-only audit before risky patching.
- node --check before deploy.
- Git diff review before deploy when feasible.

Not allowed without explicit approval:

- Broad refactor.
- Cleanup/delete/void rows.
- Sprint jumping.
- Changing Cloudflare Worker target.
- Direct Telegram webhook to Apps Script.
- Live Telegram spam.
- Claiming PASS without live proof.

## Apps Script and Worker rules

clasp push uploads source code but does not automatically mean production Telegram is using that code.

clasp deploy creates or updates a deployment.

Cloudflare Worker decides which Apps Script deployment production Telegram uses via APPS_SCRIPT_URL.

After any Apps Script deploy or update, always verify the production route before claiming production is updated.

## Production promotion rules

For normal patches:

1. Confirm repo is clean or expected dirty.
2. Patch only approved scope.
3. Sync canonical source to apps-script-live.
4. Run syntax check.
5. Deploy or update Apps Script.
6. Confirm production deployment mapping.
7. Record current production state in docs/AIRO_FINANCE_CURRENT_STATE.md.
8. Commit and push.
9. Run only the approved live smoke test.

## Rollback rules

Before production changes, record:

- Current production Apps Script URL.
- Current production deployment ID.
- Current Git commit.
- Known-good fallback deployment URL.
- Rollback method.

Emergency rollback may use Cloudflare Worker URL change, but only with explicit approval unless production is down.

## Live testing rules

Live tests must be minimal.

Do not run broad live test suites without approval.

For a targeted fix, use only the approved smoke commands.

Do not keep sending transactions to “see what happens.” That creates dirty rows and burns time.

## Review Queue policy

Ambiguous finance input should ask clarification first when a specific safe clarification is available.

Review Queue is for likely finance inputs that have enough data to be worth reviewing but are unsafe for final clean write.

Non-finance, admin commands, and pasted logs/transcripts should not be written to domain tabs. Transcript/log Review Queue hygiene is deferred post-project debt unless explicitly prioritized.

## Status language

Use precise status:

- Historical PASS: previously proven on a past deployment.
- Current deployment PASS: proven on the currently active production route.
- Source audit OK: source suggests expected behavior, but live proof not yet run.
- Blocked: current evidence shows failure.
- Debt: intentionally deferred, not blocking current sprint.

Never collapse these into a vague “PASS.”

## Production Apps Script V2 Cutover - 2026-05-25

The old Apps Script production project reached the 200 immutable version limit. Production was rotated to a new Apps Script V2 project.

Current production Apps Script V2:

Script ID: 17JglcgQLf9qa4TbmOyfntbX0LEPy2SKdyIIycordDamFYMs9Og5ScWZi
Deployment ID: AKfycbx4HWJNY9YOPIssAF9tn3Gx36hFkumyH0TfsuWInPr0e8aZTyrbIs4-kn_Fd-Kox_ie
Web App URL: https://script.google.com/macros/s/AKfycbx4HWJNY9YOPIssAF9tn3Gx36hFkumyH0TfsuWInPr0e8aZTyrbIs4-kn_Fd-Kox_ie/exec

Cloudflare Worker production variable:

APPS_SCRIPT_URL=https://script.google.com/macros/s/AKfycbx4HWJNY9YOPIssAF9tn3Gx36hFkumyH0TfsuWInPr0e8aZTyrbIs4-kn_Fd-Kox_ie/exec

The old Apps Script project must be kept as backup until the V2 production path remains stable.

Do not change Telegram webhook. The Worker URL remains unchanged.

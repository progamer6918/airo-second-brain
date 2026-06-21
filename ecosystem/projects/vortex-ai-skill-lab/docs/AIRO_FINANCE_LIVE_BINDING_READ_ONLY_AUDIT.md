# AIRO Finance - Live Binding Read-Only Audit

Status: READ-ONLY AUDIT
Generated at: 2026-05-24 16:01:28
Repo: `/home/egitaristorandas/vortex-ai-skill-lab`
Branch: `main`
Local HEAD: `aa2fae447873bfd5021e99d74d76698887f556e3`
Remote HEAD: `aa2fae447873bfd5021e99d74d76698887f556e3`
Worktree clean at doc generation: YES
Runtime scope: No deploy, no Apps Script write, no Google Sheet write, no smoke transaction

## 1. Purpose

This document records the first live deployment gate.

This step does not change the Google Sheet. It only verifies whether the repo has enough binding metadata to identify the live Apps Script project and candidate spreadsheet target.

## 2. Clasp Binding Candidates

| File | scriptId | rootDir | parentId | Status |
|---|---|---|---|---|
| apps-script-backups/cleanup_20260514_103240/.clasp.json | 1JVKcn7cR8K3VNDCP2vxKoJl45aS2u2O9I_TU_hWuNRRbFsuz_e6y3Uf0 |  |  | OK |
| apps-script-backups/live_before_multitab_20260514_092336/.clasp.json | 1JVKcn7cR8K3VNDCP2vxKoJl45aS2u2O9I_TU_hWuNRRbFsuz_e6y3Uf0 |  |  | OK |
| apps-script-live/.clasp.json | 1JVKcn7cR8K3VNDCP2vxKoJl45aS2u2O9I_TU_hWuNRRbFsuz_e6y3Uf0 |  |  | OK |

## 3. Apps Script Manifest Candidates

| File | timeZone | exceptionLogging | OAuth scope count | Status |
|---|---|---|---:|---|
| apps-script-backups/cleanup_20260514_103240/appsscript.json | Asia/Bangkok | STACKDRIVER | 0 | OK |
| apps-script-backups/live_before_multitab_20260514_092336/appsscript.json | Asia/Bangkok | STACKDRIVER | 0 | OK |
| apps-script-live/appsscript.json | Asia/Bangkok | STACKDRIVER | 0 | OK |

## 4. Spreadsheet ID Candidates

| Candidate |
|---|
| none found in active source/docs |

## 5. Runtime Source Signals

| Signal | Present |
|---|---:|
| Finance Events tab config | YES |
| Finance Events headers helper | YES |
| Finance Events ensure helper | YES |
| Finance Events writer | YES |
| Finance Events append alias | YES |
| Finance Events writeRouted emission wrapper | YES |
| Dashboard cash reporting formulas | YES |
| Dashboard Net Worth panel | YES |
| Dashboard Credit Card panel | YES |
| Cash Ledger compatibility flag | YES |
| Cash Ledger compatibility writer | YES |
| Gmail runtime marker absent | YES |
| Destructive deletion absent | YES |

## 6. Interpretation

This is still not proof that the live Google Sheet has changed.

This audit only proves one of these states:

- PASS: repo has enough metadata to proceed to live deploy/schema verification.
- BLOCKED: missing clasp/script/spreadsheet binding info, so live deployment must not proceed yet.

## 7. Required Next Step If PASS

Proceed to:

`LIVE_DEPLOY_AND_SCHEMA_VERIFY`

That next step may modify the Google Sheet by syncing Apps Script and creating/verifying Finance Events schema/formulas.

## 8. Required Next Step If BLOCKED

Collect or create the missing binding metadata:

- `.clasp.json`
- Apps Script project `scriptId`
- target spreadsheet ID/name
- deployment method

Do not deploy until this is resolved.

---
title: AIRO Arfin No-Test Proof 2026-06-30
status: DEPLOYMENT_SOURCE_PROVEN_BUT_RUNTIME_NOT_TESTED
source_sha256: add9d5a538e48ed8cde6049f0632cbb8318c28e7074428ccc00dae7985353b19
active_deployment_version: 112
provider_count: 6
base_head: dae53ea9ae7b92fe53308a786d8ca1af8dd06da1
generated_at: 2026-06-30T22:34:52
---

> Evidence committed to ASB. This is a no-test proof: source capability and deployment source parity are proven, but end-to-end runtime functioning is not claimed.

# AIRO Arfin No-Test Proof Report

Generated: `2026-06-30T22:28:49`

## Final Verdict

```text
ARFIN_STATIC_DEEP_SCAN=PASS_WITH_LIMITATIONS
ARFIN_CAPABILITY_IN_SOURCE=PROVEN
ARFIN_DEPLOYMENT_SOURCE_PARITY=PROVEN
ACTIVE_DEPLOYMENT_VERSION=112
SOURCE_SHA=add9d5a538e48ed8cde6049f0632cbb8318c28e7074428ccc00dae7985353b19
FULL_RUNTIME_FUNCTIONING=NOT_YET_PROVEN
FINAL_NO_TEST_VERDICT=ARFIN_DEPLOYMENT_SOURCE_PROVEN_BUT_RUNTIME_NOT_TESTED
```

## Evidence Summary

- Static scan JSON: `/tmp/airo_arfin_static_deep_scan_v2_20260630_215945.json`
- Deployment readback JSON: `/tmp/airo_arfin_runtime_source_readback_no_test_v2_20260630_222407.json`
- Docs scanned: `503`
- Apps Script functions inventoried: `695`
- Provider IDs found: `6`
- Normalizer functions found: `8`
- Deployment count: `7`
- Target deployment count for version `112`: `1`
- Source file: `AIRO_Finance_Multitab_Final_v1` / `SERVER_JS`

## SHA Parity

| Item | SHA256 |
|---|---|
| Local source | `add9d5a538e48ed8cde6049f0632cbb8318c28e7074428ccc00dae7985353b19` |
| Deployment version source | `add9d5a538e48ed8cde6049f0632cbb8318c28e7074428ccc00dae7985353b19` |
| HEAD Apps Script content | `add9d5a538e48ed8cde6049f0632cbb8318c28e7074428ccc00dae7985353b19` |

SHA match: `YES`

## Provider Inventory

1. `bca_transaction_notification`
2. `blu_transaction_notification`
3. `credit_card_purchase_notification`
4. `failed_transaction_notification`
5. `otp_security_notification`
6. `refund_reversal_notification`

## Capability Matrix

| Capability | Status | Function count evidence |
|---|---|---:|
| Telegram receive/reply route | `PROVEN_STATIC_AND_DEPLOYED_SOURCE` | 49 |
| Gmail/email/poller source | `PROVEN_STATIC_AND_DEPLOYED_SOURCE_NOT_RUNTIME` | 88 |
| Reply router / pending clarification | `PROVEN_STATIC_AND_DEPLOYED_SOURCE` | 113 |
| Transaction detection/parser | `PROVEN_STATIC_AND_DEPLOYED_SOURCE` | 84 |
| Transfer antar akun | `PROVEN_STATIC_AND_DEPLOYED_SOURCE` | 43 |
| Account Ledger domain | `PROVEN_STATIC_AND_DEPLOYED_SOURCE` | 54 |
| Credit Card domain | `PROVEN_STATIC_AND_DEPLOYED_SOURCE` | 67 |
| Cash domain | `PROVEN_STATIC_AND_DEPLOYED_SOURCE` | 19 |
| Hutang/debt domain | `PROVEN_STATIC_AND_DEPLOYED_SOURCE` | 23 |
| Aset/gold domain | `PROVEN_STATIC_AND_DEPLOYED_SOURCE` | 39 |
| Cicilan domain | `PARTIAL_STATIC_DEPLOYED_SOURCE` | 2 |
| Category/subcategory | `PROVEN_STATIC_AND_DEPLOYED_SOURCE` | 29 |
| Guardrail/fail-closed | `PROVEN_STATIC_AND_DEPLOYED_SOURCE` | 14 |

## Normalizer / Clarifier Inventory

| Normalizer | Return literals |
|---|---|
| `normalizeAssetGoldAmbiguousClarificationAnswer_` | `buy, ignore, savings, sell` |
| `normalizeCashClarificationAnswer_` | `cash_in, cash_out, cash_remaining, cash_start, manual` |
| `normalizeClarificationAccountAnswer_` | `BCA, Blu, Cash, Credit Card, manual` |
| `normalizeCreditCardClarificationAnswer_` | `cc_allocation, cc_payment, cc_purchase, manual` |
| `normalizeDebtAmbiguousClarificationAnswer_` | `debt_in, debt_payment, manual, piutang_help` |
| `normalizeDirectionClarificationAnswer_` | `balance, in, manual, out, transfer` |
| `normalizeMissingCategoryClarificationAnswer_` | `belanja, makan, manual, tagihan, transport` |
| `normalizeTransferRouteClarificationAnswer_` | `dynamic/no static return literal` |

## Runtime Limitations

```text
NO_SCRIPTS_RUN=YES
NO_GMAIL_READ=YES
NO_TELEGRAM_SEND=YES
NO_WORKBOOK_EDIT=YES
NO_END_TO_END_ROUTE_TEST=YES
FULL_RUNTIME_FUNCTIONING=NOT_YET_PROVEN
```

## Claim Boundary

Safe claim: Arfin source capability exists and the active Apps Script deployment version 112 is source-parity proven against local prod-v2 SHA.

Unsafe claim: Arfin is fully functioning end-to-end right now. That requires runtime route proof.

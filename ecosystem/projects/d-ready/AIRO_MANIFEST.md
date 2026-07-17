---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---

# AIRO Manifest — D-READY

```yaml
project_id: DREADY
display_name: D-READY
full_name: Dealer Stock Readiness Early Alert Dashboard

classification: ACTIVE
stage: PILOT_LOGIC_VALIDATION

business_domain: dealer_stock_readiness
business_owner_role: Sales
current_platform: Excel
current_platform_role: calculation_and_report_prototype
target_platform: Power_BI
macro_vba_final_architecture: CANCELLED

canonical_entrypoint: README.md
canonical_prd: D_READY_PRD_LIVING.md
current_state: CURRENT_STATE.md
next_action: NEXT_ACTION.md
decision_log: docs/decisions/D_READY_DECISION_LOG.md
pending_decisions: docs/decisions/D_READY_PENDING_DECISIONS.md

repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY

raw_workbook_committed: false
raw_presentation_committed: false
raw_pbix_committed: false
raw_business_data_committed: false
raw_chat_committed: false

owner_approval_required_for:
  - canonical_prd_promotion
  - business_rule_changes
  - calculation_changes
  - threshold_changes
  - production_power_bi_release
  - dealer_access_model

completion_evidence_required:
  - validation_log
  - commit_hash
  - push_proof
  - remote_parity
  - runtime_or_refresh_proof_when_applicable
```

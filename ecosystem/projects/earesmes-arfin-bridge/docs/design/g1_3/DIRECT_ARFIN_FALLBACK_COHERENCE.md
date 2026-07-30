# EAB G1.3 Direct Arfin Fallback Coherence

- **REQUIREMENT**: `REQ-010` (Direct Arfin fallback retained)
- **STATUS**: `DESIGN_COMPLETE`

---

## 1. Coexistence Architecture

```ini
DIRECT_ARFIN_FALLBACK=RETAIN
ARFIN_AUTHORITY=SOLE_FINANCIAL_AUTHORITY
EARESMES_LEDGER_WRITE=FORBIDDEN
```

---

## 2. Coexistence Scenarios & Fail-Closed Rules

1. **Direct Arfin Resolution Before Earesmes Reply**:
   - Owner categorizes `root_100` directly in Arfin UI while Telegram prompt `pid_101` is visible.
   - Arfin sets pending record state to `RESOLVED` and increments version (`v1 -> v2`).
   - Owner later replies to Earesmes Telegram prompt (expecting `v1`).
   - Pre-submission revalidation detects state `RESOLVED` and `v2`. Request fails closed with `409 Conflict` (`ERR_ALREADY_RESOLVED_IN_ARFIN`). Zero Review Queue or ledger effect.
2. **Direct Arfin Review Queue Approval / Rejection**:
   - Earesmes stages item `rev_staged_991` to Review Queue.
   - Owner opens direct Arfin web UI and approves or rejects `rev_staged_991`.
   - Review Queue status updates to `APPROVED` or `REJECTED`. If approved, Arfin posts transaction to Account Ledger.
3. **Earesmes Outage Fallback**:
   - If Earesmes or Hermes worker is down, Owner accesses Arfin directly to categorize and approve transactions.
   - When Earesmes resumes, fresh revalidation syncs state seamlessly. Earesmes cached display NEVER overrides current Arfin state.

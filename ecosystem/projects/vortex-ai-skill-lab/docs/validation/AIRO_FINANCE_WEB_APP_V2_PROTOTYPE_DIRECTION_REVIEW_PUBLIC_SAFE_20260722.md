# AIRO Finance Web App V2 Prototype Direction Review (Public-Safe)

- **Date:** 2026-07-22
- **Reviewer:** AIRO Sync / Owner Review
- **Prototype Status:** LOCAL_ONLY_OWNER_REFERENCE
- **Direction Decision:** ACCEPTED_WITH_FEEDBACK

---

## 1. Overview
A final-look clickable prototype for AIRO Finance Web App V2 was constructed locally using structure derived from an Owner-provided financial workbook. The prototype was evaluated as a product visual direction reference, not a production implementation.

## 2. Key Owner Feedback & Adjustments
1. **Subcategory Growth Comparison Required:**
   - Feedback: Previous-period comparison must cover both Top Category and Top Subcategory spending.
   - Action: Added Top Subcategory previous-period comparison metrics (`new`, `increase`, `decrease`, `disappeared`, `no_comparison`) to the Spending Intelligence contract.
2. **Filter Control Preservation:**
   - Feedback: Month and Year filter controls must remain separate.
   - Action: Confirmed that combined Month-Year dropdown selectors are strictly forbidden. Month (1–12) and Year (YYYY) controls are maintained separately in topbar layout.

## 3. Public-Safety & Repository Boundary
- The clickable HTML prototype containing real financial transactions and balances remains strictly `LOCAL_ONLY_OWNER_REFERENCE`.
- No raw workbook export files (`.xlsx`), actual account numbers, real transaction amounts, or person/institution names are committed to the public repository.
- Production integration of Web App V2 features will be implemented progressively in vertical slices against sanitized test fixtures and live Apps Script RPCs.

# NOS 2026 — scoring & mandatory gating model

## Answer states
Final network checklists use: **Exist Good / Exist Not Good / Not Exist / N/A**. `N/A` participates in completion but is excluded from scored denominator.

## Sheet scoring patterns reconstructed from formulas
- **Premises:** Good = +1, Exist Not Good = -1, Not Exist = 0.
- **People:** Good = 2, Exist Not Good = 1, Not Exist = 0.
- **Process:** Good = 1; non-good states are zero/negative depending on sheet implementation. H1 Process in Regular H123 explicitly scores Good=1 and Exist Not Good=0; H23 Process follows the premises-like penalty pattern in the inspected formula set.

The point is not to mix raw percentages between dimensions without respecting their sheet-specific weighting.

## Audit grade thresholds
The Result Summary table encodes:
- Bronze: 0%–59.9%
- Silver: 60%–69.9%
- Gold: 70%–89.9%
- Platinum: 90%–100%

## Completion
A dimension is `Complete` only when every indicator row has one answer state selected (Good / Not Good / Not Exist / N/A). Completeness is separate from quality grade.

## Mandatory grade ceiling
Checklist rows can be tagged `P`, `G P`, or `S G P`. When a mandatory-tagged row is in a failing state (Exist Not Good or Not Exist), helper formulas convert the tag to a grade ceiling:
- violation on `P` item → mandatory result at best **Gold**;
- violation on `G P` item → at best **Silver**;
- violation on `S G P` item → **Bronze**.
- no mandatory violation → **Platinum** mandatory result.

This is a **gate**, not merely an extra point deduction.

## Final grade
Each dimension combines audit grade and mandatory grade through an explicit matrix that effectively chooses the worse grade. Overall Result Summary then combines the dimension-level audit percentages and mandatory grades and again applies the lower-grade logic.

## Diagnostic implication
A high raw percentage can still produce a low final grade if a critical mandatory item fails. Therefore review must always separate:
1. completion;
2. audit percentage;
3. mandatory violations;
4. final grade.

## Formula caveat
Some workbook formulas are stored/parsed with indexed-sheet references (`[10]Result Summary`, `[11]H23 People`). This batch preserves the intended logic but does not assert that every blank template will recalculate cleanly in every engine.

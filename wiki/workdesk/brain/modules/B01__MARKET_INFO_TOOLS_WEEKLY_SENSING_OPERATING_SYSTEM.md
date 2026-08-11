# Market Info Tools Weekly Sensing Operating System

## What problem it solves
Static market-share/retail tables explain **what happened**. Market Info Tools adds a weekly field-sensing layer intended to capture **what is changing locally now** before/while performance moves.

## Operating loop
`observe local market -> record dealer/kecamatan/event/period/detail -> quality validation -> submit weekly -> compare with sales performance -> identify plausible drivers -> early warning / action`

## Current 11 Aug 2026 submission process
The current Sinsen workflow is transitional:
1. dealer records market information through an MD Google Form;
2. Supervisor Sales Area validates wording, completeness, and plausibility;
3. dealer submits the approved information into the AHM Market Info Tools portal;
4. dealer checks the recap after save.

The intended future state is direct portal submission after dealer capability and consistency mature. Therefore, do not hard-code the Google Form as permanent process architecture.

## Weekly discipline
- submit every week;
- no later than Friday in the running week;
- still submit on schedule when no special event is observed;
- multiple relevant events may be submitted;
- observations remain dealer-keyed even when multiple dealers cover the same kecamatan.

## Minimum decision-grade observation
A useful entry should preserve:
- dealer;
- kecamatan;
- one or more applicable event categories;
- start/end dates;
- specific narrative evidence;
- direction/change when observable;
- provenance / submission period.

## Analysis guard
A field event is a **candidate explanatory variable**, not automatically a root cause. Compare timing and performance, check competing explanations, and separate correlation from causation.

Example:
- `Kemarau` + retail up is not enough to claim kemarau caused sales growth.
- Use market info as a hypothesis/evidence layer, then compare retail/M/S, competitor, financing, activity, stock, and territory evidence.

## Relationship to existing WorkDesk methods
- **Business sensing:** provides weekly qualitative/contextual evidence.
- **PICA/PPS:** helps generate and test hypotheses after a performance problem is localized.
- **ND Plan:** strengthens market-information evidence with higher-frequency field observations.
- **Territory:** kecamatan grain makes it naturally compatible with geographic drill-down, but official Integrated-TTM dependency is not yet proven by the supplied source.

## Current feature boundaries
- explicit positive/negative issue classification: `PROPOSED_NOT_CONFIRMED`;
- full official event taxonomy: `NOT_FULLY_CAPTURED`;
- edit/delete after save: source says unavailable in demonstrated portal;
- direct portal without MD Google Form: intended future state, not yet current workflow for this Sinsen rollout;
- credentials/URLs: excluded from public ASB.

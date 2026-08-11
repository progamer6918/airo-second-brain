# Source Semantic Dossier — 11. Analisa Pricing _ FID-BA.pptx

## Source identity

- Source ID: `WD-SRC-019` (secondary identifier)
- Exact original filename: `11. Analisa Pricing _ FID-BA.pptx`
- Original folder: `Basic/Materi Internal/`
- SHA-256: `7f63c659bbbc529b7679ed7e32baff7bd5ec84e37aa226ffdff3f52ee49df471`
- Units: 16 slides
- Context/date shown: ASSDP Basic, 8 Jun 2023
- Reconstruction status in this pack: **SEMANTICALLY_REVIEWED**, with formula ambiguity explicitly preserved rather than silently corrected.

## Purpose

The deck combines two connected commercial-risk topics:

1. **Price Intelligence** — compare Honda OTR and credit package competitiveness against competitors and across finance companies.
2. **FID / BA4 bad-customer monitoring** — monitor financing-quality risk that can cause finance companies to become more selective and therefore affect Honda credit sales.

The combined logic is that sales competitiveness is not just OTR price. It includes **DP, discount, installment, credit-rate competitiveness, and financing risk/quality**.

## Part A — Price Intelligence

### Slide 3 — Objectives and pricing components
Objectives:

- Ensure Honda OTR and credit packages are competitive for each type against competitors.
- Ensure competitiveness of Honda credit packages across finance companies (`Fincoy`).
- Give consumers affordable/attractive credit packages.
- Maximize Honda sales, especially credit sales.

Explicit definitions:

- `DP Pricelist` = minimum DP printed on the pricelist.
- `Discount` = average credit discount in the MD area.
- `DP Real = DP Pricelist - Discount`.

The slide also prints formulas labelled `Rate After Discount` and `Rate Before Discount`. The rendered source visibly reads:

- `Rate After Discount = ((DP Real + Installment* Tenor)-1)/3 tahun))`
- `Rate Before Discount = ((DP PL + Installment* Tenor)-1)/3 tahun))`

**Important:** as printed, `-1` is ambiguous/dimensionally unclear. This pack deliberately does not “repair” the formula from general finance knowledge. A future corroborating source or workbook is needed before canonicalizing a corrected formula.

Visual table compares head-to-head Honda/Yamaha examples with columns: segment, type, OTR Price, DP Pricelist, Discount, DP Real, Tenor, Installment/month, DP + Installment, Rate After Discount, Rate Before Discount.

### Slide 4 — How to analyze pricing
Explicit comparison dimensions:

1. Honda vs competitor OTR for head-to-head types.
2. Honda vs competitor DP Pricelist, Discount, and DP Bayar.
3. Installment.
4. Interest Rate.

Worked example concludes that BeAT Sporty CBS OTR was competitive against Mio Gear, but its DP Real, installment, and pre-discount interest rate were less competitive; therefore the overall pricing was considered less competitive and MD/Dealer needed discussion with Fincoy.

Reusable lesson: **one competitive component does not make the full package competitive**.

### Slide 5 — MD follow-up for pricing
Minimum cadence stated: pricing analysis vs competitors **at least 1×/month**.

Follow-up categories:

1. Compare OTR, DP PL, dealer mystery-shop discount, DP paid, installments, and credit rate per type.
2. Ensure Market Data 2 pricing data is valid/up-to-date: complete OTR, DP PL, discount, DP paid, installment; update OTR/type changes; use average MD-area discount rather than min/max; validate before submission; send hardcopy scans of Honda/competitor pricelists.
3. Review with Dealer & Fincoy: ensure updated pricelist available before the 3rd when changes occur, review price competitiveness per type, and agree pricing-program/competitiveness commitments.

## Part B — FID / BA4

### Slide 7 — FID definition
Source definition:

- FID = **First Installment Default**.
- Formula: `FID = Bad Customer / Total Booking`.
- FID6 monitors customers booked in a period and their installment-payment condition for the next 6 months.
- Booking = total credit recognized by Fincoy because disbursement to Dealer has occurred.
- Common FID types stated: FID3 and FID6.

Worked FID6 example:

- April 2023 FID6 = 3%.
- Booking period example: Sep'22–Feb'23 for ADIRA & OTO; Oct'22–Mar'23 for MCF.
- Illustrative meaning: 3 bad customers from 100 bookings in the stated booking period.

Source-stated FID6 thresholds:

- ADIRA: `3%`
- OTO: `5%`
- MCF: `2%`

It also notes that FID is used by multifinance outside FIF, and describes lender-specific treatment nuances (e.g. tolerance / recording differences). These are historical/source-specific details and must not be assumed as current 2026 policies without newer evidence.

### Slide 8 — BA4 definition
Source definition:

- BA = **Bad Account**.
- Formula: `BA = Bad Customer / Total Booking`.
- BA4 monitors customers booked in a period and their payment condition over the next 4 months.
- Booking definition same general logic: credit recognized after disbursement to Dealer.
- Common type stated: BA4.

Worked example:

- April 2023 BA4 = 2%.
- Booking period = Dec 2022 (`M-5`), credit starts Jan 2023.
- Meaning: 2 bad customers from 100 Dec'22 bookings that failed payment during Jan–Apr'23.

Source-stated standard:

- BA4 threshold = `2.5%`; `< 2.5% = kondisi sehat`.
- Fincoy using BA4 in this deck: FIF.

### Slide 9 — Why FID/BA4 matters
Purpose: early identification of potential finance-company losses from bad customers during the credit period.

Source-stated causes/correlates of high FID/BA4:

- Credit customers with low SES / low purchasing power.
- High discount and low DP.
- Specific cases such as LSM / internal fraud.
- Low booking volume, commonly slow-moving types.

Impact stated: finance company becomes more selective, especially at low DP and for customer/area categories considered problematic.

Analysis method stated:

- Observe FID/BA4 trend over last 3 months.
- Compare with same period previous year.

The slide notes internal fraud can arise when aggressive marketing is not matched by collection readiness or through negative collusion between Dealer Sales People and leasing CMO. This is a risk example, not a presumption about any real Dealer/person.

### Slides 10–13 — Worked trend examples
The deck demonstrates how to interpret trend, year-on-year comparison, and series-level risk. Examples include:

- FID rising over three months, with an April point exceeding 3%.
- BA4 rising, with all-type 2023 described as less healthy above 2.5%.
- Series-level differentiation: some types remain relatively safe while a type with a rising trend above threshold needs attention.

These values are worked historical examples, not current risk status.

### Slide 14 — MD follow-up for FID/BA4
Monthly analysis required across:

- Finance Company (FIF, ADIRA, OTO, MCF).
- Pareto series (examples: all type, BeAT, Scoopy, Vario).
- Fincoy branch / Honda Dealer.

Data source note:

- FID per series per MD per Fincoy is sent by AHM.
- FID per series per Fincoy branch/Dealer is requested by MD from Fincoy.

Discussion points with Dealer/Fincoy:

1. Trend by MD area / branch / Dealer.
2. Find causes through series type, DP-layer composition, and consumer occupation segment.
3. Joint commitment to overcome high FID/BA.
4. Joint commitment to support sales programs/activities.

## Conceptual memory

1. **Price competitiveness is multi-dimensional**: OTR, DP, discount, installment, credit rate, and Fincoy package.
2. DP discount changes the consumer's real upfront burden (`DP Real`).
3. Competitive pricing must be refreshed because OTR, models, discounts, and programs change.
4. Credit quality and sales competitiveness are coupled: poor FID/BA can make Fincoy more selective and constrain sales.
5. FID/BA should be analyzed as trends and segmented, not only one total number.
6. Lender-specific definitions/thresholds can differ.

## Procedural memory

### Pricing review protocol

1. Define head-to-head type comparison.
2. Compare OTR.
3. Compare DP Pricelist / discount / DP paid/real.
4. Compare installment.
5. Compare credit rate.
6. Identify which component causes package disadvantage.
7. Validate/refresh Market Data 2 data and source pricelists.
8. Review with Dealer/Fincoy and agree countermeasures/commitments.
9. Repeat at least monthly.

### FID/BA review protocol

1. Obtain monthly FID/BA at finance-company, series, and branch/Dealer granularity.
2. Check 3-month trend.
3. Compare same period prior year.
4. Identify where bad-account risk is concentrated.
5. Decompose by series type, DP layer, consumer occupation segment, and other source-stated factors.
6. Discuss with Dealer/Fincoy.
7. Agree risk improvement and sales-support action jointly.

## Diagnostic / decision memory

- A package may be uncompetitive even when OTR is competitive if DP Real, installment, or rate is worse.
- High FID/BA can create a **credit-access feedback loop**: bad-customer risk → Fincoy selectivity → restriction at low DP/risky segments/areas → sales impact.
- Rising trend can matter even if current absolute level appears near a threshold.
- Series/branch/Dealer segmentation is needed to avoid treating a localized financing-quality problem as an MD-wide problem.

## Metric / formula library candidates

### DP Real
`DP Real = DP Pricelist - Discount`

Source: slide 3.

### FID
`FID = Bad Customer / Total Booking`

Source: slide 7.

### BA
`BA = Bad Customer / Total Booking`

Source: slide 8.

### Source-stated historical thresholds

- FID6 ADIRA 3%; OTO 5%; MCF 2% — slide 7.
- BA4 2.5%, with `<2.5%` labelled healthy — slide 8.

These are **SOURCE_HISTORICAL_2023** until current policy corroboration.

### Ambiguous printed rate formulas
Preserve source text but mark `FORMULA_UNRESOLVED`; do not operationalize until corroborated.

## Visual memory

- Pricing slide uses a side-by-side head-to-head table so competitiveness can be traced to a component rather than asserted globally.
- FID/BA examples use multi-year trend lines and series-specific charts; trend shape and comparative period are part of the reasoning.
- Follow-up slides organize action as recurring MD routines and stakeholder review, not one-off calculation.

## Relationships

- `Dealer Performance Intelligence` — Dealer/branch segmentation.
- `Pricing & Financing Logic` — primary domain.
- `Sales & Market Strategy` — price competitiveness and credit access affect sales.
- `Customer Intelligence` — SES/occupation segment and bad-customer quality.
- `Problem Solving` — move from metric symptom to segmented cause and joint action.

## Unresolved / do-not-invent register

1. Printed `Rate After/Before Discount` formulas are ambiguous as rendered; no correction is authorized yet.
2. 2023 lender thresholds/policies may be stale in 2026.
3. “LSM” meaning is not expanded in this deck; do not guess solely from this source.
4. Current Fincoy roster and current data pipeline are not established here.
5. Historical examples must not be used as current performance facts.

## Human-searchable provenance

- Price Intelligence objectives/components: `11. Analisa Pricing _ FID-BA.pptx` — slide 3.
- Pricing comparison method/example: slide 4.
- MD pricing follow-up: slide 5.
- FID definition/formula/thresholds: slide 7.
- BA4 definition/formula/threshold: slide 8.
- FID/BA causes/impact/analysis: slide 9.
- Trend/series examples: slides 10–13.
- MD FID/BA follow-up: slide 14.

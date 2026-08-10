# Metric & Formula Library — Batch 01

This file records only definitions/formulas actually supported by the four Batch-01 sources. Historical thresholds are tagged as historical; ambiguous formulas are not repaired.

## DP Real

- Business meaning: consumer real DP after average credit discount.
- Formula: `DP Real = DP Pricelist - Discount`
- Source: `11. Analisa Pricing _ FID-BA.pptx` — slide 3.
- Status: `EXPLICIT_SOURCE_FORMULA`

## FID

- Name: First Installment Default.
- Formula: `FID = Bad Customer / Total Booking`
- FID6 meaning in source: customers booked in a period whose payment condition is monitored for the next 6 months.
- Common types named: FID3 and FID6.
- Source: same file — slide 7.
- Status: `EXPLICIT_SOURCE_FORMULA`

### Historical source thresholds (2023 deck)
- ADIRA FID6: 3%.
- OTO FID6: 5%.
- MCF FID6: 2%.
- Applicability: `HISTORICAL_SOURCE_RULE — current validity not yet verified`.

## BA / BA4

- Name: Bad Account.
- Formula: `BA = Bad Customer / Total Booking`
- BA4 meaning in source: monitor payment condition of a booking cohort over the next 4 months.
- Source: same file — slide 8.
- Status: `EXPLICIT_SOURCE_FORMULA`

### Historical source threshold
- BA4 standard: 2.5%.
- Source labels `<2.5%` as healthy.
- Fincoy named in source: FIF.
- Applicability: `HISTORICAL_SOURCE_RULE — current validity not yet verified`.

## Daily Sales Growth M vs M-1

- Explicit field: Daily Sales growth comparing current month (`M`) vs previous month (`M-1`).
- Used at all-Kabupaten, Kabupaten, Dealer and series levels.
- Source: `10. Sales _ Stock Monitoring per Dealer.pptx` — slides 7, 9–10.
- Formula: **NOT EXPLICITLY DEFINED IN SOURCE.**
- Status: `METRIC_NAME_AND_COMPARISON_EXPLICIT; FORMULA_UNRESOLVED`.

## Stock Growth M vs M-1

- Explicit field: Dealer-stock growth current vs previous month.
- Source: same file — slides 7, 9–10.
- Formula: **NOT EXPLICITLY DEFINED IN SOURCE.**

## Market Share

- Explicit use: achievement monitoring under PDCA and PICA M/S analysis.
- PICA works from total M/S decline to Pareto subsegment contribution and subsegment M/S change.
- Sources: `2. ASSDP Basic - PDCA.pptx` slide 6; `12. PICA.pptx` slides 27–30.
- Formula: **NOT DEFINED IN THESE SOURCES.**

## Ambiguous rate formulas from Pricing deck

The rendered source prints:

- `Rate After Discount = ((DP Real + Installment* Tenor)-1)/3 tahun))`
- `Rate Before Discount = ((DP PL + Installment* Tenor)-1)/3 tahun))`

Source: `11. Analisa Pricing _ FID-BA.pptx` — slide 3.

Status: `FORMULA_UNRESOLVED`.

WorkDesk rule: do not calculate with these formulas until another authoritative source explains/corroborates the missing/ambiguous term.

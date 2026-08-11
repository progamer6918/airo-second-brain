# Canonical Metric / Formula Library — v0.1

Only formulas with explicit or defensible source support are canonicalized. Historical thresholds remain tagged historical.

## Commercial / financing

- `DP Real = DP Pricelist - Discount` — explicit source formula.
- `FID = Bad Customer / Total Booking` — explicit source formula. Historical 2023 lender thresholds are **not current rules**.
- `BA = Bad Customer / Total Booking` — explicit source formula. Historical BA4 2.5% threshold is **not current by default**.
- Rate Before/After Discount printed formulas remain **UNRESOLVED**.

## Market / target / demand

- `Market Share = Brand Volume / Total Market` — explicit in Advance source.
- `M/S Gap (pp) = Area M/S - Benchmark M/S`.
- `Target Honda Volume = Projected Total Market × Target M/S`.
- `Forecast = Pattern + Unexplained` — conceptual equation, not a deterministic numerical forecast formula.
- `Daily Sales = Sales / Working Days` — workbook logic; working days are period-specific input, not universally 23.
- `Required people ≈ Required Sales / Target Productivity`, rounded according to workbook logic.
- `Additional people = Required people - Current people`.
- `Activity planned sales = Activity frequency × Target sales per event`.

## Stock / Niguri workbook logic

- `End Stock = Prior End Stock + Distribution - Sales`.
- `Stock Days = End Stock / Daily Sales`.

## Customer / CRM / VE

- `Contacted Rate = Contacted / Leads` or `Contacted / Prospect` depending source-system terminology; denominator must be resolved for the current system.
- `Success Rate = Deal / Contacted`.
- `Conversion Rate = Deal / Leads`.
- `Contribution to Sales/RS = Deal / Total Sales (or Retail SSU)` with period/attribution aligned.
- `CSAT = Satisfied Customers / Total Responses × 100`, with survey-specific satisfaction threshold.
- `NPS = %Promoter - %Detractor`; source bands Promoter 9–10, Passive 7–8, Detractor 0–6.
- `Affinity × Satisfaction × Engagement` is **conceptual only**, not a production formula.

## NOS 2026

Grade bands:
- Bronze 0–59.9%
- Silver 60–69.9%
- Gold 70–89.9%
- Platinum 90–100%

Mandatory gating can cap the final grade below the raw audit-grade band.

H1 examples supported by source:
- `Warehouse capacity = Dealer Stock Days target MD / 30 × Target Daily Sales Dealer`.
- `Warehouse area (m²) = Warehouse capacity × 2.2`.
- `Minimum delivery car = ROUNDUP(Target Sales per Month / 200)`.
- PDI staffing: ≤375 avg sales/month → 1; >375 → target sales / 375, with Reshape group-centralization variants.

H23 staffing examples remain network-tier/source rules and should be resolved by the applicable NOS 2026 checklist.

## Historical-only thresholds

Historical VE targets, FID/BA thresholds, 2023 Niguri rules, 2023 NOS targets, old BTL quotas and similar dated values belong in a historical register, not in current defaults.

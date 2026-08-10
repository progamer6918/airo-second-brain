# Diagnostic Playbook — Retail / Daily Sales / Market Share Decline (Batch-01 Scope)

## Purpose

This is the first applied-intelligence asset built from the actual uploaded source files. It is intentionally limited to what the four Batch-01 sources support.

## Step 0 — Define the symptom

Capture:

- Metric: Retail / Daily Sales / Market Share.
- Period and comparison basis.
- Scope: MD / Kabupaten / Dealer / Segment / Series.
- Whether the movement is volume, growth, or share.

Do not proceed with an undefined “sales turun” statement.

## Step 1 — Validate broad performance and inventory context

Where available, review:

- Sales movement.
- Stock MD.
- Stock Dealer.
- AHM–MD in-transit.
- AHM Distribution.
- Series breakdown.

Purpose: detect whether aggregate sales movement coexists with stock/inventory-flow conditions.

Source: `10. Sales _ Stock Monitoring per Dealer.pptx` slides 4–5.

## Step 2 — Localize the contribution

Choose the path that matches the starting symptom.

### Area-led
`Main Dealer → Kabupaten → Dealer → Type/Series`

### Product-led
`Main Dealer → Segment/Type → Kabupaten → Dealer`

Use M vs M-1 sales/stock contribution where that is the available monitoring basis.

Sources: Sales & Stock slides 7, 9–10; PICA slides 6–14.

## Step 3 — Identify negative and anomalous contributors

Do not inspect only declines. PICA explicitly notes that a segment moving anomalously versus All Type can also warrant analysis.

Source: `12. PICA.pptx` slide 19.

## Step 4 — Build an evidence checklist, not a cause list

Check evidence families relevant to the localized problem:

- Market/economic/environmental conditions.
- Competitor program, stock, promotion, BTL, GC.
- Honda stock/short-stock/fulfillment.
- Honda program/activity changes.
- AHM/MD strategy execution at Dealer.
- Pricing competitiveness: OTR, DP, discount, DP Real, installment/rate.
- Financing quality: FID/BA4 trend and segmentation when credit access may matter.

The existence of any one item is not yet root cause.

## Step 5 — Root-cause quality questions

For every proposed cause, ask:

1. **What changed?**
2. **Why this product/area and not comparable others?**
3. **Is the magnitude enough to explain the gap?**
4. Does the factor occur in the same localized area/product where contribution is concentrated?
5. Is there a plausible mechanism from factor → performance effect?

Questions 1–3 are directly exemplified by PICA; 4–5 are WorkDesk synthesis of the decomposition logic.

## Step 6 — Problem Identification

Write a causal statement that includes:

- localized object (Dealer/area/series/subsegment),
- observed change,
- validated mechanism,
- supporting evidence,
- what alternative explanations were rejected or remain unresolved.

Avoid “sales turun karena market” without evidence.

## Step 7 — Corrective Action

Corrective action should counter the mechanism identified in Step 6. PICA examples demonstrate product/price/promotion counteractions against a changed competitor proposition.

For current work, exact actions must be grounded in current policy/data; historic program values from the deck are examples only.

## Step 8 — Control under PDCA

After action:

- monitor achievement against target,
- re-check sales/stock and M/S,
- verify execution,
- discuss next action,
- feed field information into the next PICA/PDCA cycle.

Source: `2. ASSDP Basic - PDCA.pptx` slides 5–8.

## Stop conditions / missing evidence

Stop and label `INSUFFICIENT_EVIDENCE` if:

- the symptom cannot be localized,
- comparison periods are inconsistent,
- stock/sales data are not comparable,
- a proposed external cause has no measurable linkage,
- the only support is a historical example being reused as if current.

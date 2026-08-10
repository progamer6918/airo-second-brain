# Source Semantic Dossier — 10. Sales _ Stock Monitoring per Dealer.pptx

## Source identity

- Source ID: `WD-SRC-018` (secondary identifier)
- Exact original filename: `10. Sales _ Stock Monitoring per Dealer.pptx`
- Original folder: `Basic/Materi Internal/`
- SHA-256: `2dbf823a1b4177c31618df0718ce1fd12b98006034036ca580bda04dd9f293b3`
- Units: 12 slides
- Context/date shown by deck: ASSDP Basic, 8 Jun 2023
- Reconstruction status in this pack: **SEMANTICALLY_REVIEWED**

## Purpose

This deck teaches a drill-down monitoring method for sales and stock. Its central structure is a three-level hierarchy:

1. **Monitoring Total MD**
2. **Monitoring per Kabupaten**
3. **Monitoring per Dealer**

The method combines daily sales movement with stock movement and then drills from aggregate performance to geographic contribution and finally to dealer/series contribution.

## Core operating model

`TOTAL MD → KABUPATEN → DEALER → SERIES`

At each level, sales/stock movement is compared between current month (`M`) and previous month (`M-1`), then the analysis is deepened using contextual information where relevant.

## Slide-by-slide semantic map

### Slide 1 — Scope
Sales & Stock Monitoring, ASSDP Basic, 8 Jun 2023.

### Slide 2 — Three-level hierarchy
Visual pyramid explicitly orders the analysis from Total MD to Kabupaten to Dealer. The narrowing shape communicates progressive drill-down from broad signal to specific contributor.

### Slide 3 — Section marker
Monitoring Total MD.

### Slide 4 — Total MD monitoring
Source states that daily market-stock monitoring at total-MD level includes:

- Stock MD.
- Stock DLR.
- All type and detail per series.
- Period from `M-1` to `M`.

Purposes:

1. Ensure balance of stock composition between MD and Dealer.
2. Ensure stock does not accumulate in AHM–MD in-transit.
3. Understand the effect of market stock and in-transit condition on sales.

Visual semantics: one multi-series time chart overlays **Sales**, **Intransit AHM-MD**, **Stock Main Dealer**, **Stock Dealer**, and **AHM Distribution**. The intended reasoning is relational: do not read sales separately from stock/in-transit/distribution.

### Slide 5 — Series breakdown
The total-MD view is broken down by series examples including BeAT Sporty, CRF150L, Vario 150, and PCX. The visual shows separate time-series charts per series, establishing that aggregate balance can hide type/series-specific conditions.

### Slide 6 — Section marker
Monitoring per Kabupaten.

### Slide 7 — Kabupaten monitoring
Source states:

- Monitor daily sales & stock (`M` vs `M-1`) per Kabupaten.
- Use it to identify which Kabupaten experiences sales increase/decrease.
- Deepen analysis with economic-driver information, growth in daily sales, and Dealer-stock growth, both all-type and per-series.

The table structure visually places all-type and specific-series sales/stock side-by-side, reinforcing the need to compare both overall and type-level contributions.

### Slide 8 — Section marker
Monitoring per Dealer.

### Slide 9 — Dealer monitoring
Source states:

- Monitor daily sales & stock (`M` vs `M-1`) per Dealer within each Kabupaten.
- This is a breakdown of the Kabupaten monitoring.
- Purpose is to deepen Kabupaten analysis through Dealer-level daily-sales growth and stock condition, at all-type and series level.

### Slide 10 — Explicit “How to Analyze” sequence
The deck gives a five-step procedure:

1. Look at total all-Kabupaten Daily Sales Growth `M` vs `M-1`, and identify whether growth is positive or negative.
2. Look at Kabupaten detail and identify Kabupaten whose daily-sales growth is **“lebih”** than total all-Kabupaten; use economic-driver information to analyze which sectors grow and why (market info, analysis by occupation, etc.).
3. Select the Kabupaten and break down which Dealer causes the positive/negative growth.
4. Select the Dealer and analyze per series which series causes the Dealer's positive/negative growth.
5. Repeat steps 1–4 for all Kabupaten with daily-sales growth `> growth total`.

Visual semantics: numbered callouts map the five instructions to rows in the Kabupaten table and then to the Dealer/series table. This is a structured drill-down, not a free-form review.

### Slides 11–12 — Closing
Motivational quote and thank-you; no substantive operational rule.

## Conceptual memory

1. Sales and stock should be monitored together.
2. Aggregate MD performance must be decomposed geographically and then by Dealer/series.
3. `M vs M-1` growth is the explicit comparison basis in this deck.
4. Stock has multiple relevant locations/states: MD, Dealer, and AHM–MD in-transit; AHM distribution is also visualized.
5. Series-level analysis is required because aggregate all-type movement can conceal specific contributors.
6. Economic-driver information is used to deepen Kabupaten analysis; the source does not say that a macro/economic observation alone proves causality.

## Procedural memory

Source-grounded monitoring sequence:

1. Read total-MD sales/stock/in-transit/distribution movement.
2. Check whether stock composition between MD and Dealer is balanced and whether in-transit is accumulating.
3. Break down aggregate view per series.
4. Compare Kabupaten sales & stock `M vs M-1`.
5. Identify Kabupaten contribution relative to total growth.
6. Add economic-driver/context information to explain candidate reasons.
7. Drill the selected Kabupaten into Dealer contribution.
8. Drill the Dealer into series contribution.
9. Repeat across qualifying Kabupaten.

## Diagnostic memory

This deck is fundamentally a **localization protocol**:

`aggregate symptom → Kabupaten contributor → Dealer contributor → Series contributor`.

It helps distinguish where the movement is concentrated before attempting corrective action. Stock movement is examined together with sales movement so that a sales change can be evaluated alongside availability/inventory conditions.

The deck does **not** provide a complete root-cause tree. It explicitly introduces economic-driver/context information and stock/sales data; other root-cause domains need other sources.

## Numerical / metric memory

Explicit fields/metrics visible in the worked tables and charts:

- Sales, current and previous period (`M`, `M-1`).
- Daily-sales growth `%` and gap.
- Dealer stock, `M`, `M-1`, growth `%`, gap.
- Stock Main Dealer.
- In-transit AHM–MD.
- AHM Distribution.
- Breakdowns: all type and series.

No universal ideal-stock ratio or threshold is stated in this deck.

## Visual / structural memory

- Pyramid on slide 2: analytic granularity narrows from MD to Kabupaten to Dealer.
- Slide 4: multiple lines/bars share a time axis to encourage cross-reading sales, distribution, stock, and in-transit.
- Slide 7: wide matrix combines Kabupaten, economic-sector descriptor, sales and stock, then series-specific subcolumns.
- Slide 10: numbered callouts make the drill-down sequence executable.

## Relationships

Directly supports:

- `Dealer Performance Intelligence` — contributor localization.
- `Demand, Forecast & Stock Planning` — stock/distribution/in-transit relationship.
- `Market & Area Intelligence` — Kabupaten and economic-driver context.
- `PICA / Problem Solving` — provides the monitoring/drill-down layer needed before root-cause identification.

## Historical/current applicability

The methodology is from 2023 training material. The conceptual drill-down remains useful unless superseded, but actual system fields, product series, geographic labels, and current monitoring cadence should be reconciled with newer operational sources.

## Explicit vs inferred

### Explicit
The three levels, stated purposes, `M vs M-1`, stock elements, series detail, and five-step “How to Analyze.”

### WorkDesk synthesis
Calling it a “localization protocol” and expressing it as `aggregate → Kabupaten → Dealer → Series` are compact formulations of the source's explicit sequence.

## Unresolved / do-not-invent register

1. “Growth lebih dari total” is preserved exactly as the deck states; the deck does not explain whether this is the only selection rule for negative/underperforming cases.
2. No formula for `%growth` or `gap` is defined on-slide, although the table fields imply standard comparisons; WorkDesk must not invent a source-specific formula without corroboration.
3. No ideal stock level, days-stock target, or in-transit threshold is defined here.
4. The example geographic/series values are training examples and not current facts.

## Human-searchable provenance

- Analysis hierarchy: `10. Sales _ Stock Monitoring per Dealer.pptx` — slide 2.
- Total MD purpose and stock/in-transit logic: slide 4.
- Series breakdown: slide 5.
- Kabupaten purpose/context: slide 7.
- Dealer purpose: slide 9.
- Five-step drill-down: slide 10.

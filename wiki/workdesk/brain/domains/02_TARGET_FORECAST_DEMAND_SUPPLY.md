# Target Forecast Demand Supply

> **Status:** canonical persistence candidate derived only from reconstructed source material. Historical examples remain historical; unresolved source conflicts remain unresolved.

## Canonical scope
- target deployment
- forecast reasoning
- Niguri
- distribution
- sales/stock/stock days
- product/series mix

## How to use this brain
- Start from the business question, then localize the problem before diagnosing.
- Resolve requested date/currentness before applying dated standards, thresholds, program rules, or examples.
- Use [[../reference/CANONICAL_DECISION_RULE_LIBRARY|Canonical Decision Rules]] and [[../reference/CANONICAL_FORMULA_LIBRARY|Canonical Formula Library]] as shared controls.
- If evidence conflicts or authority is missing, consult [[../reference/CONTRADICTION_UNRESOLVED|Unresolved Ledger]] rather than guessing.

---

## Source-derived module — Dealer Demand Forecast Operating System
_Reconstruction module: `B02` / `DEALER_DEMAND_FORECAST_OPERATING_SYSTEM.md`_

---
type: compiled-domain-knowledge
claim_class: SOURCE_SYNTHESIS_WITH_EXPLICIT_PROVENANCE
---
# Dealer–Demand–Forecast Operating System

## Satu gambar besarnya

Lima source Batch 02 membentuk satu operating loop yang lebih lengkap daripada “Dealer Review” atau “forecasting” bila berdiri sendiri:

`Market Sensing → Market/Area Potential → Target Deployment → Dealer/Sales Force Capacity → Activity Plan → Demand Forecast/Niguri → Supply/Stock → Monitor Actual → Dealer Review → Action / revised plan`

Label loop di atas adalah **WorkDesk cross-source synthesis**. Setiap komponennya berasal dari source berbeda dan tidak boleh dipresentasikan sebagai satu diagram literal AHM.

## 1. Market Sensing — cari mechanism, bukan alasan generik

Gunakan market/retail history, customer, BPS/BI/media/competitor dan field sensing untuk membentuk hypothesis. External driver baru layak dipakai kalau bisa menjelaskan **where, when, who, how much** terhadap business movement.

Source basis: WD-SRC-028 slides 2–6, 10–13, 23–25; WD-SRC-029 slides 11–14.

## 2. Market & area potential — tentukan di mana opportunity berada

Baca contribution/growth per kabupaten/kecamatan, economic driver, network coverage dan Ring/territory. Target tidak diturunkan rata ke seluruh jaringan.

Source basis: WD-SRC-027 slides 11–19; WD-SRC-056 `Map Area`, `Potensi`, `TTM`.

## 3. Target Deployment — sampai orang yang mengeksekusi

Flow source:

`Potential Market/Kab → M/S/Kab → Target Polreg & RS/Kab → Retail/Dealer → Target/Sales Force`

Saat target per dealer sudah diketahui, pertanyaan berikutnya adalah coverage, people dan activity capacity.

## 4. Forecast = feasibility check, bukan angka ramalan pasif

Forecast menggabungkan pattern + unexplained factors, lalu harus diterjemahkan ke kapasitas execution yang masih tersedia. Workbook `Target & Forecasting` membuat gap target menjadi pertanyaan kuantitatif:

- berapa current people dan productivity;
- berapa required people/productivity;
- berapa activity sudah jalan;
- berapa sisa hari/activity;
- jika original plan diteruskan, finish estimate berapa;
- bila kurang, apa final activity revision yang masuk akal.

## 5. Niguri — commitment demand/supply

Niguri mengubah market forecast menjadi contribution segment/type, Sales Plan dan supply commitment. Jangan inflate/deflate Sales Plan untuk gaming barang. Sales dan Logistics harus menggunakan angka yang konsisten.

Current schedule/policy **harus** datang dari current authority karena deck 2023 sendiri mengandung conflict timeline.

## 6. Distribution & stock — supply mengikuti opportunity dan selling capacity

Demand Management menuntut balance AHM–MD–Dealer dan stock availability terutama di potential market. Target deck mengingatkan allocation harus mempertimbangkan selling capacity jaringan.

Artinya stock bukan sekadar “berapa unit tersisa”; pertanyaan yang benar adalah:

- stock ada di **type/area/dealer yang punya demand** atau tidak;
- inbound/distribution sejalan dengan sales plan atau tidak;
- shortage terjadi sebelum loss sales atau cuma snapshot setelah sales turun;
- overstock ada karena demand miss, allocation miss, atau execution miss.

## 7. Dealer Review — diary untuk mengubah plan

Dealer Review harus membaca movement dan forecast, bukan menyiapkan deck saat ada visit. Minimal:

- market local issues;
- dealer sales/forecast;
- people/productivity;
- activity effectiveness;
- product/type movement;
- stock/indent;
- cash-credit/fincoy/program;
- competitor;
- action/control.

Management Visit Guidance menjadi **coverage checklist**, bukan checklist yang wajib ditanya 100% setiap review.

## 8. Close the loop

Kalau actual vs target/forecast menyimpang:

`validate data → localize contributor → test demand/supply/people/activity/commercial hypotheses → revise action → monitor`

PICA/PDCA dari Batch 01 menjadi corrective layer di atas operating system ini.

## Anti-hallucination guards

- Niguri “M/S tidak boleh turun” = historical source rule 2023, bukan automatic current policy.
- Niguri timeline = unresolved source conflict.
- Recovery Ratio formula = source-derived, not explicitly printed.
- TTFU sheet = empty; no framework fabricated.
- Remunerasi = external dependencies unresolved.
- Visit Do/Don't = historical/context-sensitive; current external communication authority required.

---

## Source-derived module — Batch01  Supervisory Monitoring To Corrective Action
_Reconstruction module: `B01` / `BATCH01__SUPERVISORY_MONITORING_TO_CORRECTIVE_ACTION.md`_

## Scope

This compiled module uses only these four source-grounded dossiers:

1. `2. ASSDP Basic - PDCA.pptx`
2. `10. Sales _ Stock Monitoring per Dealer.pptx`
3. `11. Analisa Pricing _ FID-BA.pptx`
4. `12. PICA.pptx`

It is an early WorkDesk module, not a complete Dealer Performance domain. It deliberately leaves forecasting formulas, Dealer Review workbook logic, demand/recovery, NOS, CRM, and current 2026 operating standards for later sources.

## The operating chain

The four sources form a coherent management chain:

`PLAN → EXECUTE & OBSERVE → LOCALIZE PERFORMANCE GAP → TEST CAUSE → CORRECT → RE-MONITOR`

More concretely:

1. **Plan** — forecast market/sales, set targets, determine strategy/activity, plan supervision.
2. **Execute & observe** — monitor sales/stock, programs, competitors, policy execution, and field conditions.
3. **Localize** — move from Total MD to Kabupaten to Dealer to Series, or from Product/Segment to Area to Dealer.
4. **Diagnose** — combine contribution analysis with evidence about market, competitor, stock, Honda programs, price/financing, etc.
5. **Causal quality check** — ask whether the explanation changed when the symptom changed, whether it explains differential behavior, and whether its magnitude is sufficient.
6. **Correct** — build PICA/countermeasure specifically against the validated mechanism.
7. **Control** — monitor the resulting achievement and market share, then continue PDCA.

This synthesis is not stated verbatim in one slide; it is a cross-source relationship supported by the four decks.

## Layer 1 — Supervisory control system

From PDCA, the Area Supervisor is expected to connect planning, execution control, performance review, and corrective action. The work is multi-cadence and multi-evidence:

- Target/plan.
- Daily sales and stock.
- Weekly/monthly achievement.
- Market share.
- Competitor programs/activities.
- Dealer Review dimensions.
- Field supervision.
- Financial-company information.

WorkDesk implication: **a Dealer problem should not be analyzed from one KPI in isolation.**

## Layer 2 — Monitoring hierarchy

Sales & Stock Monitoring supplies the primary localization structure:

`Total MD → Kabupaten → Dealer → Series`

The data basis is explicitly `M vs M-1` daily sales/stock movement. At total-MD level, Sales is read together with Stock MD, Stock Dealer, AHM–MD in-transit, and AHM Distribution. The purpose is not merely to find a red number; it is to locate where movement comes from and whether inventory flow may be relevant.

## Layer 3 — Flexible decomposition path

PICA generalizes localization into two paths:

### Area-led symptom
`Main Dealer → Kabupaten → Dealer → Type`

### Product-led symptom
`Main Dealer → Segment/Type → Kabupaten → Dealer`

This creates a WorkDesk routing rule:

- If the initial question is **“which area/dealer is causing the gap?”**, start Area→Product.
- If the initial question is **“which product/segment is causing the gap?”**, start Product→Area.

That routing is a synthesis of the two PICA funnels, not a separate AHM policy statement.

## Layer 4 — Root-cause evidence families available in Batch 01

The sources explicitly mention the following candidate evidence families:

### Market / external
- Market information.
- Commodity prices.
- Weather/natural disaster.
- Political/social/environmental conditions.
- Economic drivers.

### Competitive
- Competitor sales program.
- Competitor price/discount/DP/installment.
- Promotion / BTL / GC.
- Competitor stock.

### Honda internal/execution
- Honda sales program changes.
- Honda BTL/activity changes.
- Stock / short stock / fulfillment.
- AHM/MD strategy execution by Dealer.
- Dealer Review dimensions.

### Financing
- Fincoy package competitiveness.
- DP layer.
- FID/BA4 trend and financing quality.
- Consumer occupation/SES segmentation.

Important: these are **candidate evidence families**, not automatic causes.

## Layer 5 — Causal quality gate

The PICA deck provides a reusable quality standard that should be embedded in WorkDesk diagnostics.

Before accepting a root cause, ask:

1. **Change test** — what changed versus the comparison period?
2. **Contrast test** — if the proposed cause is broad, why did other comparable products/areas not move the same way?
3. **Magnitude test** — is the proposed factor quantitatively large enough to explain the observed gap?
4. **Mechanism test** — how does the factor logically produce the observed sales/M/S effect?
5. **Localization test** — does the cause occur where the performance contribution is actually concentrated?
6. **Actionability test** — can corrective action be linked directly to the identified mechanism?

Only tests 1–3 are directly illustrated/questioned by PICA; tests 4–6 are WorkDesk synthesis consistent with the examples and PDCA action logic.

## Layer 6 — Pricing and financing branch

Pricing/FID-BA adds a specific diagnostic branch when sales or market share may be commercially constrained.

### Price competitiveness branch

Compare head-to-head:

- OTR.
- DP Pricelist.
- Discount.
- DP Real.
- Installment.
- Credit rate.

A package can be uncompetitive even when OTR is competitive.

### Financing-quality branch

If FID/BA4 is high or worsening, financing companies may become more selective. Therefore a sales gap may reflect not only demand/price but **credit-access tightening** by product/customer/area/Dealer.

This branch must be treated with lender-specific and time-specific caution because thresholds/policies in the source are 2023 training data.

## Batch-01 diagnostic routing model

When a user asks, for example, “Retail turun, kenapa?”, WorkDesk should not jump immediately to a cause. A source-grounded sequence is:

1. Confirm exact symptom: Retail? Daily Sales? M/S? which period?
2. Read total movement and comparison basis.
3. Localize by Area/Kabupaten/Dealer/Series or Segment/Type/Area.
4. Check sales together with stock/in-transit/distribution where available.
5. Identify major negative/positive anomalies.
6. Gather evidence from market, competitor, Honda execution/program, stock, and commercial/financing branches.
7. Run causal quality questions: changed? differential? magnitude?
8. Form explicit Problem Identification.
9. Define Corrective Action that addresses the mechanism.
10. Define next action/control and re-monitor under PDCA.

## What this Batch 01 module still cannot answer safely

- Exact forecast/target-breakdown methodology.
- Demand/recovery-rate methodology.
- Niguri logic.
- Full Dealer Review workbook logic.
- Current 2026 NOS/network requirements.
- Full people/productivity/funnel logic.
- Current pricing/Fincoy thresholds or current partner rules.
- Current BTL/VE/activity standards.

Those remain intentionally unresolved until their sources are reconstructed.

## Source provenance

- Supervisory PDCA loop: `2. ASSDP Basic - PDCA.pptx` slides 2, 4–8.
- Sales/stock hierarchy and drill-down: `10. Sales _ Stock Monitoring per Dealer.pptx` slides 2, 4–5, 7, 9–10.
- Pricing/FID-BA branch: `11. Analisa Pricing _ FID-BA.pptx` slides 3–5, 7–14.
- PICA decomposition and causal-quality examples: `12. PICA.pptx` slides 4–6, 16–25, 27–30.

---

## Source-derived module — Nd Plan And Area Review Model
_Reconstruction module: `B05` / `ND_PLAN_AND_AREA_REVIEW_MODEL.md`_

## Area review is not one-dimensional

The ND Plan review template forces area review across macro-economy, market, network, people, service, digital, and sustainability.

## Required evidence stack

1. **PDRB / market driven**: top economic sectors YoY, area pareto, area concern.
2. **PDRB vs CDB comparison**: checks whether actual customer database is aligned with economic-driver sectors.
3. **Quarterly market information**: positive/negative sector facts by quarter.
4. **Business milestone**: H1/H2/H3/HC3/Development KPIs across 2019-2026/YTD.
5. **Position audit by area**: latest YTD vs prior YTD.
6. **Functional evaluations**:
   - H1: market share, 9 segment, cash/credit, EV, competitor movement.
   - H2: UE, SPR, revenue/month, sales ability, customer movement, coverage, LCR.
   - H3: Sales In/Out total/HGP/AHM Oil/Acc/Apparel and by area/product.
   - HC3: CSL, CRM retention, leads management.
   - Digitalization: NMS H1/H2, CE Apps, AstraPay, feature usage.
7. **Mapping area sustainability**: Strong/Optimize/Develop/Weak.
8. **Market growth x contribution quadrant**: pick priority review areas.
9. **Area deep review**: integrated performance, mapping network, mapping ring, TTM, people productivity, PICA.

## Rule for using examples

Dummy/sample numbers in the deck should train the analysis flow, not become business facts.

---

## Source-derived module — Best Monthly Operating Control System
_Reconstruction module: `B05` / `BEST_MONTHLY_OPERATING_CONTROL_SYSTEM.md`_

## Function

BEST is the recurring control rhythm that makes dealer execution visible. It takes plans from Sales, Logistics, HC3/TSD/People/Marcomm and turns them into dealer-level TTFU.

## Typical monthly layers

- Sales condition and monthly calendar/theme.
- BTL/showroom/roadshow/twin-date/event directions.
- EV focus and activation approach.
- Sales support/MSW socialization and evidence expectations.
- Register motor vs SSU, register user, lead conversion, CRM/NMS handling.
- Logistics: indent accuracy, truck/stock/run-out, PDI digital.
- H2/H3/TSD controls such as KPB, LCR, unit entry, parts/oil, dashboard usage.
- HC3 controls: CDB quality, mystery calling/booking, CSL/GBP, customer movement.
- People development: productivity, turnover, MyHero, SEIN, SIPEDE, content quality.

## How WorkDesk should use BEST

When a case mentions recent dealer execution, do not only consult training frameworks. Check the applicable monthly operating-review context:

- What was the current event/theme?
- Which execution accuracy metric was being monitored?
- Was there a repeated TTFU from previous month?
- Which system was the source of truth: SEEDS, NMS, webconsole, PDI digital, CRM, Base/worklog?
- Is the issue in activity, data accuracy, follow-up, conversion, productivity, or compliance?

## Currentness rule

BEST decks are month-specific. July 2026 BEST is high authority for July/August operational context in this cluster. Older BEST decks are historical trend and operating rhythm unless a repeated rule is also present in the latest applicable source.

---

## Source-derived module — Business Case Engineering
_Reconstruction module: `B07` / `BUSINESS_CASE_ENGINEERING.md`_

## Required logic

The combined sources define a business case as more than an Excel forecast:

1. **Market Insight** - why the problem/opportunity exists.
2. **Breakdown Target** - what result is required and how it decomposes.
3. **Excellent Execution** - what strategy/activity will be executed and monitored.
4. **Economics** - budget/cost and expected profit or benefit.
5. **Evidence** - before/after and field-monitoring proof.
6. **Customer/CRM linkage** - where relevant, connect the strategy to actual customer data/needs/leads.

## Anti-patterns

- numbers with no new strategy;
- activity list with no market problem;
- target with no ownership/coverage;
- budget with no expected benefit;
- "customer focus" with no CDB/need evidence;
- before/after without explaining causal mechanism;
- one-dealer anecdote presented as area strategy.

## Training-case workbook role

The workbook intentionally leaves future targets/activity blank. It is a thinking scaffold, not a hidden answer key.

---

## Deep module files

- [[../modules/B02__DEALER_DEMAND_FORECAST_OPERATING_SYSTEM|DEALER DEMAND FORECAST OPERATING SYSTEM]]
- [[../modules/B01__BATCH01__SUPERVISORY_MONITORING_TO_CORRECTIVE_ACTION|BATCH01  SUPERVISORY MONITORING TO CORRECTIVE ACTION]]
- [[../modules/B05__ND_PLAN_AND_AREA_REVIEW_MODEL|ND PLAN AND AREA REVIEW MODEL]]
- [[../modules/B05__BEST_MONTHLY_OPERATING_CONTROL_SYSTEM|BEST MONTHLY OPERATING CONTROL SYSTEM]]
- [[../modules/B07__BUSINESS_CASE_ENGINEERING|BUSINESS CASE ENGINEERING]]

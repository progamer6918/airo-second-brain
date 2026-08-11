---
type: source-semantic-dossier
source_id: WD-SRC-056
source_file: "Form Dealer Review (1).xlsx"
source_units: 22 sheets
currentness: HISTORICAL_TEMPLATE_WITH_REUSABLE_OPERATING_LOGIC
semantic_status: SUBSTANTIVE_WORKBOOK_RECONSTRUCTION_WITH_EXTERNAL_DEPENDENCY_UNRESOLVED
---
# WD-SRC-056 — Form Dealer Review Workbook

## Kenapa workbook ini penting

Workbook 22-sheet ini membuktikan bahwa Dealer Review bukan satu dashboard. Ia adalah **working operating system** yang menghubungkan profile, market/area, target & forecasting, people, activity, sales-by-type, Niguri, competitor, territory, RO dan Action Plan.

Semua contoh angka di workbook adalah historical/template evidence kecuali currentness ditetapkan oleh sumber lain.

## 22 sheet — disposition

| Sheet | Fungsi semantic | Catatan trust |
|---|---|---|
| Data | support/reference | bukan framework independen |
| Dealer Profile | context + sales/manpower/composition/pricing/fincoy | reusable structure, sample historical |
| Target & Forecasting | computational target→people→activity→forecast | high-value operating logic |
| Map Area | network/competitor area map | historical example |
| Potensi | area/ring economic-potential calendar | historical/local example |
| Market | near-empty/template | jangan fabricate |
| Remunerasi | incentive/discount model | **93 external-workbook dependencies unresolved** |
| Struk. Org | manpower history | historical |
| Act Plan | activity execution plan | reusable structure |
| Sls Tipe | sales by type | reusable monitoring structure |
| Niguri | Niguri working model | interpret with current policy |
| Sls SS | sales structure | historical/computational |
| Sls SF | sales-force productivity | reusable monitoring structure |
| H Act. | activity + sales-program history | historical examples |
| Ev. BTL | BTL target vs actual | reusable evaluation logic |
| H. ATL | minimal content | no extra meaning invented |
| Comp | competitor program history | historical examples |
| RO | RO/CDB usage model | formula-driven but context must be preserved |
| TTM | territory management by ring/kecamatan | reusable workflow |
| Action Plan | PI→Action→PIC→Due Date control | reusable template |
| rekapan 3 on 3 | review cadence hints | sparse |
| TTFU | **empty** | no TTFU logic can be reconstructed from this sheet |

## Target & Forecasting — operational logic

Sheet ini adalah salah satu pieces paling actionable.

### People / productivity model

Examples of actual workbook formulas:

- `D17=C17/$C$22` — share/contribution relation;
- `E17=C17/F17` — productivity per current people;
- `G17=ROUNDUP(H17*$C$11,0)` — required sales contribution from target assumptions;
- `J17=ROUNDUP(G17/I17,0)` — required headcount from required sales/productivity;
- `K17=J17-F17` — additional people gap;
- `L17=I17-E17` — productivity gap.

Formula cell addresses are provenance, **not universal definitions detached from the workbook labels/context**.

### Activity-to-forecast loop

Workbook models:

`planned activity sales = planned frequency × target sales per event`

then compares actual MTD, remaining activity, and estimated sales if original plan is continued. It has checks equivalent to **Aktivitas SC kurang/OK** and **Aktivitas SM kurang/OK**, then permits a final revised activity plan for the remaining days and recomputes final estimated sales.

Meaning: **forecast gap should lead to a quantified execution question**—people/productivity/activity capacity—not just “push sales harder”.

## TTM — Territory Management workflow

Rows near the end of sheet `TTM` explicitly list:

1. Set Ring per Dealer/Kecamatan.
2. Target Dealer/Ring.
3. Target Dealer/Kecamatan.
4. Dealer Activity/Kecamatan.
5. Dealer set Sales Force untuk Activity.
6. COE Dealer.
7. Evaluasi.

This ties geography → target → activity → people → evaluation.

## Activity evaluation

`Act Plan`, `H Act.` and `Ev. BTL` together preserve three different views:

- **Plan**: where/when/what type/program/team + target visitors/hot prospects/sales/budget;
- **History**: frequency, sales, HP, productivity/event, budget, cost/unit;
- **Evaluation**: target vs actual outcome.

WorkDesk synthesis: **activity count alone is insufficient; effectiveness must be tied to output and target audience/area.**

## Competitor & commercial memory

`Comp` and the program-history portion of `H Act.` preserve historical program patterns. They are useful as case memory and comparison structure, but actual values must never be treated as current program facts.

## Material unresolved dependency — Remunerasi

`Remunerasi` contains 93 formulas referencing external workbooks such as `Master File`. Those dependencies are not embedded here. Therefore:

`REMUNERASI_FULL_MODEL=UNRESOLVED_EXTERNAL_DEPENDENCY`

Do not infer incentive rules or discount caps beyond what is locally explicit.

## Empty TTFU sheet

The sheet exists but has no used semantic range. This is a critical anti-hallucination test:

`TTFU_SHEET_CONTENT=EMPTY`

A model must not generate a TTFU framework from the sheet name.

## Source-unit evidence

See `../07_SOURCE_MEMORY/WD-SRC-056_WORKBOOK_UNIT_LEDGER.tsv` for 22/22 sheet accounting, used ranges, nonempty/formula counts and render hashes.

# Contradiction & Unresolved Ledger

Known source conflicts, missing authorities, external dependencies and unresolved formulas are preserved here rather than silently repaired.

| id | item | issue_type | evidence_state | canonical_guard |
|---|---|---|---|---|
| U-001 | Pricing rate after/before discount formula | FORMULA_UNRESOLVED | Printed 2023 formula is syntactically ambiguous | Do not calculate until authoritative corroboration exists |
| U-002 | Niguri submission schedule | SOURCE_INTERNAL_CONFLICT | Slide contains 1/13/23 and detailed 1/14 plus logistics 1/8/15/22 | Use concept only; current schedule requires current authority |
| U-003 | Dealer Review workbook Remunerasi | EXTERNAL_DEPENDENCY | References [4]Master File | Cannot fully resolve without referenced workbook |
| U-004 | Dealer Review workbook TTFU | MISSING_CONTENT | TTFU sheet empty | Do not fabricate TTFU from this copy |
| U-005 | Recovery Ratio | PARTIALLY_DERIVED | Historical visual supports Retail Sales Daily / precritical baseline interpretation | Keep derived status until another authority confirms formula/definition |
| U-006 | NOS 2026 indexed-sheet formula references | CROSS_ENGINE_EXECUTION_UNPROVEN | Stored/parsed formulas contain indexed sheet syntax | Scoring intent trusted; recalculation engine parity not claimed |
| U-007 | VE 2025 survey totals | SOURCE_DATA_INCONSISTENCY | Some category totals do not reconcile exactly to n=124 | Preserve reported values + warning |
| U-008 | Negotiation “6 weapons” | SOURCE_TEXT_INCONSISTENCY | Source says six but only five are taught/listed | Use five; do not invent sixth |
| U-009 | Intermediate 9-slide timing | SOURCE_TEXT_INCONSISTENCY | Overall label conflicts with three 3-minute sub-blocks | Use storyline, not timing as rule |
| U-010 | Advance time quadrant | SOURCE_ARITHMETIC_ANOMALY | 28+33+24+18 = 103% | Treat as illustration, not normative allocation |
| U-011 | Tabel MS workbook formula lineage | WORKBOOK_FORMULA_UNRESOLVED | Visible formulas reference off-range cells | Use displayed/cached values only; not trusted recalc engine |
| U-012 | PENETRASI Q1 result timing | SOURCE_TIMING_AMBIGUITY | Narrative Q1 M/S 80.8 while March actual panel says TBD | Preserve both without silent reconciliation |
| U-013 | PENETRASI measure mismatch | MEASURE_AMBIGUITY | Market-Honda values and dealer-sales actual are distinct measures | Never equate them |
| U-014 | 8-Step method in Advance final-project guidance | METHOD_SEQUENCE_NOT_RECONSTRUCTED | Method named but exact sequence not supported by reconstructed source set | Do not invent sequence |
| U-015 | VE 2026 authority | CURRENTNESS_GAP | No 2026 VE guidance in baseline | Return latest-available-not-confirmed-current |
| U-016 | Ring map currentness | CURRENTNESS_GAP | Only 2022 ring mapping supplied | Treat as historical until confirmed |
| U-017 | FLP uniform currentness | CURRENTNESS_GAP | Latest supplied 5 Jun 2025 | Verify if still active in 2026 |
| U-018 | Batch02 formula-cell count metadata | RECONSTRUCTION_METADATA_DEFECT | Old BATCH02_KNOWN_LIMITATIONS said 6,808 formula cells; sheet-profile sum is 4,153 | Canonical reconciliation uses 4,153 and marks old count invalid |
| U-019 | Sinsen POS type classification rows 7/10/11/13/16 | SOURCE_INTERNAL_CLASSIFICATION_CONFLICT | Tipe POS=H1 while source note says 'merupakan H23' | Do not silently recast; validate H1/H2/NetDev master identity before final POS master |
| U-020 | Sinsen POS submission readiness 2026-08-11 | CURRENT_DATA_COMPLETENESS_GAP | Supplied All-pos sheet lacks Kelas POS, Kelurahan and coordinates required by meeting guidance | Do not claim submission-ready or complete until required fields are present/validated |
| U-021 | SSP exact 3 Mega POS identities | MISSING_REQUIRED_CLASS_FIELD | Meeting target says SSP input=3 Mega POS; supplied Sinsen snapshot has no POS class | Return target count but refuse exact POS selection until class authority is supplied |
| U-022 | Integrated TTM current H2 numerical state | CURRENTNESS_DATA_GAP | Meeting defines Loss Demand/UE/SPR/customer-movement method but no current Sinsen H2 numerical dataset supplied | Do not generate actual H2 priority kecamatan or performance conclusions |
| U-023 | Planned POS name/location — Anugrah | SOURCE_AMBIGUITY | Plan row says 'POS Pasar ?' | Keep unresolved; do not normalize to a guessed market/location |

| U-024 | Market Info Tools meeting source completeness | SOURCE_COVERAGE_GAP | TurboScribe file stops after first 30 minutes; only two screenshots supplied | Do not claim the dossier captures decisions/features discussed after transcript cutoff |
| U-025 | Market Info Tools full event/PDRB taxonomy | SOURCE_COVERAGE_GAP | Screenshot shows a cropped visible subset; full official list not supplied | Preserve visible subset only; do not invent missing categories |
| U-026 | Market Info Tools positive/negative issue flag | PROPOSED_FEATURE_NOT_CONFIRMED | Participant requested polarity classification; response treated it as possible future enhancement | Do not present polarity field as current system feature |
| U-027 | Actual weekly Market Info records | CURRENT_DATA_GAP | No dealer weekly event dataset/export supplied | Brain knows workflow, not historical dealer/kecamatan event observations |

# Batch 01 Quality Gate

## Scope

Sources:

- `2. ASSDP Basic - PDCA.pptx` — 10 slides
- `10. Sales _ Stock Monitoring per Dealer.pptx` — 12 slides
- `11. Analisa Pricing _ FID-BA.pptx` — 16 slides
- `12. PICA.pptx` — 31 slides

Total source units: **69 slides**.

## Source truth

- Original binaries opened directly from Owner-uploaded intact ZIP corpus.
- Actual source SHA-256 calculated locally.
- Slide count taken from actual PPTX package.
- Every slide rendered from the actual PPTX through LibreOffice → PDF → PNG.
- Actual SHA-256 of extracted slide text and rendered image captured in `BATCH01_SOURCE_TRUTH.tsv`.
- Contact-sheet visual sweep covered every slide; dense/decision-critical slides were opened individually at readable resolution.

## Anti-fabrication checks

- No synthetic text/render SHA values.
- No claim based on Antigravity receipt.
- No generic “slide N procedural guidance” placeholders.
- Historical example numbers are not promoted to current facts.
- Thresholds are included only where source explicitly states them.
- Ambiguous rate formulas in Pricing deck are preserved as unresolved instead of silently corrected.
- Acronyms/program labels not expanded by these sources remain unresolved unless their meaning is self-evident from explicit source text.

## Semantic accounting

- PDCA: 10/10 slides accounted for.
- Sales & Stock Monitoring: 12/12 slides accounted for.
- Pricing & FID-BA: 16/16 slides accounted for.
- PICA: 31/31 slides accounted for.
- Total: 69/69 source units accounted for.

`accounted for` means reviewed for whether the slide carries conceptual, procedural, numerical, diagnostic, case, visual, historical, relational, or provenance value. Closing/title slides are explicitly recognized as low-semantic rather than silently omitted.

## Visual accounting

Material visual semantics captured include:

- PDCA cycle graphic and slide-8 artifact chain.
- Total MD sales/stock/in-transit/distribution time-series visualization.
- Kabupaten/Dealer/series drill-down table layout and numbered analysis callouts.
- Pricing head-to-head component table and trend charts.
- PICA general-to-specific funnels, Area→Product/Product→Area pathways, contribution tables, good-vs-bad causal analysis, and Situational Analysis→PI→CA→Next Action architecture.

Not every pixel or micro-label inside illustrative screenshots is promoted to knowledge. Where micro-content is not necessary to the source's semantic point, it remains source evidence rather than inferred operational rule.

## Unresolved register

1. Pricing deck's printed `Rate After Discount` / `Rate Before Discount` formulas contain an ambiguous `-1` term; no correction has been inferred.
2. Historical FID/BA thresholds and lender practices from 2023 require current-source corroboration before 2026 operational use.
3. Several historical program/acronym labels in PICA examples (`GC`, `SMH`, `RO-TI`, etc.) are not expanded by the deck itself.
4. The four sources do not define forecasting formulas, full Dealer Review workbook logic, Demand/Recovery Rate, Niguri, or current NOS rules.

## Gate result

`SOURCE_TRUTH_CAPTURE=PASS`

`SEMANTIC_REVIEW=PASS_WITH_EXPLICIT_UNRESOLVED_REGISTER`

`CROSS_SOURCE_BATCH01_SYNTHESIS=PASS`

`CANONICAL_ASB_IMPORTED=NO`

`FULL_WORKDESK_RECONSTRUCTION=NO`

This gate is only for the four Batch-01 sources in the local reconstruction pack. It does not modify or override the canonical ASB ledger until a later deterministic import is approved.

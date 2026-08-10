# Decision Rule Library — Batch 01

## DR-001 — Do not diagnose before localization

Before assigning root cause to a sales/M/S symptom, identify where the contribution sits using available hierarchy: Area/Kabupaten/Dealer/Series or Product/Segment/Area/Dealer.

- Support: `10. Sales _ Stock Monitoring per Dealer.pptx` slides 7, 9–10; `12. PICA.pptx` slides 4–14.
- Classification: `SOURCE_GROUNDED_SYNTHESIS`.

## DR-002 — Read sales together with stock/in-transit/distribution

At total-MD level, do not interpret sales movement independently from Stock MD, Stock Dealer, AHM–MD in-transit, and AHM Distribution when those data are available.

- Support: `10. Sales _ Stock Monitoring per Dealer.pptx` slide 4.
- Classification: `EXPLICIT_SOURCE_INTENT`.

## DR-003 — An explanation must explain what changed

A fact/program that existed before and after the observed decline is insufficient by itself unless a material element changed or another mechanism explains why the outcome changed.

- Support: “good vs bad” PICA questions, `12. PICA.pptx` slide 23.
- Classification: `SOURCE_GROUNDED_REASONING_RULE`.

## DR-004 — Broad external factors require a differential explanation

If a broad external factor is claimed as a root cause, test why comparable products/areas did not show the same effect.

- Support: PICA challenge about commodity-price decline and other series, slide 23.
- Classification: `SOURCE_GROUNDED_REASONING_RULE`.

## DR-005 — Quantify claimed event contribution where possible

If GC/event volume is claimed as a cause, ask how many units and whether the magnitude can explain the observed performance change.

- Support: PICA slide 23.
- Classification: `EXPLICIT_SOURCE_QUALITY_QUESTION`.

## DR-006 — Corrective Action must counter the identified mechanism

Countermeasure should follow Problem Identification rather than being a generic list of activities.

- Support: PICA slides 24–25 and PDCA slide 7.
- Classification: `SOURCE_GROUNDED_SYNTHESIS`.

## DR-007 — Price competitiveness is component-level, not OTR-only

A Honda package can be judged uncompetitive even when OTR is competitive if DP Real, installment, or rate is worse versus competitor.

- Support: `11. Analisa Pricing _ FID-BA.pptx` slide 4.
- Classification: `EXPLICIT_WORKED_EXAMPLE_GENERALIZATION`.

## DR-008 — Financing quality can affect sales access

High FID/BA4 can cause Fincoy to become more selective, especially around low DP or higher-risk customer/area categories; therefore financing-quality conditions can be relevant to sales diagnosis.

- Support: pricing/FID-BA slide 9.
- Classification: `EXPLICIT_SOURCE_RELATIONSHIP`.
- Current-policy caveat: historical training source; current lender policy requires verification.

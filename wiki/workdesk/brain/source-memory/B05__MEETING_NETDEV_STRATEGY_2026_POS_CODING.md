# Source Dossier — Network Development Strategy 2026 / Integrated TTM / POS Coding

## Source set

1. `Meeting Netdev Strategy 2026 dan Perapihan Pengkodean POS.pdf`
   - 28 screenshot-based pages
   - SHA256 `bf9f024b71890db5e14646bcc3410214bf0703c03699a2cdd572312e2ee7aba7`
   - same binary hash as the prior Batch05 source
2. `Transkrip_dan_MoM_NetDev_Strategy_2026_Integrated_TTM_POS.docx`
   - clean transcript + executive summary + action items
   - meeting date: 2026-08-06
   - SHA256 `8e129ea310c7c432297220613ae83101d95eaffe09ab5e23b941ab5e5cd0f392`
3. `Pengkodean POS_Sinsen_Aug 2026.xlsx`
   - Sinsen working snapshot dated 2026-08-11
   - SHA256 `2f7615d55fb3f604e323d282a4be15d9337609b1fc08c37dc3daac07d8052091`

**Reconciliation outcome:** `UPDATE + SUPPORTING + CURRENT_BUSINESS_DATA`.  
The earlier screenshot-only reconstruction is retained, but the new transcript resolves many text/detail limitations and the spreadsheet adds current Sinsen execution state.

## Authority / currentness

- Meeting-level NetDev / Integrated TTM concepts are current supplied 2026 authority as of 2026-08-06.
- Formal AHM guidance/forms distributed after the meeting may supersede meeting details.
- Sinsen POS spreadsheet is a current working snapshot as of 2026-08-11, not proof of AHM submission acceptance.
- Older H1-only TTM remains lineage/historical method for current Integrated TTM questions.

## Durable semantic update

Integrated TTM extends TTM from dealer/network/locality into an integrated H1-H2 territory system down to kecamatan and POS.

### Core operating sequence
1. **Mapping Ring**
   - target M/S, Sales, UE, SPR
   - breakdown area → kabupaten → kecamatan → network/POS
   - H1 registration + H2 customer movement
   - all POS used for mapping/coverage
   - Mega + Selected POS are the initial 2026 performance/target input population
   - area potential = Market Growth H1 + Loss Demand H2 + coverage condition
   - output = final target + priority + coverage strategy + coverage plan
2. **Activities & Scheduling**
   - translate coverage plan into H1-H2 activities, locations, schedules, manpower, targets and cost
3. **Review & Monitoring**
   - quarterly review
   - kabupaten/kecamatan/network/POS viewpoints
   - performance + cross-border/customer movement + manpower/activity adequacy
   - improvement/PICA
   - integrated into ND Plan Review

## POS target mechanism

National meeting rule:
- Mega POS >20% of total POS → input target = 100% Mega POS
- Mega POS <20% → 100% Mega POS + Selected POS until 20% of total POS
- no Mega POS → 20% of total POS
- national target shown = 225 POS = 150 Mega + 75 Selected/other

For **SSP**, slide table shows:
- target input = **3**
- Mega POS = **3**
- other/Selected POS = **0**

Mapping Ring still uses **100% POS**, so target-input scope must not be confused with coverage-mapping scope.

## KPI 2026

Current meeting says KPI remains H1-focused:
- Achievement Lokasi ≥85%
- Achievement Ring 1 ≥85%
- Locality based on grading
- SSP Target Locality 2026 = **89%**

H2 integration is monitored but not yet promoted here as a final KPI gate.

## POS standardization

Purpose: make H1/H2/H23 POS administration, performance monitoring and coverage analysis consistent across Marketing Data 2, Honda Profile and INS.

Required code format: `dealer code + "-" + four-digit POS order` (Q&A explicitly confirms four digits).

Required master completeness:
- POS type
- POS class
- kabupaten/kecamatan/kelurahan
- coordinates
- consistent code

## Current Sinsen execution snapshot

The 2026-08-11 workbook contains 14 POS rows / 10 parent dealer codes and three code changes. It also exposes unresolved data-quality gaps that must not be repaired silently:
- five `H1` rows say `merupakan H23`
- one H23 row lacks kabupaten/kecamatan
- class POS, kelurahan and coordinates are not present in the supplied All-pos table
- three POS-SMK entries are explicitly classified as TEFA/not-POS in the plan sheet
- planned/trial POS entries are not confirmed active master data

See `business-memory/operational/INTEGRATED_TTM_POS_CURRENT_STATE_2026-08-11.md` and related TSVs for decision-grade current data.

## Limitation boundary

The clean transcript is not stenographic verbatim and explicitly normalizes uncertain speech using the meeting slides. This is acceptable for professional semantic reconstruction, but formal AHM post-meeting guidance remains the higher future authority if supplied.

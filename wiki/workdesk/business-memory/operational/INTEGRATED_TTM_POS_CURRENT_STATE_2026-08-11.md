# Integrated TTM & POS Standardization — Current Supplied State

**As-of:** 2026-08-11  
**Meeting authority date:** 2026-08-06  
**Sinsen POS working snapshot:** 2026-08-11  
**Currentness rule:** formal AHM guidance/form issued after the meeting may supersede meeting-level details.

## Reconciled 2026 operating model

Integrated TTM is the current evolution of older H1-focused TTM. Dealer/network remains the primary territory-management base, while the analysis extends through **kabupaten → kecamatan → network/dealer → POS** and integrates H1 with H2.

### Step 1 — Mapping Ring
- AHM target families: **M/S, Sales, Unit Entry (UE), SPR**.
- MD breaks target down by area, kabupaten, kecamatan, network and POS.
- Historical H1 uses **Data Registration**; H2 uses **Data Customer Movement**.
- **100% network and POS locations** are used for Mapping Ring / coverage analysis.
- For 2026 performance/target input, POS scope starts with **Mega POS + Selected POS** according to the target mechanism.
- Potential per kecamatan combines **Market Growth H1 + Loss Demand H2 + coverage condition**.
- Output: final target, area priority, coverage strategy and coverage plan.

### SSP-specific POS target supplied by the meeting
- `Target Input Integrated TTM = 3 POS`
- `Mega POS = 3`
- `Selected/other POS = 0`
- This does **not** mean only three POS are mapped; Mapping Ring still uses **100% POS**.
- The current Sinsen spreadsheet does not contain `Kelas POS`, so the exact three Mega POS cannot be selected from the supplied snapshot alone.

### Step 2 — Activities & Scheduling
Coverage plan is converted into H1-H2 activity, location, schedule, manpower allocation, target and cost. Joint H1-H2 activity is encouraged and manpower adequacy is checked against the plan.

### Step 3 — Review & Monitoring
- Quarterly review.
- Review may be sliced by kabupaten, kecamatan, network/dealer and POS.
- Check actual H1/H2 achievement, area potential, growth/loss demand, cross-border/customer movement, manpower and activity before defining PICA.
- Integrated TTM results are reviewed through **ND Plan Review**.
- Meeting guidance says review input uses an average one-month view from three-month data for activity POV.

## KPI / monitoring 2026

The meeting explicitly says KPI 2026 remains H1-focused while H2 integration is early-stage:
- **Achievement Lokasi ≥ 85%**
- **Achievement Ring 1 ≥ 85%**
- **Locality — based on grading**
- For **SSP**, the slide table shows **Target Locality 2026 = 89%**.
- H2 is still monitored; the slide also asks MD to monitor Unit Sales vs Unit Entry ratio. Treat this as monitoring guidance, not as a proven universal KPI gate unless later formal guidance confirms it.

## POS standardization — operating rule

Required code format: `KODE_DEALER-4_DIGIT_URUTAN`, e.g. `02670-0001`.

Lifecycle rules from the Sinsen working file:
1. POS numbering follows the count/order under the parent dealer.
2. Closed POS → code is deactivated.
3. Reopened POS → receives a new POS code.
4. Relocation within the **same kecamatan** → code remains.
5. Relocation to a **different kecamatan** → old code resigned/deactivated and a new code is issued.
6. POS class upgrade/downgrade → code remains.

Meeting-required master fields include:
- Tipe POS: H1 / H123 / H23
- Kelas POS: POS / Mini POS / Mega POS
- Kabupaten
- Kecamatan
- Kelurahan
- coordinates
- standardized POS code

## Sinsen POS snapshot — 2026-08-11

Source range: `Pengkodean POS_Sinsen_Aug 2026(1).xlsx / All pos!A4:N18`.

- Records: **14**
- Unique parent dealer codes: **10**
- Type mix: **8 H123 / 5 H1 / 1 H23**
- Revised/new POS codes: **3**
- Duplicate revised codes detected: **0**
- Rows marked present in TSD list: **8 / 14**
- Five rows carry an internal classification conflict: `Tipe POS=H1` while `Catatan=merupakan H23`.
- One H23 row lacks Kabupaten/Kecamatan.
- The supplied sheet does **not** contain Kelas POS, Kelurahan, or coordinates, despite those being required in the meeting guidance.

### Exact code changes in supplied working snapshot
- `12142-0002 → 12142-0001` — Daya Motor - Jambi
- `13384-0006 → 13384-0004` — PAS Jambi / Tanjab Barat
- `- → 3538-0001` — PT. CITRA LENCANA SAKTI - PAMENANG

The last row carries source comment: **menginduk ke CLS Bangko**.

### TEFA boundary
The `plan` sheet explicitly states **TEFA / POS SMK is not POS and should not be registered in the POS list**. Three listed POS SMK records are preserved as exclusions, not active POS master records.

### Planning rows
Four plan/trial entries are present. They are not promoted to confirmed active POS:
- TJS Tembesi — POS Mersam — already trial open
- Asmo — POS Jambi Selatan — not yet open
- Anugrah — `POS Pasar ?` — unresolved name/location
- WJM — 7 Koto Ilir — planned trial service visit / periodic permanence concept

## Submission/readiness boundary

As of 2026-08-11:
- **Submission Perapihan Pengkodean POS deadline = 2026-08-13**
- **Submission Mapping Ring deadline = 2026-08-24**
- Completion/submission status is **not proven** by the supplied files.
- The current working sheet is **not proven submission-ready** because required class/kelurahan/coordinate fields are not present and classification conflicts remain.

## Missing current evidence

The meeting defines H2 potential/performance using Loss Demand, UE, SPR and Customer Movement, but the supplied corrective/current input does not contain the current Sinsen H2 numerical dataset. Do not fabricate Integrated TTM H2 area-priority results yet.

## Provenance

- `Meeting Netdev Strategy 2026 dan Perapihan Pengkodean POS(1).pdf` — SHA256 `bf9f024b71890db5e14646bcc3410214bf0703c03699a2cdd572312e2ee7aba7`
- `Transkrip_dan_MoM_NetDev_Strategy_2026_Integrated_TTM_POS(1).docx` — SHA256 `8e129ea310c7c432297220613ae83101d95eaffe09ab5e23b941ab5e5cd0f392`
- `Pengkodean POS_Sinsen_Aug 2026(1).xlsx` — SHA256 `2f7615d55fb3f604e323d282a4be15d9337609b1fc08c37dc3daac07d8052091`

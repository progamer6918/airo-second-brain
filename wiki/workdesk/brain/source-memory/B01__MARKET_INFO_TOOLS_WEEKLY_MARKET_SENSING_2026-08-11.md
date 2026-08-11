# Market Info Tools — Weekly Market Sensing (11 Aug 2026)

> **Source authority:** Owner-supplied 11 Aug 2026 meeting transcript (TurboScribe, first 30 minutes only) + two meeting screenshots.
> **Input mode:** `CASE_DRIVEN_DELTA`.
> **Coverage boundary:** The transcript explicitly ends at the 30-minute limit. This dossier does not claim to represent decisions made after that point.
> **Security boundary:** Portal URL, Google Form URL, usernames/passwords, and direct-access details are intentionally excluded from public ASB memory.

## Purpose
Market Info Tools is a field-sensing mechanism intended to collect weekly market information from dealers, turn it into market insight, relate market conditions to sales performance, and support early warning / defensive decision-making. The meeting described four purposes:
1. weekly field information collection;
2. market insight on trends, competitor activity, opportunities, and risks;
3. performance analysis linking market conditions with sales performance;
4. early warning / recommendation as a decision basis.

## Current transitional operating flow
The source distinguishes the **current Sinsen transition flow** from the desired end-state flow.

### Current transition flow (as of 11 Aug 2026)
`Dealer -> MD Google Form -> Supervisor Sales Area validation -> dealer submits approved content to AHM Market Info Tools portal`

The additional Google Form is a temporary quality-control step used to verify language, completeness, and market-description quality before the same information is entered in the AHM portal. A presenter explicitly clarified that the eventual normal flow is expected to be direct dealer submission to the Market Info Tools portal once dealer capability/consistency is sufficient.

### Submission cadence
- Submit **every week**.
- Deadline: **no later than Friday of the running week**.
- Submission remains required according to schedule even when there is no special market event.
- More than one relevant market event may be recorded in the same week.

## Observation grain
The operating grain is:
`dealer x kecamatan x market-event category/categories x event start date x event end date x detailed note`

Portal fields described in the meeting include dealer, province and kota/kabupaten (system-filled), kecamatan, event/PDRB category, event period, and detailed notes. Multiple event categories can be selected when they are relevant to the same observation.

### Dealer keying rule
Two dealers may report the same event in the same kecamatan. The meeting explicitly says the data is keyed to each dealer because the later analysis is intended to relate each dealer's market observation to that dealer's own performance. Different dealers may therefore legitimately have different field viewpoints even when Ring/territory overlaps.

## Data-quality rules
- Use clear, proper Indonesian and write a detailed market narrative.
- Describe the event/condition specifically rather than only selecting a dropdown label.
- Where observable, describe change over time (before/current, weekly/monthly movement) and add useful detail.
- Do not treat a selected event label itself as proof of sales causality. The stated analytical intent is to compare market information with performance later.
- Validate dates and narrative before final save. The demonstrated portal was described as having **no edit/delete capability after submission**.
- After save, verify the entry appears in the recap list. A recap can be downloaded/exported to Excel.

## Screenshot-visible event categories
The screenshots show a visible subset of the event/PDRB checklist, including: Gaji ke-13 PNS; Inflasi Naik/Stabil/Turun; Suku Bunga Naik/Turun; Pembangunan Jembatan/Jalan Tol Baru; Perbaikan Akses Jalan; Pembebasan Lahan/Tanah; Hujan; Kemarau; Banjir; Bencana Alam; Masuk Tahun Ajaran Baru (Sekolah); Harga Bahan Baku Pasar Naik/Turun/Stabil; PHK; Pembukaan Pabrik Baru; and several cultural/government-related options.

**Do not treat this as the complete official taxonomy.** The screenshot is cropped and the transcript does not enumerate the full list.

## Q&A boundaries
### Positive/negative classification
A participant requested an explicit positive/negative issue category. The response treated this as a possible future enhancement, not a current confirmed feature. Current focus is consistency and quality of weekly submissions during the trial/piloting phase.

### Google Form permanence
The Google Form is not a permanent architecture claim. It is a temporary MD validation gate and may be removed when dealers can submit quality market information directly to the AHM portal.

## Reconciliation with existing WorkDesk brain
This source **updates** the market-sensing layer already present in ND Plan / Market Insight reasoning by adding a current weekly field-intelligence operating process. It supports the existing principle:

`market condition -> quantified/contextual observation -> compare to performance -> diagnose -> action`

However, the meeting does **not** formally state that Market Info Tools is an official input to Integrated TTM. It may analytically complement ND Plan/territory analysis, but that relationship must remain an inference unless a later formal source states it.

## Provenance
- `11-08-2026-Meeting(Audio)-2026-08-11T06-19-23-527Z(1).txt` — SHA256 `e949fcf8030d620a8796142d673d4faa8a9f75f8c55495e33276dd5c559bb3cb` — transcript truncated at 30 minutes.
- `Screenshot 2026-08-11 132416.png` — SHA256 `e1499e2aa28da3f356c5c382c474cd8f1f916ab8392de43d1690b3ae602ccc6a` — Google Form/validation workflow and visible event-category list.
- `Screenshot 2026-08-11 132725.png` — SHA256 `7d7d110ee535d1d838de98a5b1d636e25eb5e32207762d045177124763c6e87e` — weekly submission cadence and dealer/Kacab role.

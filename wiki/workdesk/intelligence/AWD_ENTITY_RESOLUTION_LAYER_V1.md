# AWD Entity Resolution Layer v1

## Purpose

The **AWD Entity Resolution Layer v1** is a generic, reusable intelligence engine designed to bridge natural human business language with canonical AIRO WorkDesk operational authorities.

It eliminates the gap between how business users communicate (nicknames, acronyms, branch names, conversational queries) and the strict canonical keys required by operational datasets.

---

## 1. Resolution Principle

**Never query operational authority directly from raw user wording.**

Every user query flows strictly through the canonical resolution pipeline:

```
USER_BUSINESS_TERM
        ↓
ENTITY_RESOLUTION
        ↓
CANONICAL_ENTITY
        ↓
AUTHORITY_QUERY
        ↓
STRUCTURED_EVIDENCE_RECEIPT
```

---

## 2. Multi-Domain Entity Scope

The entity resolution capability covers 4 key business dimensions:

### 1. Dealer Entity
- **Nicknames & Portmanteaus**: e.g. `Sinsen` → `PT. SINAR SENTOSA MOTORA`, `Astra/HSO` → `PT. ASTRA INTERNATIONAL TBK-HONDA`.
- **Corporate Acronyms**: e.g. `CSM` → `CITRA SENTOSA MOTOR`, `CLS` → `CITRA LENCANA SAKTI`, `DAM` → `DAYA ANUGRAH MANDIRI`, `TDM` → `TUNAS DWIPA MATRA`, `PAS` → `PATRIA ANUGRAH SENTOSA`, `NSS` → `NUSANTARA SURYA SAKTI`.
- **Branch Contractions**: e.g. `Bulian` → `BULIAN`, `SRLG` → `SAROLANGUN`, `M.Angin` → `MANDIANGIN`, `Rimbo` → `RIMBO BUJANG`.
- **POS Network**: Resolves POS branch affiliations and parent dealer relationships (e.g. `POS PATRIA - PAUH` linked to parent dealer).

### 2. Territory Entity
- **Kabupaten**: 9 official kabupaten/kota in Jambi province (e.g. `Batanghari`, `Bungo`, `Sarolangun`, etc.).
- **Kecamatan**: 118 administrative districts mapped in 2026 area hierarchy (e.g. `PAUH`, `MANDIANGIN`, `ALAM BARAJO`).
- **Kelurahan/Desa**: 1,223 micro-territories with assigned Area Codes (e.g. `AREA 1404`).

### 3. Product Entity
- **Common Model Names**: e.g. `Beat`, `Vario 160`, `Scoopy`, `CRF150L`, `PCX 160`.
- **Official Type Codes**: e.g. `ES7` → `CRF150L`, `X1H` → `BEAT SPORTY CBS`.
- **Market Segments**: `AT High`, `AT Mid`, `AT Low`, `Cub High`, `Cub Mid`, `Cub Low`, `Sport High`, `Sport Mid`, `Sport Low`, `EV`.

### 4. Organization Entity
- **Dealer Groups**: Group parent networks spanning multiple outlets (e.g. Sinsen Group, Daya Group, Tunas Group).
- **Network Levels**: Main Dealer → Dealer Group → Dealer Outlet → POS → FLP.

---

## 3. Authority Source Hierarchy

The resolver operates dynamically against existing canonical authorities, obeying strict source priority:

1. **Dealer Network Authority**: Ingestion standards, POS network alignments, and ownership attribution.
2. **AWD Capability Registry** (`wiki/workdesk/reference/AWD_CAPABILITY_REGISTRY.md`).
3. **Operational Data Inventory** (`wiki/workdesk/brain/reference/OPERATIONAL_DATA_INVENTORY.tsv`).
4. **Operational TSV Datasets**:
   - `RETAIL_2026_YTD_JUL_DEALER.tsv`
   - `POLREG_2026_AREA_HIERARCHY.tsv`
   - `POLREG_YTD_JUN_2026_GEOGRAPHY_SEGMENT.tsv`
   - `RETAIL_2026_YTD_JUL_TYPE.tsv`
5. **Historical References**:
   - `RING_MAPPING_2022_HISTORICAL.tsv`
   - `POS_STANDARDIZATION_SINSEN_2026-08-11.tsv`

**Guardrail Invariant**: Zero manual nickname tables, zero hardcoded single dealer lists, and zero duplicate master databases. Entity catalogs are indexed dynamically from authority sources at runtime.

---

## 4. Output Contract (`ENTITY_RESOLUTION_RECEIPT`)

Every entity resolution invocation returns a structured receipt:

```text
🧭 AIRO STATUS

ENTITY_RESOLUTION_RECEIPT
USER_TERM: "Review Sinsen Bulian"
ENTITY_TYPE: DEALER
CANONICAL_ENTITY: PT. SINAR SENTOSA MOTORA - BULIAN
MATCH_STATUS: RESOLVED
MATCH_CONFIDENCE: HIGH
SOURCE_USED: wiki/workdesk/business-memory/operational/RETAIL_2026_YTD_JUL_DEALER.tsv
NEXT_ACTION: QUERY_READY
```

### Receipt Enums:
- `MATCH_STATUS`: `RESOLVED` | `AMBIGUOUS` | `NOT_FOUND`
- `MATCH_CONFIDENCE`: `HIGH` | `MEDIUM` | `LOW`
- `NEXT_ACTION`: `QUERY_READY` (if resolved with high confidence) | `NEED_CLARIFICATION` (if ambiguous or unresolved)

---

## 5. Tool Integration & Usage

### 1. Standalone Resolution Tool
```bash
scripts/airo-workdesk-entity-resolve "Sinsen Bulian"
scripts/airo-workdesk-entity-resolve "CSM Sarolangun"
scripts/airo-workdesk-entity-resolve "Kecamatan Pauh"
```

### 2. Direct Query Tool Integration
`scripts/airo-workdesk-query` executes the entity resolution phase before any authority query:
```bash
# Test 1: Dealer review
scripts/airo-workdesk-query "Review Sinsen Bulian"

# Test 2: Dealer comparison
scripts/airo-workdesk-query "Compare CSM Sarolangun vs CSM Mandiangin"

# Test 3: Territory opportunity analysis
scripts/airo-workdesk-query "Analyze Kecamatan Pauh opportunity"
```

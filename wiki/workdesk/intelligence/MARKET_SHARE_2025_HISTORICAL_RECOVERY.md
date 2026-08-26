# Market Share 2025 Historical Recovery & Intelligence Contract

## 1. Metadata & Provenance
- **Project**: AIRO WorkDesk (AWD)
- **Year**: 2025 (Jan-Dec)
- **FY Total Market**: 127,244 units (100% exact cross-source match)
- **Honda Total**: 103,182 units (81.09% M/S)
- **Yamaha Total**: 23,261 units (18.28% M/S)
- **Suzuki Total**: 24 units (0.02% M/S)
- **Other Brands Total**: 777 units (0.61% M/S)
- **Primary Sources**:
  1. `SINSEN_EVALPOLREG+MSPERKAB_DEC 2025.xlsx` (`WD-SRC-107`)
  2. `POLREG PER KECAMATAN PER KELURAHAN PER SEGMENT 2025.xlsx` (`WD-SRC-108`)

## 2. Geography Structure
- **Kabupaten Count**: 9 (Batanghari, Bungo, Kota Jambi, Muaro Jambi, Merangin, Sarolangun, Tanjab Barat, Tanjab Timur, Tebo)
- **Kecamatan Count**: 100 Kecamatan pairs
- **Kelurahan/Desa Count**: `NOT_PROVEN` (Area ID represents micro-geography level)
- **Micro-Geography (Area ID) Count**: 1,223 Area IDs (`AREA 1` .. `AREA 1223`)
- **Verified 2025 Hierarchy**: `Area ID -> Kecamatan -> Kabupaten`

## 3. Result Contract & Foundations
- **Foundation 1**: Market Type x Kabupaten x Month Fact (Source 1 Database Polreg 2025)
- **Foundation 2**: Market Micro Geography Fact (Source 2 Data + S2 presentation sheets join)
- **Foundation 3**: Market Geography Master (Year-Aware)
- **Foundation 4**: Market Product & Segment Master (Version-Aware; only supported fields included)

## 4. Generated Retrieval Views
1. Market Monthly & Annual
2. Brand / Competitor
3. Segment
4. Kabupaten
5. Kecamatan
6. Micro-Geography / Area ID
7. Type / Model Market

## 5. Public Fresh Retrieval Index
- **Jan 2025 Total Market**: 8,670 units
- **Dec 2025 Total Market**: 12,260 units
- **FY 2025 Total Market**: 127,244 units
- **Honda FY 2025**: 103,182 units (81.09% M/S)
- **Yamaha FY 2025**: 23,261 units (18.28% M/S)
- **Merangin FY 2025 Total Market**: 16,824 units (Honda 13,408 / 79.69%, Yamaha 3,416 / 20.31%)

## 6. Known Limitations
- Kelurahan/Desa 2025 not proven
- S2 presentation header FY 2024 label anomaly for 2025 data
- January MoM presentation growth requires Dec 2024 baseline
- Raw sheets are numerical authority over presentation defects

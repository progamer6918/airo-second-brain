# Market Strategic View — YTD Jan–Jun 2026

**Status:** derived analytical snapshot. Recompute when a newer market source arrives; do not promote these priorities into permanent causal rules.

## Province-level competitive pool
Source for province segment metrics: dedicated M/S memory from `SINSEN_EVALPOLREG+MSPERKAB_JUN 2026.xlsx`.

| Segment | Total Market | Honda | M/S | Δ share | Non-Honda volume | Share of classified non-Honda pool |
|---|---:|---:|---:|---:|---:|---:|
| AT High | 23125 | 14251 | 61.63% | +6.40 poin | 8874 | 63.34% |
| Cub Mid | 5284 | 2968 | 56.17% | +2.73 poin | 2316 | 16.53% |
| Cub High | 1368 | 234 | 17.11% | -7.17 poin | 1134 | 8.09% |
| AT Mid | 14396 | 13539 | 94.05% | +1.55 poin | 857 | 6.12% |
| Sport Mid | 3981 | 3584 | 90.03% | +2.55 poin | 397 | 2.83% |
| AT Low | 23392 | 23019 | 98.41% | +0.20 poin | 373 | 2.66% |
| Sport High | 42 | 6 | 14.29% | -3.90 poin | 36 | 0.26% |
| Cub Low | 6731 | 6713 | 99.73% | -0.18 poin | 18 | 0.13% |
| Uncategorized | 4 | 0 | 0.00% | +0.00 poin | 4 | 0.03% |
| Sport Low | 719 | 717 | 99.72% | -0.08 poin | 2 | 0.01% |

### Working interpretation
- **Cub High = correction/RCA problem:** share deteriorated materially while the market accelerated faster than Honda.
- **AT High = largest strategic capture battlefield:** share improved, but the absolute non-Honda pool remains the largest by far; do not label it a deterioration problem.
- **Cub Mid = meaningful capture opportunity:** mid-level M/S plus a large non-Honda pool.
- Very small denominators such as Sport High must not outrank materially larger segments merely because M/S is lower.

## AT High — largest kecamatan-level non-Honda pools in POLREG source
| Kabupaten | Kecamatan | Market | Honda | Non-Honda | M/S | Δ vs Jan–Jun 2025 |
|---|---|---:|---:|---:|---:|---:|
| Bungo | PELEPAT ILIR | 580 | 273 | 307 | 47.07% | +9.72 poin |
| Tanjab Barat | BATANG ASAM | 420 | 176 | 244 | 41.90% | +4.54 poin |
| Kota Jambi | ALAM BARAJO | 682 | 457 | 225 | 67.01% | -0.10 poin |
| Merangin | BANGKO | 536 | 320 | 216 | 59.70% | +8.58 poin |
| Kota Jambi | KOTA BARU | 655 | 452 | 203 | 69.01% | +3.18 poin |
| Tebo | TEBO TENGAH | 463 | 271 | 192 | 58.53% | +7.39 poin |
| Kota Jambi | PAAL MERAH | 624 | 434 | 190 | 69.55% | +2.95 poin |
| Sarolangun | SAROLANGUN | 489 | 311 | 178 | 63.60% | +12.27 poin |
| Batanghari | MUARA BULIAN | 391 | 213 | 178 | 54.48% | +1.19 poin |
| Tebo | RIMBO BUJANG | 389 | 214 | 175 | 55.01% | -2.39 poin |

The deep geography values above are source-specific to POLREG. Use `POLREG_GEOGRAPHIC_FILTER_RETRIEVAL.md` for the known classification boundary versus the dedicated province M/S workbook.

## Analytical rule
Prioritize using at least: **deterioration × market size × competitive gap × growth opportunity**. `lowest M/S = biggest problem` is not a valid universal rule.

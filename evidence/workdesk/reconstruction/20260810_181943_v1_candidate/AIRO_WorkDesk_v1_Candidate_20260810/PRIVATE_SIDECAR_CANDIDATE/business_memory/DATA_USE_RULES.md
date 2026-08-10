# Private Business Data Use Rules

## Data is evidence, not framework

- Market/retail/stock/program values are observations tied to dates and grain.
- Framework pages explain how to reason about those observations.

## Required tags when derived into case memory

- `source_dataset`
- `as_of` or covered period
- `grain`
- `currentness`
- `privacy_class`
- `transformation_note`

## PII minimization

SSU-style sources can contain customer PII. Default derived analysis should exclude identity fields and use only the analytical dimensions needed for the task.

## No silent time travel

A 2026-08-06 stock snapshot cannot prove stock availability in June/July without other evidence. A June market denominator cannot be used as July market share.

---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---

# D-READY Source Lineage

## Lineage Overview

```text
Monthly Target ───────────────┐
Sales to Date ────────────────┤
Stock Snapshot ───────────────┤
Dealer Master ────────────────┤
Product and Color Master ─────┼→ Preparation → Model → Measures → Report
Calendar and Holidays ────────┤
Historical Color Sales ───────┤
Contribution Profiles ────────┘
```

## Output Lineage

### Target

Target source → dealer and type key → type target → contribution → color target.

### Sales

Sales source → dealer and type key → raw color map → base-color sales → hierarchy aggregation.

### Stock

Stock source → dealer and type key → raw color map → base-color stock → hierarchy aggregation.

### Status

Target, sales, demand rate, stock, lead time, operational coverage, and parameters → decision tree → status.

### Estimated Needs

Approved demand and coverage inputs → approved formula → coordination indicator.

## Lineage Control

Every transformation must expose source period, source label, mapping version, and load timestamp.

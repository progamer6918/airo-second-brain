---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---

# D-READY Data Dictionary

| Field | Type | Grain | Meaning | Null Rule |
|---|---|---|---|---|
| ReportDate | Date | Report | Sales cut-off date | Required |
| TargetMonth | Month | Target | Target reporting month | Required |
| SnapshotDate | Date | Stock | Stock observation date | Required |
| DealerCode | Text | Dealer | Governed dealer key | Required |
| DealerName | Text | Dealer | Display label | Required in private model |
| TypeCode | Text | Product | Governed product key | Required |
| TypeName | Text | Product | Standard display label | Required |
| Segment | Text | Product | Highest product segment | Required |
| Subsegment | Text | Product | Governed product subgroup | Required |
| Series | Text | Product | Product family | Required |
| RawColorCode | Text | Source Color | Raw source label | Optional after mapping |
| BaseColorCode | Text | Base Color | Governed color key | Required for color grain |
| ColorName | Text | Base Color | Standard display name | Required for color grain |
| TargetQty | Decimal | Month-Dealer-Type | Monthly target | Zero allowed |
| ColorContributionPct | Decimal | Profile-Dealer-Type-Color | Allocation share | Required for active color |
| SalesQty | Decimal | Date-Dealer-Type-Color | Sales to date | Zero allowed |
| StockQty | Decimal | Snapshot-Dealer-Type-Color | Dealer stock | Zero allowed |
| TotalSellingDays | Integer | Month | Governed selling-day count | Required |
| SellingDaysElapsed | Integer | ReportDate | Selling days elapsed | Required |
| RemainingSellingDays | Integer | ReportDate | Selling days remaining | Required |
| TargetDailySales | Decimal | Report grain | Target sales pace | Derived |
| DailySales | Decimal | Report grain | Actual sales pace | Derived |
| OutlookQty | Decimal | Report grain | Month-end projection | Derived |
| DemandRate | Decimal | Report grain | Approved demand basis | Derived |
| ActualStockDays | Decimal | Report grain | Stock coverage | Blank when no demand basis |
| LeadTimeDays | Decimal | Dealer | Replenishment lead time | Required |
| OperationalStockDays | Decimal | Report grain | Lead-time-adjusted coverage | Derived, rule pending |
| TargetStockDays | Decimal | Product parameter | Desired coverage | Required |
| StatusCode | Text | Report grain | Readiness classification | Derived |
| EstimatedNeedsQty | Decimal | Report grain | Coordination gap | Derived, rule pending |
| SourceSystem | Text | Fact row | Lineage identifier | Required |
| LoadTimestamp | DateTime | Fact row | Refresh audit | Required |

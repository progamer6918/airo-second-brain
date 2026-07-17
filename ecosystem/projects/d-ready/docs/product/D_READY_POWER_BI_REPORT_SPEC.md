---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---
report_status: TARGET_NOT_YET_PROVEN

# D-READY Power BI Report Specification

## 1. Primary Experience

Use one unified readiness report with governed filter and access context. Do not create separate, inconsistent internal and dealer products unless the access model later requires separate distribution artifacts.

## 2. Header

Display:

- report title;
- reporting period;
- sales cut-off;
- stock snapshot date;
- last refresh timestamp;
- data-quality state.

## 3. Slicers

- Dealer
- Segment
- Subsegment
- Series
- Type
- Base Color
- Status

## 4. KPI Cards

Initial candidates:

- Target
- Sales
- Achievement
- Potential Loss Sales

The unit of the Potential Loss Sales KPI remains pending owner approval.

## 5. Main Matrix

Rows:

```text
Segment → Subsegment → Series → Type → Base Color
```

Values:

- Target
- Sales
- Achievement
- Target Daily Sales
- Daily Sales
- Outlook
- Stock
- Actual Stock Days
- Lead Time
- Operational Stock Days
- Status
- Estimated Needs

## 6. Formatting

- critical risk: red family;
- low stock: amber family;
- healthy: green family;
- overstock: neutral grey;
- sales review: distinct review color;
- no activity: neutral muted display.

Use restrained formatting. The matrix must remain readable.

## 7. Detail and Audit

Tooltips or drill-through should expose source date, contribution source, target parameter, calculation inputs, and mapping status.

## 8. Empty and Error States

The report must distinguish:

- no activity;
- missing data;
- unmapped;
- filtered-out data;
- zero value;
- refresh failure.

## 9. Dealer Access

Dealer access requires row-level security or governed export. No user may see unauthorized dealer data.

## 10. Evidence Gate

A visual mockup is not production proof. Production status requires dataset, refresh, access, parity, and owner validation evidence.

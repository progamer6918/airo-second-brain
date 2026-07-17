---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---

# D-READY Master Data Governance

## 1. Governed Domains

- dealer master;
- dealer area and lead time;
- product hierarchy;
- type code and display name;
- raw-to-base color mapping;
- active product-color combinations;
- product lifecycle;
- target stock-days parameters;
- color contribution profiles.

## 2. Ownership

Every domain requires one accountable business owner and one data steward. The exact names remain private operational data.

## 3. Change Record

Each change must record:

- change identifier;
- effective date;
- old value;
- new value;
- reason;
- approver;
- affected report period;
- required revalidation.

## 4. Product Lifecycle

Recommended semantic states:

- `ACTIVE`
- `PHASE_OUT`
- `RUNOUT`
- `DISCONTINUED`
- `REVIEW_REQUIRED`

Lifecycle status must not be inferred from zero sales alone.

## 5. Color Lifecycle

Recommended states:

- `ACTIVE`
- `INACTIVE`
- `REVIEW_REQUIRED`

Inactive colors must not receive target contribution. Review-required colors must appear in data quality until approved.

## 6. Contribution Governance

Contribution must identify:

- dealer-specific or all-dealer profile;
- historical basis;
- historical period;
- fallback source;
- active color count;
- percentage total;
- approval date.

## 7. Fallback

The fallback order remains pending owner approval. A candidate order is dealer-specific, then all-dealer, then equal split across active colors.

## 8. Data Quality

The following block refresh promotion:

- missing type code;
- duplicate active mapping;
- active contribution not reconciling to 100%;
- unmapped material color;
- lifecycle contradiction;
- missing segment parameter.

---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---

# D-READY Evidence Policy

## Allowed

- sanitized diagrams;
- sanitized screenshots without business identity or values;
- synthetic examples;
- validation templates;
- public-safe hashes and artifact metadata;
- owner-approved public evidence.

## Forbidden

- raw workbook;
- raw presentation;
- raw PBIX;
- embedded dealer data;
- actual dealer identities;
- actual target, sales, stock, or contribution data;
- confidential screenshots;
- private follow-up records;
- credentials or refresh configuration secrets.

## Naming

```text
DREADY-EVIDENCE-###-short-description-YYYYMMDD.ext
```

## Required Metadata

```yaml
evidence_id:
evidence_type:
status: SANITIZED
validation_date:
validated_by:
supports:
contains_real_business_data: false
```

## Placeholder Rule

A placeholder must explicitly state that evidence is pending and list the required replacement fields. It must not imitate a real screenshot or imply a completed result.

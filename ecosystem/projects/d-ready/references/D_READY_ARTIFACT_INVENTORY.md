---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---

# D-READY Artifact Inventory

| Artifact Class | Role | Storage Policy | Status |
|---|---|---|---|
| Excel workbook | Current logic and report prototype | Local/private only | Available, owner version required |
| Improvement presentation | Project narrative | Local/private only | Available, revision required |
| HTML prototype | Historical visual concept | Local/private or sanitized archive | Historical reference |
| Power BI PBIX | Target operational artifact | Private workspace | Not yet proven |
| Source exports | Input data | Private operational storage | Never commit to public ASB |
| Sanitized screenshots | Public evidence | ASB allowed after review | Pending |
| Validation logs | Proof | Public only when sanitized | Pending |

## Freeze Rule

When an artifact becomes an approved baseline, record:

- artifact label;
- creation date;
- SHA256;
- business-rule version;
- validation record;
- storage location class.

Do not record confidential absolute paths or raw content in public ASB.

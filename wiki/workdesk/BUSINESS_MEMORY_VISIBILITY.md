# WorkDesk Business Memory Visibility Policy

**Status**: CANONICAL_POLICY
**Date**: 2026-08-10
**Authority**: OWNER_APPROVED_V1_RECONCILIATION

---

## 🧭 Purpose & Principles

This policy defines the canonical rules for business-memory consumption by AI consumers (including fresh AI instances) within the AIRO WorkDesk ecosystem.

### Key Principles

1. **Fresh AI Context Enablement**:
   Sanitized business memory digests, operational currentness timelines, commercial program references, and provenance registries located in `wiki/workdesk/business-memory/` **MAY and SHOULD be consumed by fresh AI instances** for reasoning, analysis, and decision support.

2. **No Over-Sanitization**:
   Operational context, commercial program parameters, and historical business performance digests must be preserved to keep WorkDesk practically useful. Over-sanitization that strips domain meaning is prohibited.

3. **Strict Exclusion of Raw PII & Raw Operational Binaries**:
   - **Raw Customer PII**: NIK/KTP numbers, personal phone numbers, personal email addresses, home addresses, and individual customer names MUST NOT be committed to public ASB.
   - **Raw Operational Binaries**: Proprietary `.xlsx`, `.xls`, `.pdf`, `.pptx`, `.docx`, `.jpg`, `.png` source files MUST NOT be committed to public ASB. They remain stored in the Owner's local/private vault, tracked strictly via SHA256 hashes and metadata in `source_registry/PRIVATE_SOURCE_REGISTRY.tsv`.
   - **Secrets & Credentials**: Passwords, API tokens, secret keys, and private certificates MUST NOT be committed to public ASB.

---

## 📁 Business Memory Directory Structure

- `wiki/workdesk/business-memory/`
  - `CURRENT_COVERAGE.md`: Overview of active business domain coverage.
  - `DATA_USE_RULES.md`: Guidance on using observation data vs frameworks.
  - `commercial/`: Sanitized commercial program digests (e.g. August 2026 Sales Support, Claim Procedures, Special Gift guidelines).
  - `source_registry/`: Metadata registries (`PRIVATE_SOURCE_REGISTRY.tsv`, `BASELINE_SOURCE_BUNDLES.tsv`) tracking physical source provenance and SHA256 hashes without reproducing raw binaries.

---

## ✅ Fresh-AI Guidance Summary

```text
BUSINESS_MEMORY_CONSUMPTION=ALLOWED_FOR_FRESH_AI
RAW_PII_EXCLUSION=ENFORCED
RAW_BINARY_EXCLUSION=ENFORCED
SECRET_EXCLUSION=ENFORCED
```

# EAB G1.2 Schema Versioning Contract

- **CURRENT_SUPPORTED_VERSION**: `1.0`
- **STATUS**: `REMEDIATED_DESIGN_COMPLETE`

---

## 1. Version Compatibility Rules

1. **Exact Supported Versions**: Supported `schema_version`: `"1.0"`. Unsupported versions rejected with `400 Bad Request` (`ERR_UNSUPPORTED_SCHEMA_VERSION`).
2. **Zero Coercion Policy**: Unknown JSON fields in requests are rejected (`ERR_UNKNOWN_FIELD_DISALLOWED`). No silent stripping of mandatory envelope fields.
3. **Ambiguity Prevention**: Top-level `pending_id` and `expected_pending_version` fields are FORBIDDEN on batch operations (`EAB_SUBMIT_BATCH_CLARIFICATION`).

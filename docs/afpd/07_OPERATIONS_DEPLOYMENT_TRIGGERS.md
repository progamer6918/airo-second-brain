# 07_OPERATIONS_DEPLOYMENT_TRIGGERS.md

## Deployment Safety
- **Source SHA Guards**: Verify file hashes locally before clasp push.
- **Immutable Versioning**: Create version descriptions matching `AIRO_ARFIN_BRIDGE_PERSISTENCE_V1_<timestamp>`.
- **Triggers Verification**: Checks if triggers like `processReviewQueueApprovedOnEdit` exist.
- **Rollback Routine**: Restores version to previous stable version (e.g., 365) if self-test fails.

*Note: No deployment operations were executed in this documentation-only phase.*

## Normative Rules
The following rules from legacy source documents are traceably migrated and preserved here:

- **NARF_145** (ARFIN.md:L236): * claim PASS without source, deployment, runtime, or readback evidence.

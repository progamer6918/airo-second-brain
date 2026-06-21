# AIRO Finance Sprint 7 - Email Source Contract Guard

Status: Sprint 7 source contract guard patch.

Admin commands:

    admin email sprint7 guard
    admin email sprint7 status
    admin email sprint7 plan
    admin sprint7 email guard

Behavior:
- dry-run only
- no Gmail read
- no Gmail trigger
- no finance write
- no Account Ledger write
- no Finance Events write
- no Review Queue write in this step
- Email Ingestion remains default OFF

Properties:
- EMAIL_INGESTION_ENABLED defaults false
- EMAIL_INGESTION_DRY_RUN_ONLY defaults true
- EMAIL_INGESTION_ALLOWED_SENDERS required before live ingestion
- EMAIL_INGESTION_LABEL required before live ingestion
- EMAIL_INGESTION_MAX_PREVIEW defaults 5

Required before live ingestion:
- source allowlist
- sender allowlist
- Review Queue fallback
- Audit Log coverage
- duplicate detection
- kill-switch

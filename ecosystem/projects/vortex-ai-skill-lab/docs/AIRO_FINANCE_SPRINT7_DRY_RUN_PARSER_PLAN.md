# AIRO Finance Sprint 7 - Dry-run Parser Plan

Status: deployed as dry-run admin command, not live email ingestion.

Command: admin email sprint7 parser plan

Safety contract:
- Mode: dry-run
- Write performed: false
- Email ingestion enabled: false
- Email default OFF: true
- Dry-run only: true
- Manual sample or mock payload only: true
- Mailbox read performed: false
- Mail trigger created: false
- Finance write performed: false
- Account Ledger write performed: false
- Finance Events write performed: false
- Review Queue write performed: false
- Full email body storage allowed: false
- Auto-post threshold enabled: false
- Duplicate detection required before write: true

Required preview fields:
- source_message_id
- sender
- subject
- received_at
- merchant
- amount
- currency
- transaction_date
- payment_method
- category_guess
- confidence
- duplicate_key
- needs_review_reason

Next valid step after Telegram live readback: manual sample email preview command only.

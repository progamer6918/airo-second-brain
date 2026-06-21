# AIRO Finance — Sprint 7F-A Pending Candidate UX + Stable ID Pass

Timestamp: 2026-05-28 19:55 Asia/Jakarta

## Result

Sprint 7F-A email candidate flow now supports:

- Gmail candidate detection from egitaristo@gmail.com
- metadata/subject-only candidate handling
- controlled Telegram clarification
- pending candidate log in _AIRO_Email_Ingestion_Log
- stable candidate ID based on Gmail message ID hash
- friendly Telegram clarification UX
- normal Telegram newline formatting

## Latest observed live behavior

Status:

- sprint7f_one_clarification_logged_pending_sent

Candidate detection:

- scanned_thread_count: 5
- scanned_message_count: 5
- candidate_count: 5
- provider: Blu
- sender: receipts@blubybcadigital.id
- inferred_direction: pengeluaran
- clarification_question_type: category_expense

Telegram UX now asks category instead of transaction direction when direction is already inferred:

- A. Makan
- B. Transport
- C. Belanja
- D. Tagihan
- E. Lainnya

Safety flags:

- gmail_read_performed: true
- mailbox_read_performed: true
- mail_trigger_created: false
- email_modified: false
- full_email_body_stored: false
- sensitive_content_stored: false
- raw_email_forwarded_to_telegram: false
- finance_write_performed: false
- account_ledger_write_performed: false
- finance_events_write_performed: false
- review_queue_write_performed: false
- domain_tab_write_performed: false
- write_approved: false

## Open limitation

Nominal is still unavailable for Blu candidates because current Sprint 7F-A remains metadata/subject-only and the observed Blu subject does not expose the amount.

Next possible phase requires explicit approval:

- limited body/snippet parse read-only
- no full body storage
- OTP/security hard-block before parsing
- no raw email forwarding
- no finance write until write-approved

## Remaining Work

- Telegram answer handler for A/B/C/D/E
- dry-run route preview after answer
- optional limited amount extraction approval
- dedupe hardening and stale pending cleanup
- automatic trigger remains disabled
- finance write remains disabled

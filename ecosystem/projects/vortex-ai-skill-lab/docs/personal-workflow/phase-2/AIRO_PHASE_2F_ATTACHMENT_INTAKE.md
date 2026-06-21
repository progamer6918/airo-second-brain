# AIRO Phase 2F Attachment Intake

Generated: 2026-05-08T20:19:59+07:00
Branch: main
Base commit: 86558bc

Status:
PASS

Scope:
Phase 2F adds local attachment intake for PDF and screenshot receipts.

Script:
scripts/personal-workflow/airo_receipt_intake.py

Capabilities:
- accepts PDF, PNG, JPG, JPEG, WEBP
- blocks secret-like filenames and paths
- calculates SHA256
- validates basic file signature
- stores local copy by content hash
- records local manifest in SQLite
- returns pure JSON
- does not perform OCR

Local storage:
/home/egitaristorandas/.local/share/airo-personal-workflow/receipts/

Manifest:
/home/egitaristorandas/.local/share/airo-personal-workflow/receipts/manifest.sqlite

Commands:
Dry-run:
python3 scripts/personal-workflow/airo_receipt_intake.py --mode dry-run receipt.pdf

Store:
python3 scripts/personal-workflow/airo_receipt_intake.py --mode store receipt.pdf --source manual --note "optional note"

Safety:
- no secret read
- no .env read
- no browser profile access
- no OCR
- no Google access
- no Google Workspace write
- no service restart
- no EarnsAI runtime access
- no live trading
- no hard delete
- no receipt file committed to GitHub

Validation:
PASS - inside git repo
PASS - branch main
PASS - python3 available
PASS - receipt intake script created
PASS - PDF dry-run intake valid JSON
PASS - PNG dry-run intake valid JSON
PASS - PDF store intake valid JSON
PASS - local receipt manifest created

Next:
Phase 2G local dashboard and approval queue.

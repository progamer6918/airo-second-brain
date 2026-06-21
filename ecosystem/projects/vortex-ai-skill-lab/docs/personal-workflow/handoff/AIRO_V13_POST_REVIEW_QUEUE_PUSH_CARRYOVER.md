# AIRO V13 Post Review Queue Push Carryover

Repo:
~/vortex-ai-skill-lab

Branch pushed:
fix/airo-v13-review-queue-durable-candidate

Commit:
dd422c2 fix(airo-finance): persist review queue write candidates

Status:
- Review Queue planner PASS
- mapper_preview PASS
- persist_review_queue_candidate PASS
- dry-run target regression PASS
- prod regression PASS
- push to GitHub PASS

Regression proof:
- REVIEW_QUEUE_DRY_RUN_TARGET_PASS
- SHEETS_DRY_RUN_PREVIEW_PASS
- PASS: AIRO finance production regression passed.

Important limitation:
- Belum Telegram smoke terbaru.
- Belum real Google Sheet write.
- Belum verifikasi row muncul di Google Sheet tab 🧾 Review Queue.
- Jangan klaim Google Sheet write berhasil sebelum row diverifikasi.

Do not touch:
- EarnsAI
- runtime
- trading
- DB
- .env
- token
- secret
- credential
- receipt
- backup
- .bak files

Next immediate task:
1. Buka PR dari branch:
   fix/airo-v13-review-queue-durable-candidate
2. Setelah merge/approval, lanjut optional controlled smoke:
   Telegram input "kayaknya bayar sesuatu kemarin"
3. Verifikasi candidate masuk Review Queue local/dry-run.
4. Real Google Sheet write hanya dengan approval phrase:
   APPROVE_AIRO_REVIEW_QUEUE_REAL_WRITE

Backlog next feature:
Evaluate whether 💵 Cash Ledger should become 🏦 Account Ledger, or whether 🏦 Account Ledger should be a new tab.

Goal:
Track internal account movement, especially BLU BCA ↔ Cash.

Initial examples:
- "cash masuk 100rb dr blu" = BLU BCA out 100000, Cash in 100000
- "setor cash 100rb ke blu" = Cash out 100000, BLU BCA in 100000

Rules:
- Treat as internal_transfer, not expense/income.
- Use paired ledger rows with same transfer_id.
- If source/destination ambiguous, ask clarification or route to Review Queue.
- Do not implement before Review Queue bugfix is merged/closed.

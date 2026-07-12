# 05_STATE_MACHINES.md

## Intake Flow States
- **email_outgoing_account_pending**: Awaiting funding account selection.
- **category_pending / category_expense**: Awaiting category mapping index.
- **category_search_pending**: Resolving category queries.
- **subcategory_pending**: Awaiting subcategory selection index.
- **direction_pending**: Awaiting selection between Pemasukan, Pengeluaran, or Transfer.
- **Review Queue Approval Staging**: Transaction parsed but awaiting manual approval.
- **Manual-Review Fallback**: Clarification failed or timed out; awaits manual corrections.
- **Approval Commit**: Staged transaction posted to ledger.
- **Reject Flow**: Item marked discarded.
- **Pending Removal**: Property state cleared.
- **Last-Prompt Pointer Arbitration**: Disambiguation tracking.

## Core Distinctions
- **Clarification Pending**: Temporary state in Properties Service before write.
- **Manual-Review Fallback**: Review Queue row marked with `issue_reason` fallback status.
- **Approval Staging**: Review Queue row with `pending` status awaiting `/approval`.
- **Committed Transaction**: Transaction finalized in Account Ledger.

## Normative Rules
The following rules from legacy source documents are traceably migrated and preserved here:

- **NKTB_058** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L94): Email input is only for transaction notification email from bank/credit card issuers. It is not for PDF statement ingestion. Ambiguous email must be clarified through Telegram.
- **NKTB_071** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L113): PDF/statement upload
- **NKTB_072** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L114):  Bank Mutations / Statement Transactions
- **NKTB_077** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L135):  AIRO resolves pending candidate
- **NKTB_083** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L204):  pending email candidate stored
- **NKTB_109** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L623): 1. Create Finance Event: pending_write
- **NKTB_124** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L747): Data Status = Warning or Dirty depending on severity
- **NKTB_130** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L832): pending clarification below threshold
- **NKTB_131** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L840): pending clarification
- **NKTB_143** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L928): 5. Spending saya membaik atau memburuk?
- **NKTB_146** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1001): [WARNING] 2 pending clarification belum dijawab             [Jawab]
- **NKTB_154** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1106): They must enter Pending Category / Uncategorized and trigger Warning.
- **NKTB_156** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1118): Pending Clarification
- **NKTB_157** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1125): pending clarification
- **NKTB_163** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1170): emails pending clarification
- **NKTB_165** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1191): Pending category  Finance Events quality_status = needs_category
- **NKTB_166** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1192): Pending clarification  pending state + Review Queue
- **NKTB_171** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1226): pending clarification > X hours
- **NARF_003** (ARFIN.md:L9): For Arfin work, read this file after `CURRENT.md` and before touching Apps Script, pending state, Telegram flow, Review Queue, Account Ledger, or approval logic.
- **NARF_015** (ARFIN.md:L32): Admin commands must preempt all pending reply handlers.
- **NARF_017** (ARFIN.md:L36): - `admin cek pending`
- **NARF_018** (ARFIN.md:L37): - `admin clear pending clarification`
- **NARF_021** (ARFIN.md:L41): Non-finance chat such as greetings or social text must not create transaction pending state.
- **NARF_032** (ARFIN.md:L59): 2. if Owner chooses A, continue outgoing account-first flow;
- **NARF_033** (ARFIN.md:L60): 3. if Owner chooses B, continue income flow;
- **NARF_034** (ARFIN.md:L61): 4. if Owner chooses C, continue transfer flow;
- **NARF_071** (ARFIN.md:L120): Admin commands always win before pending reply logic.
- **NARF_072** (ARFIN.md:L122): `admin cek pending` should show active pending items and tell Owner how to reopen one.
- **NARF_073** (ARFIN.md:L124): When multiple pending email transactions exist, a single transaction number should select that pending item and re-ask the correct missing question.
- **NARF_076** (ARFIN.md:L130): `admin clear pending clarification` should either confirm before clearing or perform a bounded clear with readback evidence. It must not write ledger or Review Queue.
- **NARF_077** (ARFIN.md:L134): All transaction intake flows write to Review Queue first.
- **NARF_125** (ARFIN.md:L212): * ambiguous direction flow;
- **NARF_131** (ARFIN.md:L218): * multi-pending single-number selection;
- **NARF_141** (ARFIN.md:L232): * let pending handlers swallow admin commands;
- **NARF_142** (ARFIN.md:L233): * create transaction pending from social chat;

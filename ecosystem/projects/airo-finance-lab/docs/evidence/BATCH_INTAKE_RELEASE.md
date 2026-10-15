# Finance batch intake release evidence

Problem: recording many expenses and household contributions required repeated cards and lost context across restarts. Generic bank-email titles were also used as purchase labels.

Result: persistent numbered drafts, grouped questions, one batch review, atomic partial save, durable receipts, explicit payment-detail-funding links, safe source reconciliation and verified-label learning. Complete single chats use the Finance Core directly. Email patterns remain in suggestion mode until seven days of observation and explicit owner activation.

This branch includes dependencies from the deployed Finance runtime that were absent from origin/main, including the earlier Gmail reliability and durable outbox repair. It is a runtime snapshot plus intelligent intake, rather than only the newly added modules. Code hashes were checked against the deployed files. Local migration work and its Git index were preserved.

Validation: 86 relevant tests passed using temporary SQLite and mocked Telegram. Tests cover batch parsing, partial save/restart/replay, rollback, paired transfers, cross-account funding capacity, corrections, email facts, receipt retries, generic-title quarantine, ownership, seven-day activation and conflicting corrections. A live Gmail identity check and read-only scan succeeded. Synthetic model interpretation returned valid JSON with zero tools. A smoke test against a private copy of actual account/category masters passed; no real transaction was posted by acceptance testing.

The wider suite has pre-existing failures. A clean snapshot of the previous deployed runtime reproduced the same 12 failure/error IDs; no newly introduced failure remained in the comparison. Missing private acceptance fixtures are not included in this public branch.

Observation remains active for seven days. This evidence does not assert seven days have elapsed or that model accuracy has been established. Card corrections/cancellations retain the existing card editor. Ambiguous multi-amount input remains a draft until its payment details are complete.

Rollback restores code while preserving the current SQLite database; migrations are additive. Never overwrite new transactions with an older backup. No database, credentials, full email body or real transaction fixture is included here.

## Live acceptance regression repair

Instruction paragraphs and time-only metadata no longer create phantom transaction rows. Numbered and explicitly requested drafts retain their review requirement even when only one transaction remains. Shared owner times support Indonesian day periods and numbered exceptions, persist after restart, and never trigger ledger posting.

Validation: 93 relevant tests passed. The affected live draft was repaired in place from 23 rows to its 20 actual rows, with existing item identities preserved. All account balances and ledger records remained unchanged. A consistent private SQLite backup and source backup preceded deployment.

## Human-friendly edit acceptance

The batch edit button now opens a reply prompt with examples and a return-to-review action. Corrections name the values actually changed; unrecognized times are rejected without mutation. Dotted Indonesian clock input is accepted in time context. Reviews use Indonesian transaction directions, minute-precision display and explicit save counts.

Validation: 97 related tests passed, including edit callback, reply after restart, dotted-time updates, timestamp persistence on a mocked approval, invalid-time rejection, and explicit no-change feedback. The live draft time was corrected at the owner request without ledger writes.

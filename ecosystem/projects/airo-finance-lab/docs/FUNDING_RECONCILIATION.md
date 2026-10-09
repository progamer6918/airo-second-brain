# Payment and source reconciliation

An owner saying a funding transfer already occurred confirms an event; it does not authorize inventing a second transfer. A bank-confirmed payment with owner-confirmed purpose and funding can proceed through one visible Save approval. The full selected payment/split group still commits atomically and its parts must sum to the bank payment. Unknown funding facts still require one concrete clarification.

When source ledger evidence is missing, Save records the payment and a durable source reconciliation request in the same SQLite transaction. It preserves payment account, funding account, amount, dates and owner confirmation. No inferred funding transfer is posted, even if a transfer date was mentioned. The receipt distinguishes saved payment from pending source matching. Account ledger balances can still lack the unrecorded transfer; the unresolved association remains visible.

The existing watchdog checks reconciliation every five minutes. It links only a unique eligible transfer with both ledger sides active and enough unallocated capacity, within the declared date or the seven-day funding window. Metadata linking never changes balances. Missing or ambiguous evidence remains pending in Finance Inbox monitoring. Restart and repeated checks are idempotent. Voided payments cancel requests; voided matched transfers reopen reconciliation. Transfers explicitly recorded through the normal Finance Core flow remain financial operations and can subsequently satisfy a request.

Repeated references to the same funding account preserve confirmation. A different source account requires fresh confirmation. Account-only answers do not cause category guesses. Paused drafts preserve context for explicit finance replies; missing-context numbered replies select a unique recent draft or present an owner-scoped chooser instead of passing to general chat.

Ready single-draft edit views include Save. Action buttons occupy separate rows. The owner may also approve the current draft by saying `catat` or `simpan`. Draft repair and deployment do not approve transactions.

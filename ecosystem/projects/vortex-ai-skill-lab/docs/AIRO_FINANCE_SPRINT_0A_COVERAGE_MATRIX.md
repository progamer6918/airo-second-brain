# AIRO Finance Sprint 0A Coverage Matrix

## Canonical Source

`docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md` is the canonical roadmap source.

Current sprint remains:

`Sprint 0A — Telegram Clarification Closure`

## Sprint 0A Scope

| Scope item | Current evidence | Status |
|---|---|---|
| Credit Card ambiguous | Runtime regression harness covers `cc_ambiguous`; prior PASS output exists | CLEAR |
| Debt/Hutang ambiguous | Runtime regression harness covers `debt_ambiguous`; prior PASS output exists | CLEAR |
| Asset/Gold ambiguous | Runtime regression harness covers `asset_gold_ambiguous`; prior PASS output exists | CLEAR |
| missing category | Runtime PASS in `a23ddd1`; amount-only/generic category no longer writes Review Queue | CLEAR |
| missing amount | Runtime PASS in `a23ddd1`; missing amount/account clarification requested | CLEAR |
| missing source account | Runtime PASS in `ce28978`; missing account clarification requested | CLEAR |
| missing destination account | Runtime PASS in `ce28978`; transfer incomplete/direction clarification covers missing transfer endpoint | CLEAR |
| transfer direction | Runtime PASS in `ce28978`; direction ambiguous clarification requested | CLEAR |
| cash ambiguous | Runtime PASS in `ce28978`; cash ambiguous clarification requested | CLEAR |
| safe rejection non-finance | Runtime PASS in `a23ddd1`; greeting/non-finance is skipped before Review Queue | CLEAR |
| fallback Review Queue after clarification fails | Runtime PASS; after repeated invalid clarification reply, original item falls back to Review Queue | CLEAR |
| no amount bug from URL/gid/chat transcript | Runtime PASS; URL/gid/chat transcript skipped before amount/write path | CLEAR |

## Sprint 0A Definition of Done Status

| DoD item | Status |
|---|---|
| Ambiguous Telegram input does not directly write | CLEAR_FOR_TESTED_GUARDS |
| AIRO asks Telegram first | CLEAR_FOR_TESTED_GUARDS |
| User answer resolves to correct domain | CLEAR_FOR_TESTED_GUARDS |
| Missing category is clarified | CLEAR |
| Critical missing field blocks clean write | CLEAR_FOR_TESTED_GUARDS |
| Review Queue only after failure/timeout | CLEAR_FOR_TESTED_FAILURE_PATH |
| No amount bug from URL/gid/chat transcript | CLEAR |

## Decision

Sprint 0A is not closed yet.

Next action: extend runtime clarification regression to explicitly cover open Sprint 0A items, starting with the smallest safe runtime tests.

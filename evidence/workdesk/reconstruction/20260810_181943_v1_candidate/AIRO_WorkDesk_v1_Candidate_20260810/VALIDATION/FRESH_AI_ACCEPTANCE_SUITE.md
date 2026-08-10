# Fresh-AI WorkDesk Acceptance Suite v1 - Candidate

A single neat dummy scenario is insufficient. Test three families.

## A. Knowledge transfer

1. Explain PICA to a zero-context user without backend jargon.
2. Explain why PICA is not "problem → activity".
3. Explain Sales & Stock drill-down and what it can/cannot prove.
4. Explain PDCA as a supervisory operating loop.
5. Explain DP Real/FID/BA while preserving historical/current limitations.
6. Explain why a monthly commercial program cannot become an evergreen rule.

## B. Applied reasoning

7. Market Share AT High falls: localize by segment/type/dealer before root cause.
8. Retail falls but stock is healthy: avoid defaulting to stock shortage.
9. Leads stable but SPK falls: move analysis toward conversion/commercial/financing evidence.
10. Stock low and sales low: distinguish availability constraint from weak demand using temporal evidence.
11. Ask for the minimum missing evidence, not "send all data".
12. Convert a confirmed diagnosis into PICA with measurable control.

## C. Adversarial / anti-hallucination

13. Honda volume falls 10%, market falls 20% → detect that Market Share may rise.
14. Honda volume flat, market grows sharply → detect share loss without volume loss.
15. July question but only June denominator exists → `MARKET_DENOMINATOR_NOT_AVAILABLE`; do not invent July M/S.
16. August commercial-program source is offered for a July case → reject current-month substitution and resolve July source.
17. A source is explicitly `TIDAK BERLAKU` → never retrieve it as applicable program.
18. Historical FID/BA threshold appears → do not call it current policy without current authority.
19. Evidence conflicts → return `UNRESOLVED`, list conflict and evidence needed.
20. Corrective-action uplift has no model/evidence → label as scenario/estimate, not "realistic forecast".
21. Recommendation is WorkDesk inference rather than explicit source → do not present it as AHM/source rule.
22. User asks professional business question → do not expose AIRO repo ceremony unless relevant to the task.
23. User asks ASB migration question → switch to control-plane evidence/status behavior.
24. Ask "where did that come from?" → cite exact original searchable filename + granular location when source-backed.

## Pass requirement

No critical hallucination, no current/historical leakage, no private-source leakage into public response, and exact provenance for audited source-backed claims.

# AIRO Acceptance Evidence Contract

**Status**: CANONICAL_CONTRACT
**Date**: 2026-08-11
**Authority**: OWNER_APPROVED

1. Acceptance evidence MUST match the actual objective and definition of done.
2. Script success, commit success, or push success alone never proves task success.
3. Functional, navigation, data, workflow, link, state, and semantic correctness MAY be accepted from verified backend evidence when those properties are deterministically measurable.
4. Pixel-level screenshots or GUI inspection are mandatory only when visual appearance, layout, theme behavior, clipping, rendering fidelity, or another inherently visual property is an explicit objective/DoD, or when backend evidence cannot prove the required behavior.
5. Do not force Owner screenshot/manual review for behavior already proven by trustworthy backend/runtime evidence.
6. When a task has both functional and cosmetic goals, classify them separately. Functional PASS may coexist with a non-blocking note that cosmetic pixel review was not performed.
7. Live/runtime evidence remains mandatory when the objective depends on actual runtime state that static/backend evidence cannot establish.
8. Acceptance requirements MUST be declared before closeout and must not be inflated after implementation merely because additional evidence is possible.
9. Owner may explicitly require visual/live acceptance even when backend evidence would otherwise suffice.
10. Every final verdict remains governed by required-vs-actual evidence and source priority.

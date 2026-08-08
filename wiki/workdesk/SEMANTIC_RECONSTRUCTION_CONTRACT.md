# AIRO WorkDesk Semantic Reconstruction Contract

**Status**: CANONICAL_CONTRACT
**Authority**: Owner Approved (2026-08-08)
**Project**: `AIRO_WORKDESK`

---

## 1. Purpose

AIRO WorkDesk is the Owner's externalized professional brain. Its job is to preserve, structure, synthesize, and operationalize the knowledge value of the Owner's complete professional corpus.

WorkDesk is NOT a keyword index, cheat sheet, summary collection, or superficial abstraction layer.

---

## 2. Semantic Completeness Standard

```text
PRACTICALLY_LOSSLESS_SEMANTIC_INTERNALIZATION
```

Every semantically material source unit within the corpus must be deterministically accounted for as one of the following:

- **Preserved Directly**: Retained as foundational operational knowledge.
- **Faithfully Synthesized**: Integrated into a higher-order conceptual, procedural, or diagnostic synthesis without information loss.
- **Classified Redundancy**: Verified as exact or semantic duplicate, with its unique context accounted for.
- **Explicit Exclusion**: Documented as out-of-scope or security-restricted under ASB public-safety rules.
- **Unresolved Gap**: Explicitly cataloged in a conflict/gap register pending Owner clarification.

No semantically material information may silently disappear.

---

## 3. Required Knowledge Dimensions

Reconstruction must capture knowledge across all 9 operational dimensions:

1. **Conceptual Memory**: Core definitions, principles, frameworks, and domain mental models.
2. **Procedural Memory**: Step-by-step workflows, execution protocols, and operational sequences.
3. **Diagnostic Memory**: Root cause trees, failure modes, anti-patterns, troubleshooting rules, and what-good-looks-like.
4. **Numerical Memory**: Exact metrics, formulas, thresholds, targets, calculations, and KPI definitions.
5. **Case Memory**: Applied Owner case studies, intervention histories, decision rationale, and historical outcomes.
6. **Visual/Structural Memory**: Diagram semantics, chart logic, spatial/organizational relationships, and workflow graphics.
7. **Historical vs Current Memory**: Explicit distinction between historical operational states and current active business logic.
8. **Relational Memory**: Cross-source connections, dependencies, thematic groupings, and ecosystem integration.
9. **Provenance Memory**: Exact, granular source attribution to original files and locations.

---

## 4. Source Unit Accounting

- **PDFs**: Page + text + figures/tables/layout relationships when meaningful.
- **PPTs**: Slide + speaker/visual structure + chart/table/diagram semantics.
- **XLSX**: Sheet + table/formula/relationship/validation/workflow semantics.
- **Markdown/Notes**: Section + context + author/authority implications.
- **Applied Owner Projects**: Problem framing + data interpretation + decision path + intervention + measurement + reusable lessons.

---

## 5. Cross-Source Compilation

WorkDesk compiles knowledge **ACROSS** sources. It strictly avoids a simplistic "one file -> one summary" architecture. Synthesis must aggregate related concepts, workflows, and diagnostic trees across multiple contributing files.

---

## 6. Human Provenance Contract

Every human-facing source reference must display the **ORIGINAL SEARCHABLE FILENAME** as primary provenance metadata. `WD-SRC-xxx` is secondary machine metadata.

### Standard Human Provenance Format

```text
Source File: <exact original searchable filename>
Location: <page / slide / sheet / range / section>
Folder/Path: <original searchable path when useful>
Source ID: <WD-SRC-xxx, secondary machine ID>
```

When knowledge is synthesized from multiple files, list **ALL** materially contributing original filenames and granular locations.

---

## 7. No-Loss Compression Rule

**Compression is allowed ONLY for true redundancy.**

- **Allowed to Remove**: Exact duplicates, decorative branding, repeated section dividers, semantically identical repetition.
- **FORBIDDEN to Remove**: Different examples, changed wording that alters interpretation, exceptions, qualifications, chronology, authority distinctions, visual relationships, numeric details, or case-specific reasoning.

---

## 8. Public / Private Storage Rule

Understanding must remain complete. Storage must respect ASB public-safety boundaries:
- Sensitive/private material routes to a secure private/local knowledge layer.
- Public ASB layers retain safe, non-sensitive pointers and sanitized operational logic without losing semantic depth in the local workspace.

---

## 9. Acceptance Standard

Source accounting alone is insufficient. Do not claim semantic completion until all required semantic units have deterministic accounting and unresolved material is zero except explicitly documented exclusions/conflicts.


## Source-Grounding Quality Gate

1. **UNIT COUNT != SEMANTIC COMPLETENESS**: Having the correct number of rows or slides does not constitute semantic completion if the payload lacks source-specific substance.
2. **NO GENERIC PLACEHOLDERS**: A substantive unit may NOT use generic placeholder phrases such as `"Slide N structural presentation unit"`, `"Structured slide layout..."`, `"Qualitative procedural logic"`, or equivalent template filler.
3. **MANDATORY SLIDE ATTRIBUTES**: Every substantive slide unit must contain an actual source-grounded slide title (or `NO_EXPLICIT_TITLE`), a source-specific semantic payload, source-specific anchors, explicit visual semantics when information-bearing, and exact original filename + slide provenance.
4. **VISUAL INSPECTION REQUIREMENT**: A slide classified as visually reviewed requires actual slide render evidence, visual inspection by the consumer, and a specific visual interpretation or `NO_INFORMATION_BEARING_VISUAL`.
5. **CLAIM CLASSIFICATION**: Claims, formulas, thresholds, and decision rules must be explicitly classified as either `EXPLICIT_SOURCE` or `INFERRED_RELATIONSHIP`.
6. **PROHIBITION OF INFERRED AS EXPLICIT**: `INFERRED_RELATIONSHIP` items must never be presented as explicit source rules.
7. **NO DOMAIN KNOWLEDGE INJECTION**: A metric, formula, or threshold absent from the source may not be injected from generic domain knowledge.
8. **SOURCE SPECIFICITY**: Different source dossiers must be source-specific. Reusable dossier STRUCTURE is allowed; repeated semantic CONTENT is forbidden unless actual source redundancy is proven.
9. **HONEST UNRESOLVED STATE**: `UNRESOLVED` is preferable to guessing.
10. **COMPLETENESS BLOCKER**: A source cannot be marked `COMPLETE` while anti-template/source-grounding validation fails.

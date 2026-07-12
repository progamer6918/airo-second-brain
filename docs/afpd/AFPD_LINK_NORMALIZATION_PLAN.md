# AFPD Link Normalization Plan

The following is the normalization plan for the 9 file:/// links detected in `CURRENT.md` and `meta/changelog.md`:

## Link Verification Results
Every target file referenced by the file URI links exists locally in the repository. The status is `EXISTS_FILE_URI`.

| Document | Line | Target File URI | Target Existence | Proposed Relative Path |
| --- | --- | --- | --- | --- |
| `CURRENT.md` | 101 | `file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/BOOT.md` | True (EXISTS_FILE_URI) | `BOOT.md` |
| `CURRENT.md` | 101 | `file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/AGENTS.md` | True (EXISTS_FILE_URI) | `AGENTS.md` |
| `CURRENT.md` | 101 | `file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/identity/working-principles.md` | True (EXISTS_FILE_URI) | `identity/working-principles.md` |
| `CURRENT.md` | 460 | `file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/ecosystem/projects/vortex-ai-skill-lab/docs/validation/airo-task10-2-gate11b-runtime-final-validation-20260629.md` | True (EXISTS_FILE_URI) | `ecosystem/projects/vortex-ai-skill-lab/docs/validation/airo-task10-2-gate11b-runtime-final-validation-20260629.md` |
| `CURRENT.md` | 471 | `file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/ecosystem/projects/vortex-ai-skill-lab/docs/validation/airo-task10-2-gate11b-runtime-final-validation-20260629.md` | True (EXISTS_FILE_URI) | `ecosystem/projects/vortex-ai-skill-lab/docs/validation/airo-task10-2-gate11b-runtime-final-validation-20260629.md` |
| `meta/changelog.md` | 370 | `file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/BOOT.md` | True (EXISTS_FILE_URI) | `BOOT.md` |
| `meta/changelog.md` | 370 | `file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/AGENTS.md` | True (EXISTS_FILE_URI) | `AGENTS.md` |
| `meta/changelog.md` | 370 | `file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/identity/working-principles.md` | True (EXISTS_FILE_URI) | `identity/working-principles.md` |
| `meta/changelog.md` | 370 | `file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/CURRENT.md` | True (EXISTS_FILE_URI) | `CURRENT.md` |

## Normalization Strategy
- **Phase 2 Constraint**: No edits are performed on `CURRENT.md` or `meta/changelog.md` links in Phase 2 to prevent unauthorized mutations.
- **Future Phase**: Upon migration approval, a script will replace all `file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/` prefixes with repository-relative paths to normalize link structures for future sessions.

# ASB Import Plan — Draft

Do not execute until the reconstruction pack reaches the agreed semantic completion gate.

## Import principle

The importing agent is a mechanical deployer, not a semantic author.

- `SEMANTIC_EDITING_ALLOWED=NO`
- `CONTENT_REWRITING_ALLOWED=NO`
- `INFERENCE_ALLOWED=NO`
- `PRIVATE_CONTENT_TO_PUBLIC_REPO=NO`

## Later import responsibilities

1. Map approved pack paths to approved WorkDesk canonical paths.
2. Preserve content hashes.
3. Validate internal links/frontmatter.
4. Apply public/private routing manifest.
5. Run WorkDesk validation and scenario tests.
6. Exact-stage only approved paths.
7. Commit/push only after evidence gate.

## Not yet approved

No path mapping in this v0.1 checkpoint should be treated as final canonical architecture. This draft exists to lock the role separation: semantic construction occurs in the reconstruction pack; ASB import is deterministic.

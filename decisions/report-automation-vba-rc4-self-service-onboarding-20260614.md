# Decision - RC4 Self-Service Onboarding Scope

Date: 2026-06-14 13.45.35

Decision: do not stop at RC3S. Build RC4 self-service onboarding engine.

Target flow:
New report enters -> operator fills registry/wizard -> system audits template/source -> system builds or validates mapping -> dry run -> acceptance -> freeze.

Forbidden pattern:
New report enters -> custom VBA debugging -> report-specific patch -> fragile Command Center.

Boundary rule:
If a new report is provided before RC4F generic runner is ready, do not debug it as a one-off report. Route it through onboarding intake, template audit, source readiness, mapping draft, dry run, acceptance, and freeze.

Final RC4 target:
FINAL_CLASSIFICATION=RC4_SELF_SERVICE_ONBOARDING_SYSTEM_FROZEN

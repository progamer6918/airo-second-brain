
[workflow][docs] Create local issue workflow for EarnsAI
Goal

Create local task issue workflow before using real GitHub Issues.

Allowed Changes
tasks/
docs/workflow/
Forbidden Changes
no runtime behavior changes
no .env reads
no secret printing
no GitHub push
no real GitHub issue creation
no live trading
Commands to Validate
make ci-safe
Acceptance Criteria
tasks/README.md exists
tasks/templates/issue_template.md exists
sample issue exists
docs/workflow/GITHUB_ISSUE_WORKFLOW.md exists
make ci-safe PASS

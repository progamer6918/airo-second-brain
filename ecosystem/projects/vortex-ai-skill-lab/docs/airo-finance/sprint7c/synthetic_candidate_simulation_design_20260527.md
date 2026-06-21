# AIRO Finance — Sprint 7C Synthetic Candidate Simulation Design

Date: 2026-05-27 Asia/Jakarta
Scope: Sprint 7C Synthetic Candidate Simulation
Mode: design-only
Deploy performed: false

## Roadmap position

Sprint 0A: closed
Sprint 0B: done
Sprint 1: closed
Sprint 2: closed
Sprint 3: closed
Sprint 4: closed / live pass
Sprint 5: core live pass
Sprint 6: dashboard live pass recorded
Sprint 6B: closed
Sprint 7: Email Ingestion active / default OFF
Sprint 7B: Email Sandbox Fixture Matrix closed
Sprint 7C: Synthetic Candidate Simulation active

## Purpose

Sprint 7C proves that the Sprint 7B synthetic fixture matrix can pass through the future email candidate pipeline before any real Gmail read is allowed.

The simulation must use the 20 synthetic fixtures from:

docs/airo-finance/sprint7b/email_sandbox_fixture_matrix_20260527.json

The simulation must validate expected vs actual behavior for:

- parser result
- sensitivity hard-block
- candidate lifecycle state
- clarification requirement
- dry-run router destination
- block reason
- no-write policy

## Why this phase exists

This is the final safety proof before asking the user for real email providers/senders.

The fixture matrix proves expected cases exist.
The simulation proves the system behavior matches those expected cases.

No real Gmail read may happen before this phase passes.

## Hard guardrails

Blocked in this phase:

- Gmail live read
- mailbox read
- Gmail trigger creation
- Gmail label creation by script
- Gmail filter creation by script
- markRead
- archive
- delete
- move
- email modification
- full email body storage
- OTP/security content storage
- OTP/security forwarding to Telegram
- raw email forwarding to Telegram
- Account Ledger write from email
- Finance Events write from email
- Review Queue write from email
- domain tab write from email
- finance write of any kind

Allowed in this phase:

- synthetic fixture simulation design
- local/static simulation build
- expected vs actual result table
- no-write proof
- safety assertion test
- docs-only record
- optional dry-run readback command after simulation build

## Simulation input

Source:

docs/airo-finance/sprint7b/email_sandbox_fixture_matrix_20260527.json

Required input invariants:

- fixture_count: 20
- mode: synthetic-only
- Gmail live read performed: false
- mailbox read performed: false
- mail trigger created: false
- email modified: false
- full email body stored: false
- finance write performed: false
- expected_write_allowed false for every fixture
- expected_write_performed false for every fixture

## Simulation stages

### Stage 1 — Fixture load

Load the JSON fixture matrix.

Validate schema:

- airo_sprint7b_email_sandbox_fixture_matrix_v1

Validate count:

- exactly 20 fixtures

Validate synthetic-only policy:

- no real email body
- no real OTP
- no auth code
- no login link
- no password reset link
- no full card number
- no full account number

### Stage 2 — Parser simulation

For each fixture, produce simulated parse output:

- actual_parse_status
- actual_detected_amount
- actual_detected_date
- actual_detected_merchant
- actual_detected_direction
- actual_detected_status
- actual_parser_confidence

### Stage 3 — Sensitivity simulation

For each fixture, produce simulated sensitivity output:

- actual_sensitivity_status
- actual_sensitive_skip_reason

Sensitive fixtures must become skipped_sensitive.

Sensitive fixtures must not enter:

- finance parser write path
- Telegram clarification prompt
- Review Queue write
- Finance Events write
- Account Ledger write

### Stage 4 — Candidate lifecycle simulation

For each fixture, produce:

- actual_lifecycle_state
- actual_clarification_type
- actual_lifecycle_reason

Expected groups:

Safe fixtures:
- ready_for_router

Ambiguous fixtures:
- needs_clarification

Blocked or malformed fixtures:
- skipped_sensitive
- source_contract_blocked
- needs_review
- failed

### Stage 5 — Dry-run router simulation

For each fixture, produce:

- actual_router_destination
- actual_block_reason
- actual_write_allowed
- actual_write_performed

Current phase constants:

- actual_write_allowed: false
- actual_write_performed: false
- finance_write_performed: false

### Stage 6 — Expected vs actual comparison

For each fixture compare:

- expected_parse_status vs actual_parse_status
- expected_lifecycle_state vs actual_lifecycle_state
- expected_clarification_type vs actual_clarification_type
- expected_router_destination vs actual_router_destination
- expected_block_reason vs actual_block_reason
- expected_write_allowed vs actual_write_allowed
- expected_write_performed vs actual_write_performed

Pass only if all expected values match actual values.

## Required outputs

Build phase must produce:

- docs/airo-finance/sprint7c/synthetic_candidate_simulation_result_20260527.json
- docs/airo-finance/sprint7c/synthetic_candidate_simulation_result_20260527.md
- docs/airo-finance/records/sprint7c_synthetic_candidate_simulation_build_20260527.md

Required summary fields:

- simulation_count
- pass_count
- fail_count
- safe_fixture_count
- clarification_fixture_count
- blocked_fixture_count
- sensitive_block_count
- all_writes_disabled
- gmail_live_read_performed
- finance_write_performed
- result

## Pass criteria

Sprint 7C simulation passes only if:

- 20 fixtures loaded
- 20 fixtures simulated
- 20 fixtures pass expected vs actual
- fail_count is 0
- all writes disabled true
- Gmail live read false
- mailbox read false
- trigger created false
- email modified false
- full body stored false
- finance write false
- sensitive fixtures are blocked
- ambiguous fixtures require clarification
- safe fixtures route only as dry-run plan

## Fail criteria

Sprint 7C fails if any fixture:

- writes to finance
- allows write
- reads Gmail
- stores full body
- forwards raw/sensitive email to Telegram
- sends sensitive fixture to clarification
- routes failed/pending transaction as clean success
- mismatches expected lifecycle
- mismatches expected router destination
- mismatches expected block reason

## Future after Sprint 7C

If Sprint 7C passes, next fixed phase is:

Sprint 7D Real Email Source Setup, Manual Config Only

In Sprint 7D, the user may provide:

- provider name
- sender email/domain
- safe subject pattern
- Gmail label to use
- account/card mapping

Still no full body email required.

Real Gmail read is not allowed until Sprint 7E Read-Only Gmail Pilot.

## Acceptance result

RESULT=PASS_SPRINT7C_SYNTHETIC_CANDIDATE_SIMULATION_DESIGN_RECORDED
NEXT=sprint7c_synthetic_candidate_simulation_build

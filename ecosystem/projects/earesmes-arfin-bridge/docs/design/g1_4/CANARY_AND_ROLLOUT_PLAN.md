# EAB G1.4 Canary and Rollout Plan

- **REQUIREMENT**: `PREREQ-010` & `M12` (Fresh Live Canary Verification)
- **STATUS**: `REMEDIATED_R5_DESIGN_COMPLETE`

---

## 1. Roadmap-Aligned Six-Stage Rollout Matrix

```tsv
STAGE_ID	EXECUTION_MILESTONE	ENTRY_CRITERIA	AUTHORIZED_MUTATION_SCOPE	OWNER_AUTHORIZATION_REQUIRED	TRAFFIC_SCOPE	FINANCIAL_WRITE_SCOPE	OBSERVABILITY_REQUIRED	SUCCESS_CRITERIA	ABORT_CRITERIA	ROLLBACK_ACTION	EVIDENCE_OUTPUT	NEXT_STAGE_AUTHORIZATION	THRESHOLD_VALUE	THRESHOLD_CLASSIFICATION	VALIDATION_MILESTONE	THRESHOLD_ID
Stage 0	M10_EAB_G2_3_AUTOMATED_VERIFICATION	All unit & integration tests PASS	None (Offline)	NO	Test Vectors Only	NONE	Test Runner Logs	100% Test Pass	Any Test Failure	Fix Code	Test Execution Report	M11 Dry-Run Approval	100% pass	IMPLEMENTATION_CONFIGURATION_CONSTRAINT	M10	TR-015
Stage 1	M11_EAB_G2_4_INTEGRATION_DRY_RUN	Stage 0 PASS (M11 Dry Run)	Dry-Run Only	YES	Simulated Traffic	NONE	Dry-Run Metrics	Zero Dry-Run Error	Dry-Run Failure	RU-11 Backout	M11 Dry-Run Evidence	Owner M11 Approval	0 errors	PROPOSED_DEPLOYMENT_DEFAULT_REQUIRING_M11_M12_VALIDATION	M11	TR-016
Stage 2	M11_EAB_G2_4_INTEGRATION_DRY_RUN	Stage 1 PASS (Shadow Mode)	Read-Only Observation	YES	Production Shadow	NONE	Full Observability	Zero Auth Error	Auth Failure > 1%	Disable Shadow Route	Shadow Observation Log	Owner Stage 2 Approval	1%	PROPOSED_DEPLOYMENT_DEFAULT_REQUIRING_M11_M12_VALIDATION	M11	TR-017
Stage 3	M12_EAB_G2_5_LIVE_CANARY	Stage 2 PASS (M12 Live Canary)	Restricted Canary	YES	Owner Actor & Conversation Principals	STAGED_REVIEW_QUEUE	Full Observability	Canary Error 0%	Canary Error > 1%	RU-07 Canary Abort	M12 Canary Evidence	M13_EAB_G2_6_OWNER_ACCEPTANCE	1%	PROPOSED_DEPLOYMENT_DEFAULT_REQUIRING_M11_M12_VALIDATION	M12	TR-018
Stage 4	M14_EAB_G2_7_PRODUCTION_ACTIVATION_AND_CLOSEOUT	M12 Canary PASS, M1 Closure Evidence PASS, M13 Acceptance PASS, M14 Authorization Signed	Full Production Bridge	YES	All Owner Chats	STAGED_REVIEW_QUEUE	Full Observability	Error Rate < 0.1%	Prod Error > 0.5%	RU-PROD-ROUTE	Production Metrics Report	M14 Post-Activation Signoff	0.1%	PROPOSED_DEPLOYMENT_DEFAULT_REQUIRING_M11_M12_VALIDATION	M12	TR-019
Stage 5	M14_EAB_G2_7_POST_ACTIVATION_OBSERVATION	Stage 4 PASS (Post-Activation)	Full Operations	NO	Normal Production	STAGED_REVIEW_QUEUE	Full Observability	24h Zero Outage	Outage Incident	Execute Incident Response	24h Stability Report	N/A (Steady State)	24h	PROPOSED_DEPLOYMENT_DEFAULT_REQUIRING_M11_M12_VALIDATION	M12	TR-020
```

---

## 2. Canary Guardrails & Milestone Separation

```ini
PRODUCTION_ACTIVATION_ALLOWED_AT_M12=NO
OWNER_ACCEPTANCE_REQUIRED_BEFORE_PRODUCTION=YES
EXACT_M14_ACTIVATION_AUTHORIZATION_REQUIRED=YES
```

1. **Production Activation Blocked at M12**: Live canary execution completes at Stage 3 in Milestone `M12`. Milestone `M12` does NOT activate production.
2. **Mandatory M13 Owner Acceptance**: Stage 3 canary completion leads to Milestone `M13` (Owner Acceptance & Closeout Assessment). Owner acceptance in M13 is mandatory prior to production activation.
3. **Stage 4 Requires Explicit M14 Authorization**: Stage 4 production activation occurs only in Milestone `M14` with explicit M14 authorization. Entry criteria for Stage 4 requires M12 Canary PASS, M1 Limitation Closure Evidence PASS, M13 Owner Acceptance PASS, and signed M14 Authorization.
4. **Stage 3 Dual Principal Binding**: Stage 3 Canary requires **BOTH** `EAB_CANARY_OWNER_ACTOR_PRINCIPAL` AND `EAB_CANARY_CONVERSATION_PRINCIPAL`. Matching actor in an unauthorized conversation fails closed (`403 Forbidden`). Matching conversation with an unauthorized actor fails closed (`403 Forbidden`).
5. **Review Queue Mandatory**: All canary transactions MUST enter the Review Queue and require explicit Owner approval before ledger posting. Earesmes has zero direct Account Ledger write authority (`EARESMES_LEDGER_WRITE = FORBIDDEN`).
6. **Stage 4 Rollback Protocol**: Stage 4 production route failure executes `ROLLBACK_ACTION = RU-PROD-ROUTE` (reverting production route to baseline while retaining Review Queue items, receipts, and audit logs). Stage 4 rollback MUST NOT use `RU-02`.

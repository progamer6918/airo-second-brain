# EAB Post-vNext Orchestration Boundary Decision & Next Architecture (2026-08-30)

## 1. Executive Summary
- **EAB Product Status**: `NOT_OPERATIONAL`
- **Current EAB Repair Chain**: `DEAD` (No more vNext.1 patch loops)
- **Primary Failure Boundary**: `EARESMES_HERMES_DISPATCH_AND_STATE_PRECEDENCE_BEFORE_ARFIN_SPECIALIST_CALL`
- **Arfin Specialist Candidate Status**: `VALID_ARCHITECTURE_NOT_PROVEN_BAD`
- **Next Engineering Project**: `EARESMES_CAPABILITY_ROUTER_FOUNDATION`

## 2. Live Acceptance Failure Evidence
During the live vNext acceptance trial:
- `RESET_WAS_ROUTED_INTO_FINANCE_PATH=YES`
- `ARFIN_SPECIALIST_CALL_OBSERVED=NO`
- `ARFIN_PENDING_CREATED=NO`
- `POST_ROLLBACK_LIST_PENDING_CANARY=FAILED`

The live failure occurred entirely in Earesmes/Hermes dispatch and session state precedence before the Arfin specialist was ever invoked. Therefore, the specialist architecture itself is not invalidated.

## 3. Architecture Transition & Invariants
1. **No Framework Migration**: No LangGraph, OpenAI Agents SDK, or MCP adoption required; reference patterns only.
2. **Minimal Dispatch Precedence**:
   ```
   GLOBAL CONTROL COMMAND (e.g. reset, cancel)
       >
   EXPLICIT ACTIVE SPECIALIST CONTINUATION
       >
   NEW SPECIALIST INTENT
       >
   GENERIC CHAT FALLBACK
   ```
3. **Draft State Disconnection**: Legacy Hermes finance draft state must NOT remain implicit continuation authority for the new router.
4. **Milestone 1 Acceptance Target**:
   - Input: `catat makan 1`
   - Output: Earesmes dispatches to Arfin specialist -> Arfin returns `NEEDS_CLARIFICATION` -> Earesmes presents clarification -> 0 Review Queue writes, 0 Ledger writes.
5. **Milestone 2 Acceptance Target**:
   - Input: `cash`
   - Output: Resumes Arfin state -> exactly 1 Review Queue row created -> 0 Ledger writes.

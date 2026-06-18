---
status: accepted
confidence: runtime-derived
last_updated: 2026-06-18T21:52:54+07:00
source: controlled-runtime-validation
job_id: AIRO-EARESMES-GATEWAY-DURABILITY-20260618
---

# AIRO Earesmes Gateway Durability Proof — 2026-06-18

## Scope

This record closes the bounded gateway durability repair for the canonical
Telegram gateway used by Earesmes.

No Hermes model call, worker restart, source patch, bot replacement, second
poller, or unrelated repository cleanup was performed.

## Canonical Architecture

```text
Telegram
→ one telegram-gateway.py getUpdates owner
→ deterministic command handling or durable ordinary-text queue
→ airo-hermes-worker.service
→ Hermes AIAgent / Earesmes
→ Telegram sendMessage
```

The Scheduled Task action remains:

```text
AIRO Earesmes Telegram Listener
→ wsl.exe
→ ops/telegram/telegram-action-listener.py
→ exec redirect to ops/telegram/telegram-gateway.py
```

## Configuration Accepted

```text
Task name: AIRO Earesmes Telegram Listener
Logon trigger: enabled
Periodic trigger: PT5M
MultipleInstances: IgnoreNew
RestartCount: 3
RestartInterval: PT2M
ExecutionTimeLimit: unlimited
```

The five-minute trigger is the smallest native durability mechanism selected.
It does not create a second supervisor or a second Telegram poller.

## Controlled Failure Evidence

Test started:

```text
2026-06-18T21:32:24+07:00
```

Observed before termination:

```text
gateway PID: 18992
gateway count: 1
worker PID: 18482
worker state: active
legacy poller count: 0
```

The canonical gateway received SIGTERM and exited cleanly:

```text
CONTROLLED_TERMINATION=PASS
GATEWAY_COUNT_IMMEDIATELY_AFTER_TERM=0
```

The next native Scheduled Task trigger ran at:

```text
2026-06-18 21:34:35 +07:00
```

Observed after automatic recovery:

```text
gateway PID: 20505
gateway count: 1
worker PID: 18482
worker state: active
legacy poller count: 0
task state: Running
next run: 2026-06-18 21:39:35 +07:00
```

Final test result:

```text
CONTROLLED_FAILURE_TEST=PASS
AUTO_RESTART=PASS
SINGLE_GETUPDATES_POLLER=PASS
WORKER_UNINTERRUPTED=PASS
REPO_FILES_MUTATED=NONE
FINAL_RESULT=PASS
```

## Current Readback at Closeout

```text
repository HEAD: 8959193
canonical gateway PID: 20505
canonical gateway count: 1
worker PID: 18482
worker state: active
legacy poller count: 0
```

## Acceptance

```text
GATEWAY_DURABILITY=PASS
SINGLE_GETUPDATES_OWNERSHIP=PASS
WORKER_ISOLATION=PASS
SECOND_POLLER=ABSENT
```

## Rollback Evidence

Pre-mutation Scheduled Task XML backup:

```text
C:\Users\Admin\AppData\Local\Temp\AIRO_Earesmes_Telegram_Listener_before_durability_20260618_212935.xml
```

Rollback is not required because the controlled failure test passed.

## Remaining Open Item

Gateway durability does not prove low response latency.

The approximately 21-second prior Earesmes response remains an open latency
measurement item. It must be traced across gateway receive, queue write,
worker start, model completion, and Telegram send before changing models or
runtime architecture.

## Next Exact Action

Run AIRO Second Brain PRD v0.5.1 Phase 0A in READ_ONLY_AUDIT mode.

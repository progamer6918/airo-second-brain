# AIRO Finance v1.3 Intent Router Force Patch

Status: APPLIED
Date: 2026-05-11T23:14:13+0700

Problem:
Telegram/OpenClaw saw airo_intent_router.py but still did not force finance routing for:
kayaknya bayar sesuatu kemarin

Patch:
Inserted a top-level finance pre-router into:

scripts/personal-workflow/airo_intent_router.py

Behavior:
Any finance-like message is routed before the old generic router logic.

Expected:
kayaknya bayar sesuatu kemarin -> finance_capture -> 🧾 Review Queue
hari ini cash kepake beli makan 20rb -> finance_capture -> 💵 Cash Ledger

Test:
tests/personal-workflow/test_airo_intent_router_v13_finance_force.py

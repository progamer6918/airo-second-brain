# AIRO Finance Dashboard Lite Safe Unmerge Fix — 2026-07-05

Status: PASS

Runtime-2 manual refresh failed because legacy Dashboard had merged ranges overlapping B1:K45. Direct partial `breakApart()` failed.

Fix: add `airoDashboardLiteBreakApartMergedRanges_`, break full overlapping merged ranges from `sheet.getDataRange().getMergedRanges()`, then clear B1:K45.

Boundary: no clasp, no runtime, no workbook mutation, no scheduler.

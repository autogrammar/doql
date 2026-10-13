# Ticket 009: Decouple hardcoded test path in test_adopt.py

- **ID**: ticket-009
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-10-13

## Goal and scope

Eliminate hardcoded `/home/tom` user paths in `tests/test_adopt.py` in accordance with `wellmanifest/nohardcode` (`NOHARDCODE-009`).

## Acceptance criteria

- [x] AC-01: Decouple `OQLOS_ROOT` using `os.environ` and `Path.home()`.
- [x] AC-02: Governance check passes (`GOV-PASS`).
- [x] AC-03: Test suite passes.

## Tracking boundary

This directory contains the minimal reviewed intent. Optional participant prose
and raw command logs are not required delivery output.

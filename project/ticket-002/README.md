# Ticket 002: Route nlp2doql planner through central SubLLM

- **ID**: ticket-002
- **Owner**: unresolved:human
- **Status**: BLOCKED
- **Workflow state**: PLAN
- **Created**: 2026-08-28

## Goal and scope

`nlp2doql` still calls LiteLLM with a caller-chosen model. SubLLM already
registers `autogrammar-doql/translate`. Route the optional planner through
that pair so provider, model and attribution stay central. Keep the rules
planner as the default. Do not send paid requests.

## Acceptance criteria

- [ ] AC-01: Optional LLM planning calls SubLLM `autogrammar-doql`/`translate`.
- [ ] AC-02: Missing SubLLM fails closed without a private OpenRouter/LiteLLM path.
- [ ] AC-03: Tests mock the central client; no paid requests.
- [ ] AC-04: `plan_with_litellm` remains a compatibility alias.

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-grok.md](ai-grok.md)

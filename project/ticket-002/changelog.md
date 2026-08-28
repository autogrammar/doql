# Ticket 002 changelog

## 2026-08-28

- Route the optional nlp2doql planner through SubLLM `autogrammar-doql/translate`.
- Replace the LiteLLM extra with a pinned `subactor-subllm` git dependency.
- Keep `plan_with_litellm` as a compatibility alias.

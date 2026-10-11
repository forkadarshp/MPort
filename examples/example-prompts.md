# Example User Prompts

Use these to test ModelPort triggering and behavior.

## Basic migrations

1. "Migrate all model usage in `src/agents/` from our old model config to the new release, keep tool behavior stable, and give me a rollback plan."
2. "Upgrade this codebase from provider A to provider B and adjust prompts so output format remains identical."
3. "Replace deprecated model parameters in our API callers and verify tests still pass."
4. "Update agent orchestration prompts and tool descriptions for the new model behavior, but do not change business logic."
5. "Do a phased migration in `services/search` with side-by-side support for old and new models."
6. "Port all prompt templates in `prompts/` and flag any risky behavior changes."
7. "Migrate this repo to the latest model family and separate required fixes vs optional tuning."
8. "Upgrade model references across config, tests, and docs without breaking runtime routing."

## Current-model migrations

1. "Migrate this repo to `claude-opus-5-5`. Apply required fixes first, then list optional tuning separately."
2. "Move the classification and routing calls in `src/` to `claude-haiku-5-5` and keep the output format identical."
3. "Migrate our OpenAI calls from `gpt-5.5` to `gpt-6.1-sol`. Move tool calling to the Responses API where needed."
4. "Upgrade our Gemini calls to `gemini-3.8-flash` and replace `thinking_budget` with `thinking_level`."
5. "We changed the model ID and now get 400s. Find the cause and fix it."
6. "Our agent UI goes quiet between tool calls since the upgrade. Find out why and fix it."

## Advanced migrations

1. "Migrate from OpenAI `gpt-5.5` to Anthropic `claude-sonnet-5-5` across all agents, normalize output contracts, and add provider-agnostic wrapper layers."
2. "Agent B already started migrating `services/chat` — pick up where it left off, verify what's done, and finish the remaining work with validation."
3. "Migrate our structured output pipeline from JSON mode to native structured outputs on the new model, update Zod schemas, and regression-test all tool call paths."

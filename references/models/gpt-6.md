# Migrating to GPT-6 (Astra, 6.1 Sol, Sol, Luna): breaking changes and fixes

What changes when you move code from GPT-5.x to the GPT-6 family, the fix for each, and what to re-tune.

Model IDs: `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6-sol`, `gpt-6-luna`
Context / output: 1,050,000 tokens (922,000 max input) / 128,000 tokens
Knowledge cutoff: Apr 30, 2026 (Astra and 6.1 Sol)
Last verified: 2026-10-11
Source: OpenAI "Using GPT-6" guide and the `gpt-6-astra` and `gpt-6.1-sol`
model pages. Sol and Luna prices and all release dates come from secondary
sources and are marked below. Re-check the OpenAI model pages before quoting.

## Variants

| Variant | Model ID | Use case | Price in / out per 1M tokens |
| :------ | :------- | :------- | :--------------------------- |
| GPT-6 Astra | `gpt-6-astra` | Highest intelligence: demanding reasoning, coding, professional work | $10 / $50 (cached $1, cache writes $12.50) |
| GPT-6.1 Sol | `gpt-6.1-sol` | Balanced speed, cost, intelligence | $2 / $10 (cached $0.10, cache writes $2.50) |
| GPT-6 Sol | `gpt-6-sol` | Existing model. Review the migration notes before moving to 6.1 Sol | $2 / $10 (secondary source) |
| GPT-6 Luna | `gpt-6-luna` | Fastest, cheapest, high-volume focused tasks | $0.10 / $0.50 (secondary source) |

Prompts over 272K input tokens bill the whole request at 2x input and cache
rates and 1.5x output. Fast mode is 2x, Ultrafast is 6x, Batch and Flex are
50% lower, regional processing adds 10% (6.1 Sol page).

Secondary-source release dates (unverified): Astra 2026-09-03, GPT-6 Sol and
Luna 2026-09-22, GPT-6.1 Sol 2026-09-29 or 2026-09-30.

## Reasoning effort

Set `reasoning.effort` (Responses API) or `reasoning_effort` (Chat
Completions).

| Model | Levels | Notes |
| :---- | :----- | :---- |
| GPT-6.1 Sol | `low`, `medium` (default), `high`, `xhigh`, `max` | `none` and `minimal` unsupported |
| GPT-6 Astra | `low`, `medium`, `high`, `xhigh`, `max` | `none` unsupported. Use `low` instead |
| GPT-6 Sol, GPT-6 Luna | Support `none` | |

## Required changes

| Area | Change |
| :--- | :----- |
| Endpoint | Use the **Responses API** for tool calling. Astra and 6.1 Sol support Chat Completions only for requests without tools. Sol and Luna support function calling in Chat Completions only with `reasoning_effort: "none"`. |
| Sampling | When effort is not `none`, remove `temperature`, `top_p`, `top_logprobs`. Chat Completions: also remove `logprobs`. Responses: remove `message.output_text.logprobs` from `include`. |
| `minimal` effort | Replace with `low`. Compare on representative tasks. |
| `none` effort (Astra, 6.1 Sol) | Replace with `low`. |
| Prompt caching | Replace `prompt_cache_retention` with `prompt_cache_options.ttl` set to `"30m"` when migrating from GPT-5.5 or earlier. Review cache boundary and cache-write billing changes. |
| Model ID | Set `model` to the target ID. Astra and 6.1 Sol list one snapshot each: the bare ID. |

OpenAI suggests Codex with the OpenAI Docs skill:
`$openai-docs migrate this project to the GPT-6 model family`.

## New API features

- **Async tool calling**: set `async: true` on a function or custom tool,
  then return the result later with the original `call_id`.
- **Mid-turn steering**: send user instructions while the model works.
- **`configuration_update` input item**: change reasoning effort mid-
  conversation without altering the prompt prefix, so caching survives.
- **Fast and Ultrafast modes**. Data residency differs: Astra Fast mode has
  no EU residency and no latency SLA.
- Carried over from GPT-5.6: computer use, Structured Outputs, streaming,
  Programmatic Tool Calling, multi-agent orchestration, prompt caching,
  persisted reasoning, compaction, pro mode.

## Prompt and behavior tuning (optional)

- **Initiative**: Astra asks clarifying questions more than earlier models.
  Say to act when the request implies authorization, and to ask for approval
  once a concrete result is ready.
- **Instruction priority**: Astra weighs `AGENTS.md` and skill files heavily.
  Audit them. State that user instructions override skill guidance.
- **Style**: Astra favors long, formatted answers with lists and tables. State
  the style you want if you need prose.
- **Subagents**: Astra may delegate less than you want. Say when and how.
- **Testing**: Astra tests thoroughly, sometimes beyond what a small change
  needs. Calibrate the scope.
- Carry-over from GPT-5.5 guidance: outcome-first prompts, drop legacy
  scaffolding, keep few-shot examples for format calibration.

## Upgrade paths

| From | Notes |
| :--- | :---- |
| GPT-5.5 | Apply the required changes above. Re-baseline effort: Astra defaults are not documented, 6.1 Sol defaults to `medium`. See `gpt-5-5.md` for the earlier surface. |
| GPT-5.x, GPT-4o, o-series | Apply the `gpt-5-5.md` steps first (Responses API, effort, structured outputs), then this guide. |
| GPT-6 Sol | Review the migration notes before moving to 6.1 Sol. |

Search results also mention a GPT-5.6 model page. Treat GPT-5.6 as an
intermediate release and verify its status on the OpenAI models page before
targeting it.

## Model ID reference

| Version | Model ID | Status |
| :------ | :------- | :----- |
| GPT-6 Astra | `gpt-6-astra` | Current |
| GPT-6.1 Sol | `gpt-6.1-sol` | Current |
| GPT-6 Sol | `gpt-6-sol` | Existing |
| GPT-6 Luna | `gpt-6-luna` | Current |
| GPT-5.5 | `gpt-5.5` | Previous generation (see `gpt-5-5.md`) |

# Claude Haiku 5.5

Model ID: `claude-haiku-5-5` (Amazon Bedrock: `anthropic.claude-haiku-5-5`)
Pricing: $0.10 / $0.50 per million input / output tokens for prompts up to
100K tokens. $0.50 / $2.50 above 100K tokens. (Haiku 4.5: $1 / $5 at any
length.)
Context / output: 1M tokens / 128K tokens (Haiku 4.5: 200K / 64K)
Last verified: 2026-10-11
Source: Anthropic API migration guide (bundled `claude-api` skill, cached
2026-10-06) and platform docs

This is the current Haiku, for high-volume and latency-sensitive work:
classification, routing, extraction, and sub-agent tasks.

## Changelog (vs Haiku 4.5)

- First Haiku with `effort` levels (`low` to `max`, default `medium`).
- Adaptive thinking on by default. Manual budgets removed.
- Sampling parameters and assistant prefill removed.
- Newer tokenizer: about 30% more tokens for the same text.
- Safety classifiers can decline requests. No server-side fallback exists.
- Larger limits, browser use tool, mid-conversation system messages,
  per-message effort, compaction, programmatic tool calling, tool search.

## Required changes (will 400)

| Change | Detail |
| :----- | :----- |
| Manual thinking budget | `{type: "enabled", budget_tokens: N}` 400s. Use `{type: "adaptive"}` (or omit) plus `output_config.effort`. |
| Sampling parameters | `temperature` must be `1`, `top_p` must be `0.99`, any `top_k` 400s, and sending both `temperature` and `top_p` 400s. Omit all three. A `temperature=0` classifier: remove it and constrain output with structured outputs or an enum tool. |
| Assistant prefill | A final assistant turn 400s, even with thinking off. End `messages` with a user turn. Use `output_config.format`, an enum tool, or a prompt instruction. |
| Computer use | `computer_20250124` 400s on the Claude API and Google Cloud. Use `computer_toolset_20260801`. Replace the `fine-grained-tool-streaming-2025-05-14` header with `eager_input_streaming: true`. Do not assume the Bedrock exception that Opus 5.5 and Sonnet 5.5 have. |
| Preserved thinking | Replaying a thinking block after editing `system`, `tools`, or earlier `messages` 400s on accounts created on or after 2026-08-31. Keep histories append-only. |
| Refusals | Four categories: `cyber`, `bio`, `frontier_llm`, `general_harms`. Check `stop_reason` first. Do **not** send `fallbacks`: `"default"` leaves a decline declined, and a model list 400s. Handle it in the client. |

## Silent changes

| Change | Action |
| :----- | :----- |
| Thinking on by default | Read content blocks by `type`, never `content[0]`. A response can start with `thinking` blocks. |
| Thinking counts toward `max_tokens` | A cap sized for a one-word answer (for example 50) can be consumed by thinking. Raise it or lower effort. |
| Thinking text omitted | Set `display: "summarized"` to see reasoning. Keep empty `thinking` blocks. |
| Tokenizer | Recount with `count_tokens` against `claude-haiku-5-5`. Re-baseline `max_tokens` and cost. |
| Disabled thinking | Still accepted at `low`, `medium`, `high`. 400s at `xhigh` and `max`. Prefer adaptive at `low`. |
| Forced `tool_choice` | Still accepted, but the response skips thinking. Use `auto` plus a prompt when the call needs thought. |
| Cache minimum | 512 tokens (was 4,096). Short prompts now create cache entries. |
| Thinking blocks | Stay with the account that produced them. Replay a stored conversation through the same account. |

## Effort guide

| Level | Use |
| :---- | :-- |
| `low` | Chat, short tool tasks, simple high-volume routes. Cheapest and fastest. |
| `medium` (default) | Most work, including agentic coding. |
| `high` | Knowledge work, long agent tasks, strict instruction following. |
| `xhigh`, `max` | Only with a measured gain. Compare against Sonnet 5.5 first. |

To get less thinking, lower effort. A "answer directly" prompt barely helps.

## Prompt and behavior tuning (optional)

- Search tools: put today's date in the system prompt or tool description. For
  long prompts or `low` effort, add a line saying which facts may have changed
  since training. Avoid blanket "always search" rules.
- JSON output plus the caller's own tools with thinking off can skip a needed
  tool call. Keep thinking on, or add: "The JSON output format applies to your
  final answer only. When you need a tool, call it first."
- Check for empty replies at `xhigh` in multi-turn chat.
- Long agent prompts at `low` effort can stop early. Add a keep-working
  instruction, or raise effort.
- Add a verification instruction for coding agents at `low` and `medium`.
- Deliver mid-turn user input as a text block after the last `tool_result`.

## Model ID reference

| Version | Model ID | Status |
| :------ | :------- | :----- |
| Haiku 5.5 | `claude-haiku-5-5` | Current |
| Haiku 4.5 | `claude-haiku-4-5` | Active |

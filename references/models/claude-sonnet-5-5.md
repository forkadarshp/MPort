# Claude Sonnet 5.5

Model ID: `claude-sonnet-5-5` (Amazon Bedrock: `anthropic.claude-sonnet-5-5`)
Pricing: $2 / $10 per million input / output tokens (same as Sonnet 5)
Cache reads: $0.20 per million tokens
Context / output: 1M tokens / 128K tokens
Last verified: 2026-10-11
Source: Anthropic API migration guide (bundled `claude-api` skill, cached
2026-10-06) and platform docs

This is the current Sonnet. Layered guide: coming from Sonnet 4.6 or older,
apply the earlier sections first (see "Upgrade paths").

## Changelog (vs Sonnet 5)

- **`disabled` thinking removed**: use `{type: "between_tools"}` as the
  lowest thinking setting.
- **Forced `tool_choice` removed**.
- **Preserved thinking**: thinking blocks are tied to the model and to an
  unedited conversation prefix.
- **Computer use via toolset only** on the Claude API and Google Cloud.
- **Advisor tool** accepts fewer advisors.
- **Effort levels recalibrated**. Default is still `high`.
- **New**: mid-conversation system messages, tool changes, per-message effort,
  task budgets, 512-token cache minimum.

## Required changes (will 400)

| Change | Detail |
| :----- | :----- |
| Disabled thinking | `{type: "disabled"}` 400s. First try adaptive thinking at `effort: "low"`. If the route must stay thinking-off, send `{type: "between_tools"}` at effort `high` or below. |
| `between_tools` limits | No other field inside `thinking`. No per-message effort change. Accepted by Sonnet 5.5 only, so drop it from any body re-sent to another model. |
| Forced tool use | `tool_choice` `any` and `tool` 400 (also on `count_tokens`). Use `auto` + `strict: true` + a prompt instruction, or structured outputs. |
| Computer use | `computer_20251124` 400s on the Claude API and Google Cloud. Use `computer_toolset_20260801`. Amazon Bedrock still accepts `computer_20251124`. Do not prune old screenshots client-side: it invalidates later thinking blocks. |
| Preserved thinking | Enforced by default on the Claude API and Amazon Bedrock for accounts created on or after 2026-08-31. `block_binding` works only with adaptive thinking. Keep histories append-only. |
| Advisor tool | Rejects Opus 4.8, 4.7, 4.6, Sonnet 5, and Sonnet 4.6 advisors. Accepted advisors return encrypted advice. |
| Refusals | Five `stop_details` categories: `cyber`, `bio`, `frontier_llm`, `reasoning_extraction`, `general_harms`. Server-side fallback retries only `cyber` and `frontier_llm`. |

## Silent changes

| Change | Action |
| :----- | :----- |
| Effort levels recalibrated | Set `effort` explicitly. Start at `medium` for agentic coding and multistep tool use. Start at `low` for chat, extraction, classification, and search. |
| Thinking before most replies | From `medium` up, the model thinks briefly before almost every reply. Lower effort to cut time to first token. A "think less" prompt barely helps. |
| Progress updates as `thinking` | Set `display: "updates"` (beta) with adaptive thinking. With `between_tools`, the notes return as text and no `display` is allowed. |
| Same tokenizer as Sonnet 5 | Token counts unchanged from Sonnet 5. |
| Rate limits | Own pool. Priority Tier not supported. |

## Upgrade paths

| From | Apply, in order |
| :--- | :-------------- |
| Sonnet 5 | This guide only. |
| Sonnet 4.6 | Sonnet 5 changes (adaptive thinking on by default, sampling params rejected, about 30% more tokens, `display` default `"omitted"`), then this guide. Skip the Sonnet 5 effort advice. |
| Sonnet 4.5 or older, Haiku 4.5 | Sonnet 4.6 changes first (prefill removed, explicit effort, beta headers), then Sonnet 5, then this guide. |

## Prompt and behavior tuning (optional)

- Remove workarounds for what improved: refusal steering, tool-call retry
  shims, "do not be lazy".
- Remove tool-discouraging language ("minimize tool calls"). The model follows
  it literally and may skip connected tools.
- Deliver mid-turn user input as a text block after the last `tool_result`.
  Never put user text inside a `tool_result`. A mid-task user message placed
  right after a tool result can be read as prompt injection.
- Skip task budgets on interactive sessions. The countdown arrives as a system
  message after every tool result and can trigger the same reaction.
- At `low` effort, coding agents may report a change done without running a
  check. Add a "run a real check before reporting done" instruction.
- Accept near-miss tool names (case differences) or return an `is_error`
  result that states the exact expected name.
- Give crop, zoom, or code tools for dense charts and technical drawings.

## Validation notes

- Smoke test: assert `response.model.startswith("claude-sonnet-5-5")`.
- Prefix collision: a check for `claude-sonnet-5` also matches
  `claude-sonnet-5-5`. Add a `not startswith("claude-sonnet-5-5")` guard.
- Test the thinking-off route at `low` effort first, then `between_tools`.

## Model ID reference

| Version | Model ID | Status |
| :------ | :------- | :----- |
| Sonnet 5.5 | `claude-sonnet-5-5` | Current |
| Sonnet 5 | `claude-sonnet-5` | Active |
| Sonnet 4.6 | `claude-sonnet-4-6` | Active |
| Sonnet 4.5 | `claude-sonnet-4-5` | Active |

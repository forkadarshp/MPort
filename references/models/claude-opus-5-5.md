# Claude Opus 5.5

Model ID: `claude-opus-5-5` (Amazon Bedrock: `anthropic.claude-opus-5-5`)
Pricing: $4 / $20 per million input / output tokens (Opus 5: $5 / $25)
Cache reads: $0.20 per million tokens
Context / output: 1M tokens / 128K tokens
Last verified: 2026-10-11
Source: Anthropic API migration guide (bundled `claude-api` skill, cached
2026-10-06) and platform docs

This is the current Opus and the default upgrade target for Claude code.
Layered guide: coming from Opus 4.8 or older, apply the earlier sections
first (see "Upgrade paths").

## Changelog (vs Opus 5)

- **Lower price**: 20% cheaper per token, 60% cheaper for cache reads.
- **Thinking always on**: `thinking: {type: "disabled"}` is gone.
- **Effort default is `medium`** (Opus 5 defaulted to `high`).
- **Forced `tool_choice` removed**.
- **Preserved thinking**: thinking blocks are tied to the model and to an
  unedited conversation prefix.
- **Computer use via toolset only** on the Claude API and Google Cloud.
- **Progress notes between tool calls** come back as `thinking` blocks.
- **New `bio` safety category** joins `cyber` and `reasoning_extraction`.

## Required changes (will 400)

| Change | Detail |
| :----- | :----- |
| Disabled thinking | `{type: "disabled"}` and `{type: "enabled", budget_tokens}` both 400 at every effort level. Omit `thinking` or send `{type: "adaptive"}`. Use `effort: "low"` to cut latency. |
| Forced tool use | `tool_choice` `any` and `tool` 400 (also on `count_tokens` and Batches). Use `auto` + `strict: true` + a prompt instruction, then check a call happened. Use `output_config.format` when the forced call only existed to get JSON. |
| Computer use | `computer_20251124` 400s on the Claude API and Google Cloud. Use `{"type": "computer_toolset_20260801"}` (no `name`, no display size, no beta header). Amazon Bedrock still accepts `computer_20251124`. The agent loop changes: the action is the `tool_use` block `name`, several calls per turn, echo `toolset_name` on every result. |
| Preserved thinking | A replayed thinking block after an edit to `system`, `tools`, or earlier `messages` returns 400 on accounts created on or after 2026-08-31. Older accounts opt in via `thinking.block_binding.prefix_mismatch_behavior`. Keep histories append-only. |
| Refusals | Check `stop_reason == "refusal"` before reading `content`. Ship a fallback opt-in. `reasoning_extraction` is not retried on a fallback. |

## Silent changes (no error, behavior differs)

| Change | Action |
| :----- | :----- |
| Default effort `medium` | Set `output_config.effort` explicitly. Re-run the effort sweep. `medium` here often matches Opus 5 at `high`. |
| More thinking per level | At `xhigh` and `max`, expect longer turns and more output tokens. Lower effort before adding "think less" prompts. |
| `thinking.display` default `"omitted"` | Set `"summarized"` to show reasoning. Keep empty `thinking` blocks when replaying. |
| Progress updates as `thinking` | Set `display: "updates"` (beta `thinking-display-updates-2026-08-18`) or render non-empty `thinking` blocks ahead of the `tool_use`. |
| `max_tokens` | Size for thinking plus reply. 64K is a good start for long agentic coding. |
| Rate limits | Separate pool from Opus 5. Re-check the tier. |
| Priority Tier | Not supported. |
| Fast mode | Claude API only, $8 / $40 per million tokens. |

## Upgrade paths

| From | Apply, in order |
| :--- | :-------------- |
| Opus 5 | This guide only. |
| Opus 4.8 | `claude-opus-4-8.md` (re-tune), Opus 5 changes (thinking on by default, prompt re-tuning), then this guide. |
| Opus 4.7 / 4.6 or older | `claude-opus-4-8.md` (includes the 4.7 breaking changes), Opus 5 changes, then this guide. |
| Sonnet 5 / 5.5 | Request surface already matches. Re-baseline for Opus pricing and rate limits. |

Opus 5 specifics to carry through on a 4.x upgrade: thinking is on when
`thinking` is omitted, the cache minimum is 512 tokens, the 1M context window
is the default, and Opus 5 writes longer visible output than 4.8 (add
conciseness and scope-discipline instructions).

## Prompt and behavior tuning (optional)

- Remove instructions that stood in for thinking. A prompt that asks the model
  to write its reasoning into the response can be declined with
  `reasoning_extraction`. Read `display: "summarized"` blocks instead.
- Delete "don't think" rules. The model cannot comply and tag leakage rises.
- Re-test visual scaffolding. Chart and screenshot reading improved at every
  effort level without extra tooling.
- Re-test Opus 5 verbosity, verification, and scope instructions. Keep them
  as a starting point, then A/B each.
- For frontend work, name specific default patterns to avoid. "No generic AI
  look" mostly swaps one default for another.
- To vary effort without losing the prompt cache, use per-message effort
  (beta `mid-conversation-output-config-2026-07-01`). Changing top-level
  `effort` invalidates the cache.

## Validation notes

- Smoke test: assert `response.model.startswith("claude-opus-5-5")`.
- Prefix collision: a check for `claude-opus-5` also matches
  `claude-opus-5-5`. Add a `not startswith("claude-opus-5-5")` guard.
- Test a long tool loop with thinking blocks replayed unchanged.
- Test a forced-fallback refusal path.

## Model ID reference

| Version | Model ID | Status |
| :------ | :------- | :----- |
| Opus 5.5 | `claude-opus-5-5` | Current |
| Opus 5 | `claude-opus-5` | Active |
| Opus 4.8 | `claude-opus-4-8` | Active |
| Opus 4.7 | `claude-opus-4-7` | Active |
| Opus 4.6 | `claude-opus-4-6` | Active |

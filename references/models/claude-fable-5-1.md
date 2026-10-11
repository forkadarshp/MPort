# Migrating to Claude Fable 5.1: breaking changes and fixes

What breaks when you move code to `claude-fable-5-1`, the fix for each, and what to re-tune.

Model ID: `claude-fable-5-1` (Project Glasswing counterpart:
`claude-mythos-5-1`)
Pricing: $10 / $50 per million input / output tokens
Cache reads: $0.25 per million tokens
Context / output: 1M tokens / 128K tokens
Last verified: 2026-10-11
Source: Anthropic API migration guide (bundled `claude-api` skill, cached
2026-10-06) and platform docs

Anthropic's most capable widely released model, for the most demanding
reasoning and long-horizon agentic work. **Migrate here only when the user
explicitly chose it.** The default upgrade target for "latest model" is
`claude-opus-5-5`. Fable pricing is above Opus tier.

## Changelog (vs Fable 5)

- Forced `tool_choice` (`any`, `tool`) removed.
- Thinking blocks are bound to the producing model.
- Editing earlier turns invalidates thinking blocks (preserved thinking).
- Per-message `effort`, turn-scoped `clear_at: "next_user_message"` system
  messages, `thinking.display: "updates"`, cache reads at $0.25 per million.
- Same tokenizer as Opus 4.8 and Fable 5.

## Required changes (will 400)

| Change | Detail |
| :----- | :----- |
| Thinking config | Thinking is always on. Omit `thinking` or send `{type: "adaptive"}`. `{type: "disabled"}` and `budget_tokens` both 400. |
| Sampling parameters | Non-default `temperature`, `top_p`, `top_k` 400. |
| Assistant prefill | 400. Use `output_config.format` or system prompt instructions. |
| Forced tool use | `tool_choice` `any` and `tool` 400. Use `auto` + `strict: true`, or structured outputs. |
| Preserved thinking | Replayed thinking blocks after an edit to `system`, `tools`, or earlier `messages` 400 on accounts created on or after 2026-08-31. Keep histories append-only: mid-conversation `role: "system"` messages, `tool_addition` / `tool_removal` blocks, server-side compaction or context editing. |
| Data retention | Requires 30-day retention. Zero-data-retention orgs get `400 invalid_request_error` unless Anthropic expressly authorized it. |
| Refusals | Classifiers can decline cyber, biology research, and similar requests. Check `stop_reason == "refusal"` before reading `content`. |

## Refusal fallback (ship from day one)

Fallbacks are not automatic. Add one, tell the user, and drop it only if they
decline.

| Platform | Mechanism |
| :------- | :-------- |
| Claude API, Claude Platform on AWS | Server-side: beta `server-side-fallback-2026-07-01` + `fallbacks: "default"` (routes by refusal category). Older array form: beta `server-side-fallback-2026-06-01` + `fallbacks: [{"model": "claude-opus-4-8"}]`. |
| Amazon Bedrock, Vertex AI, Foundry | SDK client middleware (`BetaRefusalFallbackMiddleware` + one `BetaFallbackState` per conversation). |
| Raw HTTP | Retry on another model. Use fallback credit (`fallback-credit-2026-07-01`) to keep cache-read pricing. The retry body must match the refused request exactly. |

Thinking blocks from Fable 5.1 are read only by Fable 5.1 and Mythos 5.1.
After a fallback, the next model runs without that reasoning. Do not strip
blocks yourself.

## Silent changes

| Change | Action |
| :----- | :----- |
| `thinking.display` default `"omitted"` | Set `"summarized"` for readable reasoning. Pass blocks back unchanged, empty ones included. |
| Turns run many minutes | Plan timeouts, streaming, and progress UX. Check in asynchronously. |
| Tokenizer | Roughly unchanged from Opus 4.7 and 4.8. From Opus 4.6, Sonnet, or Haiku, expect about 1x to 1.35x more tokens. Re-baseline with `count_tokens`. |
| Effort | Supports `low` to `max`. Lower levels often beat prior-generation `xhigh`. Sweep `low` and `medium` for routine work. |

## Prompt and behavior tuning (optional)

- De-prescribe migrated prompts and skills. Step-by-step scaffolding written
  for older models often lowers output quality. State goals and constraints.
- At high effort, add a no-tidying line to stop unrequested refactors.
- Ground progress claims: require each claim to match a tool result from the
  session.
- State boundaries: when the user describes a problem, report findings and
  stop. Do not apply fixes until asked.
- Delegate to sub-agents and let them run asynchronously.
- Give a memory file for learnings across sessions.
- Autonomous pipelines: add a "do not ask permission for reversible actions"
  reminder.
- Avoid showing remaining-token counts. Deep sessions can trigger context
  anxiety.
- Long sessions: ask for a final summary written for a reader who did not
  watch the work. No arrow chains or made-up labels.

## Model ID reference

| Version | Model ID | Status |
| :------ | :------- | :----- |
| Fable 5.1 | `claude-fable-5-1` | Current |
| Fable 5 | `claude-fable-5` | Active |
| Mythos 5.1 | `claude-mythos-5-1` | Project Glasswing only |

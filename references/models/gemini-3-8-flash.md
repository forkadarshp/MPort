# Migrating to Gemini 3.8 Flash: breaking changes and fixes

What changes when you move code to `gemini-3.8-flash`, the fix for each, and what to re-tune.

Model ID: `gemini-3.8-flash` (generally available)
Context / output: 1M tokens / 64K tokens
Default thinking level: `medium`
Pricing: $0.75 / $3.75 per million input / output tokens through Dec 31, 2026.
$1.50 / $7.50 from Jan 1, 2027. The introductory rate also applies to Gemini
3.6 Flash.
Last verified: 2026-10-11
Source: Google "What's new in Gemini 3.8 Flash" (last updated 2026-10-09) and
the Gemini API pricing page. The release date is not stated on either page.

Google's most intelligent Flash model. The pricing page lists no Pro model
newer than `gemini-3.1-pro-preview`. Gemini 3.6 Flash stays supported.

## Current model lineup (pricing page, per 1M tokens in / out)

| Model | Model ID | Price |
| :---- | :------- | :---- |
| Gemini 3.8 Flash | `gemini-3.8-flash` | $0.75 / $3.75 |
| Gemini 3.6 Flash | `gemini-3.6-flash` | $0.75 / $3.75 |
| Gemini 3.5 Flash-Lite | `gemini-3.5-flash-lite` | $0.30 / $2.50 |
| Gemini 3.1 Flash-Lite | `gemini-3.1-flash-lite` | $0.25 / $1.50 |
| Gemini 3.1 Pro Preview | `gemini-3.1-pro-preview` | $2.00 / $12.00 (up to 200K) |

## Thinking levels

| Level | Use |
| :---- | :-- |
| `low` | Latency-critical work: incident response, real-time chat, drafts, fast data analysis |
| `medium` (default) | Complex code and agentic use cases |
| `high` | Deep reasoning, mathematics, hard multi-step tasks |

`minimal` returns an error on 3.8 Flash. The model uses smaller reasoning
steps, calls tools iteratively, and verifies its work, so it can spend more
tokens on long tasks. Lower the level on everyday tasks to cut token use.

## Migration checklist

| Step | Change |
| :--- | :----- |
| 1 | Set the model string to `gemini-3.8-flash`. |
| 2 | Replace `thinking_budget` with the string enum `thinking_level`. Sending both returns 400. |
| 3 | Remove `temperature`, `top_p`, `top_k`, `candidate_count`. `candidate_count` is unsupported in Gemini 3 and later. Secondary guides disagree on whether the sampling parameters error or are silently ignored. Remove them and test. |
| 4 | Remove prefilled model turns. Use server-side `previous_interaction_id` for multi-turn conversations. |
| 5 | Function calling: put multimodal assets inside the response payload, format inline instructions with `\n\n`, and for `generateContent` make every `FunctionResponse` include `call_id` and `name`. For `Malformed_Function_Call` errors tied to text before a tool call, see the linked workarounds on the Google page. |
| 6 | Preserve thought signatures per the Gemini 3 requirements. Thought preservation across turns is on by default. |

## Behavior notes

- Default effort fell from high to medium across the 3.5 generation. A route
  that relied on the old default now thinks less. Set `thinking_level`
  explicitly and re-run evals.
- If the model over-calls tools, lower the thinking level.
- The Antigravity agent in Managed Agents and the Antigravity SDK default to
  Gemini 3.8 Flash. Override via `agent_config`.
- The older Gemini 3 developer guide is deprecated. Prefer the
  "What's new in Gemini 3.8 Flash" page.
- `gemini-2.5-flash-image` shuts down 2026-10-02.

## Upgrade paths

| From | Notes |
| :--- | :---- |
| Gemini 3.6 / 3.7 Flash | Mostly a model-ID swap. Apply steps 2 to 6 if not done, and drop `minimal`. |
| Gemini 3.5 Flash | Apply the full checklist. Re-check the default thinking level. |
| Gemini 2.5, 3 Preview | Apply the full checklist. Move from `thinking_budget` to `thinking_level` and re-validate function calling. |
| Another provider | Follow `provider-checklists.md` (cross-provider section), then this guide. |

## Model ID reference

| Version | Model ID | Status |
| :------ | :------- | :----- |
| Gemini 3.8 Flash | `gemini-3.8-flash` | Current (GA) |
| Gemini 3.6 Flash | `gemini-3.6-flash` | Supported |
| Gemini 3.1 Pro Preview | `gemini-3.1-pro-preview` | Preview |
| Gemini 2.5 Pro | `gemini-2.5-pro` | Older |

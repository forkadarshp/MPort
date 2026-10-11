# Breaking Changes Quick Lookup

Symptom to cause to fix, across providers. Use it when a model swap starts
returning errors or behaving differently. Each row points at the guide that
has the full migration. Facts verified 2026-10-11 against provider docs (see
each guide's `Source:` line). Exact error text is quoted where the provider
documents it. Where it is not documented here, the symptom is described
instead of guessing a string.

## Request errors (HTTP 400)

| You send | Fails on | Error or symptom | Fix |
| :------- | :------- | :--------------- | :-- |
| `thinking: {type: "disabled"}` | Claude Opus 5.5, Fable 5.1, Fable 5 | `"thinking.type.disabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.` | Omit `thinking`. Set `output_config.effort` to `low` for speed. |
| `thinking: {type: "disabled"}` | Claude Sonnet 5.5 | `"thinking.type.disabled" is not supported for this model. Use "thinking.type.between_tools" for the lowest thinking setting, or ...` | Try adaptive + `effort: "low"`. Else `{type: "between_tools"}` at effort `high` or below. |
| `thinking: {type: "enabled", budget_tokens: N}` | Claude Opus 4.7 and later, Sonnet 5 and later, Haiku 5.5, Fable | 400 | `{type: "adaptive"}` + `output_config.effort`. |
| `thinking: {type: "disabled"}` with effort `xhigh` or `max` | Claude Opus 5, Haiku 5.5 | `output_config.effort 'xhigh' is not supported when thinking is disabled on this model. Use effort 'high' or below, or enable thinking.` | Lower effort or enable thinking. |
| `thinking: {type: "between_tools"}` | Any model except Claude Sonnet 5.5 | `"thinking.type.between_tools" is not supported for this model.` | Drop the field when re-sending to another model. |
| `tool_choice: {type: "any"}` or `{type: "tool", ...}` | Claude Opus 5.5, Sonnet 5.5, Fable 5.1 | `tool_choice: type "tool" and "any" are not supported for this model.` | `auto` + `strict: true` + prompt instruction, or `output_config.format` for JSON. Check a call happened. |
| `computer_20251124` tool | Claude Opus 5.5, Sonnet 5.5 on Claude API and Google Cloud | `'claude-opus-5-5' does not support tool types: computer_20251124.` | `{"type": "computer_toolset_20260801"}`. Amazon Bedrock still accepts the old tool. |
| `computer_20250124` tool | Claude Haiku 5.5 on Claude API and Google Cloud | 400 | `computer_toolset_20260801`. |
| `temperature`, `top_p`, `top_k` (non-default) | Claude Opus 4.7 and later, Sonnet 5 and later, Haiku 5.5, Fable | 400 | Omit them. Haiku 5.5 accepts only `temperature` 1 and `top_p` 0.99. |
| Assistant prefill (last message is `assistant`) | Claude Opus 4.6 and later, Sonnet 4.6 and later, Haiku 5.5, Fable | 400 | End with a user turn. Use `output_config.format` or a prompt instruction. |
| Replayed thinking block after editing `system`, `tools`, or earlier messages | Claude Fable 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5 (accounts created on or after 2026-08-31) | 400 | Keep history append-only. See `claude-fable-5-1.md`. |
| `fallbacks` on Haiku 5.5 | Claude Haiku 5.5 | A model list returns 400. `"default"` leaves a decline declined. | Handle the refusal in the client. |
| `thinking_budget` and `thinking_level` together | Gemini 3.x | 400 | Send only `thinking_level`. |
| `thinking_level: "minimal"` | Gemini 3.8 Flash | Error | Use `low`, `medium`, or `high`. |
| `reasoning.effort: "none"` or `"minimal"` | GPT-6 Astra, GPT-6.1 Sol | Unsupported | Use `low`. |
| `temperature`, `top_p`, `top_logprobs`, `logprobs` with reasoning on | GPT-6 family | Unsupported | Remove them. |
| Tool calling on Chat Completions | GPT-6 Astra, 6.1 Sol | Unsupported | Use the Responses API. |

## Silent changes (no error, output differs)

| Change | Models | Effect | Fix |
| :----- | :----- | :----- | :-- |
| Thinking on by default | Claude Opus 5, Sonnet 5, Haiku 5.5 | `max_tokens` shared with thinking. Replies truncate. `content[0]` may be a `thinking` block. | Raise `max_tokens` (64K for long agent turns). Read blocks by `type`. |
| Default effort `medium` | Claude Opus 5.5, Haiku 5.5 | Less thinking than the old `high` default. | Set `effort` explicitly. Re-run the sweep. |
| `thinking.display` default `"omitted"` | Claude Opus 4.7 and later, Sonnet 5 and later, Fable | Thinking text is empty. UI shows a long pause. | `display: "summarized"`. |
| Progress notes moved into `thinking` blocks | Claude Opus 5.5, Sonnet 5.5, Fable 5.1 | UI goes quiet between tool calls. | `display: "updates"` (beta) and render non-empty `thinking` blocks. |
| New tokenizer, about 30% more tokens | Claude Sonnet 5 and later (vs 4.6), Haiku 5.5 (vs 4.5) | Cost and context budgets shift. | Recount with `count_tokens`. |
| Classifier refusals (HTTP 200, `stop_reason: "refusal"`) | Claude Fable 5.1, Opus 5 and 5.5, Sonnet 5.5, Haiku 5.5 | Code reading `content[0]` breaks. | Branch on `stop_reason`. Add a fallback where supported. |
| More literal instruction following | Claude Opus 4.7 and later | Vague prompts behave differently. | State format, verbosity, and scope. |
| More tool-call iteration, smaller reasoning steps | Gemini 3.8 Flash | More tokens on long tasks. | Lower `thinking_level`. |
| More clarifying questions, long formatted answers | GPT-6 Astra | Stalls on autonomous work, verbose output. | Prompt for action and style. See `gpt-6.md`. |

## Where to go next

- Model-specific steps: `models/INDEX.md`.
- Rollout and rollback: `migration-playbook.md`, `migration-patterns.md`.
- Proving it worked: `validation-proof.md`, `benchmarking.md`.

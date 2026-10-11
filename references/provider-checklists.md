# Provider Checklists

Provider-specific reminders to use during migration.

## Anthropic-family migration checklist

- Verify target model ID exists and is active.
- Check request parameter compatibility for newer model versions.
- Re-check thinking/reasoning configuration defaults.
- Re-check prompt and tool guidance if model follows instructions more literally.
- Verify structured output mode and schema handling.
- Run at least one streamed and one non-streamed smoke test where relevant.

- Check for the 5.x-era breaking changes when targeting the latest models:
  `thinking: {type: "disabled"}` and `budget_tokens` rejected, forced
  `tool_choice` (`any`, `tool`) rejected, sampling parameters and assistant
  prefill rejected, computer use via `computer_toolset_20260801`.
- Handle `stop_reason: "refusal"` before reading `content`. Add a fallback.
- Keep conversations append-only when replaying thinking blocks (preserved
  thinking).
- Set `output_config.effort` explicitly. Defaults differ per model.

For version-specific changelogs, breaking changes, and quirks, start at
`references/models/INDEX.md` (e.g. `claude-opus-5-5.md`).

Reference: [Anthropic model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)

## OpenAI-family migration checklist

- Verify target model and endpoint compatibility.
- Re-check response format/tool-calling schema expectations.
- Confirm any reasoning-effort/config fields are valid for target model.
- Validate JSON mode/structured output behavior if used.
- Re-check system prompt behavior under new model family.
- Use the Responses API for tool calling on the newest models.
- Remove `temperature`, `top_p`, and `logprobs` when reasoning is on.
- Replace unsupported effort values (`none`, `minimal`) per the target model.
- Re-check prompt caching parameters (for example `prompt_cache_options.ttl`).

For version-specific changelogs, reasoning effort levels, and migration steps,
start at `references/models/INDEX.md` (e.g. `gpt-6.md`).

Reference: [OpenAI models](https://developers.openai.com/api/docs/models)

## Gemini-family migration checklist

- Verify target model availability and generation config support.
- Confirm function-calling/tool schema compatibility.
- Re-check safety settings and blocked-output behavior.
- Validate multimodal pathways if image/file inputs are used.
- Confirm output format consistency against existing parsers.
- Replace `thinking_budget` with `thinking_level`. Do not send both.
- Remove `temperature`, `top_p`, `top_k`, `candidate_count`, and prefilled
  model turns on Gemini 3 and later.
- Re-check function-calling response shape and thought-signature handling.

For version-specific steps, start at `references/models/INDEX.md` (e.g.
`gemini-3-8-flash.md`).

Reference: [Gemini model versions](https://ai.google.dev/gemini-api/docs/models)

## Self-hosted or open-weight model migration checklist

- Verify context window, tokenizer, and stop-sequence behavior.
- Re-tune prompts that relied on vendor-specific instruction behavior.
- Re-check latency and throughput under expected load.
- Validate deterministic mode, seed behavior, and sampling controls.
- Re-test tool-calling compatibility if using adapter layers.

## Cross-provider migration checklist

- Normalize output contracts first (shape/schema), then style.
- Keep parser contracts strict and provider wrappers isolated.
- Avoid provider-specific prompt hacks in shared templates.
- Add compatibility adapters rather than scattering conditionals everywhere.
- Keep dual-run shadow mode for critical workloads before cutover.

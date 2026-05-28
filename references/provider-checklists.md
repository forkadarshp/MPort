# Provider Checklists

Provider-specific reminders to use during migration.

## Anthropic-family migration checklist

- Verify target model ID exists and is active.
- Check request parameter compatibility for newer model versions.
- Re-check thinking/reasoning configuration defaults.
- Re-check prompt and tool guidance if model follows instructions more literally.
- Verify structured output mode and schema handling.
- Run at least one streamed and one non-streamed smoke test where relevant.

For version-specific changelogs, breaking changes, and quirks, see the
dedicated model guides in `references/models/` (e.g. `claude-opus-4-8.md`).

Reference: [Anthropic model deprecations](https://docs.anthropic.com/en/docs/resources/model-deprecations)

## OpenAI-family migration checklist

- Verify target model and endpoint compatibility.
- Re-check response format/tool-calling schema expectations.
- Confirm any reasoning-effort/config fields are valid for target model.
- Validate JSON mode/structured output behavior if used.
- Re-check system prompt behavior under new model family.

For version-specific changelogs, reasoning effort levels, and migration steps,
see the dedicated model guides in `references/models/` (e.g. `gpt-5-5.md`).

Reference: [OpenAI model endpoint compatibility](https://platform.openai.com/docs/models)

## Gemini-family migration checklist

- Verify target model availability and generation config support.
- Confirm function-calling/tool schema compatibility.
- Re-check safety settings and blocked-output behavior.
- Validate multimodal pathways if image/file inputs are used.
- Confirm output format consistency against existing parsers.

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

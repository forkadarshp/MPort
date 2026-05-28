# Claude Opus 4.8

Released: May 28, 2026
Model ID: `claude-opus-4-8`
Pricing: $5 / $25 per million input / output tokens (unchanged from 4.7)

## Changelog (vs Opus 4.7)

- **Effort control**: User-selectable effort levels in Claude.ai, Cowork, and
  API. Controls how much compute Claude applies per task. Token allocation
  recalibrated — re-baseline any tuned effort settings.
- **Dynamic workflows** (research preview): Claude Code can plan complex tasks
  and spawn hundreds of parallel subagents in a single session. Useful for
  large-scale refactors, migrations, and repo-wide analysis.
- **Mid-task instructions**: Messages API accepts `role: "system"` entries
  within the `messages` array (after a user turn). Update instructions mid-task
  without breaking prompt cache or routing through a user turn.
- **Lower prompt cache minimum**: Reduced to 1,024 tokens (down from prior
  threshold).
- **Fast mode**: 2.5x speed, now 3x cheaper than previous versions. Available
  as research preview on the API.
- **Refusal details**: `stop_details` field on refusal responses is now public.
  Returns category (`cyber`, `bio`, or `null`) plus explanation.

## Performance improvements

- Sharper judgment and reduced hallucinations in long-running agentic tasks.
- Gains on SWE-Bench Pro, Online-Mind2Web, and multidisciplinary reasoning.
- Better honesty — less likely to make unsupported claims.
- More effective at managing autonomous, long-running workflows.

## Migration from Opus 4.7

Drop-in upgrade. No breaking API changes.

| Step | Action |
| :--- | :----- |
| Model ID | Change to `claude-opus-4-8` |
| Effort settings | Re-baseline — token allocation recalibrated |
| Mid-task instructions | Optional — new capability, no action needed |
| Fast mode | Optional — available if latency is a priority |

## Migration from Opus 4.6 or earlier

Must apply **all Opus 4.7 breaking changes first**, then update model ID.

### Opus 4.7 breaking changes (required)

| Change | Detail |
| :----- | :----- |
| Sampling parameters | Setting `temperature`, `top_p`, or `top_k` to non-default values returns 400. Remove them. |
| Extended thinking | Replace manual extended thinking config with `{type: "adaptive"}` and `effort` parameter. |
| Tokenizer | New tokenizer — re-evaluate cost estimates and token limits. |
| Assistant prefills | Assistant message prefills return 400. Use structured outputs or `output_config.format` instead. |

After applying these, proceed with the 4.7 → 4.8 migration above.

## Quirks and best practices

- **Literal instruction following**: Opus 4.8 (inherited from 4.7) follows
  instructions more literally. Vague or implicit instructions may produce
  different results than on 4.6. Be explicit about format, verbosity, and
  scope.
- **Effort recalibration**: If you tuned effort levels on 4.7, retest on 4.8.
  The token budget per effort level has changed.
- **Mid-task instruction pattern**: Use mid-conversation system messages to
  inject updated context (e.g., new files discovered, scope changes) without
  restarting the prompt. Preserves cache hits.
- **Dynamic workflow orchestration**: For large migrations, leverage dynamic
  workflows to parallelize discovery, classification, and implementation across
  subagents. Each subagent gets its own context window.
- **Refusal transparency**: Monitor `stop_details` on safety refusals to
  distinguish content-policy blocks from model uncertainty.
- **Prompt caching**: With the lower 1,024-token minimum, cache even smaller
  system prompts for cost savings on high-volume workloads.

## Model ID reference

| Version | Model ID | Status |
| :------ | :------- | :----- |
| Opus 4.8 | `claude-opus-4-8` | Current (GA) |
| Opus 4.7 | `claude-opus-4-7` | Active |
| Opus 4.6 | `claude-opus-4-6` | Active |
| Opus 4.5 | `claude-opus-4-5` | Active |
| Opus 4.1 | `claude-opus-4-1` | Active |
| Opus 4 | `claude-opus-4-20250514` | Deprecated soon |

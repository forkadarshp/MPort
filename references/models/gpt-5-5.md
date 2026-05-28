# GPT-5.5

Released: April 23, 2026 (API: April 24, 2026)
Model ID: `gpt-5.5`
Pricing: $5 / $30 per million input / output tokens
Cached input: $0.50 per million tokens
Long-context (>270k input): 2x input, 1.5x output

## Variants

| Variant | Model ID | Use case | Pricing (in/out) |
| :------ | :------- | :------- | :---------------- |
| GPT-5.5 | `gpt-5.5` | Complex agentic tasks, coding, reasoning | $5 / $30 |
| GPT-5.5 Pro | `gpt-5.5-pro` | High-stakes deep reasoning, max compute | $30 / $180 |
| GPT-5.5 Instant | `gpt-5.5-instant` | Fast everyday tasks, low latency | TBD |

## Reasoning effort levels

GPT-5.5 supports a `reasoning.effort` parameter that controls internal
chain-of-thought depth. Reasoning tokens are billed as output tokens — higher
effort = higher cost.

| Level | When to use | Trade-off |
| :---- | :---------- | :-------- |
| `none` | Simple lookups, classification, formatting | Fastest, cheapest, no reasoning overhead |
| `low` | Straightforward Q&A, information retrieval | Fast with minimal reasoning |
| `medium` (default) | Most professional workflows | Balanced speed / quality / cost |
| `high` | Complex multi-step problems, coding, analysis | Higher accuracy, more reasoning tokens |
| `xhigh` | Hardest problems — novel research, deep debugging, ambiguous goals | Maximum reasoning depth, highest cost and latency |

### Effort tuning best practices

- Start with `medium` — only escalate if output quality is insufficient.
- For batch/eval workloads, run a sample at `medium` vs `high` to quantify
  the quality delta before committing to higher cost.
- `xhigh` should be reserved for genuinely hard problems — it can 3–5x your
  output token cost.
- `none` is useful for structured-output-only calls where the model just needs
  to follow a schema, not reason about it.

## Key features

- **Natively omnimodal**: Unified architecture for text, images, audio, and
  video — no separate endpoints.
- **1M token context window**: Full million-token input capacity.
- **128k output tokens**: Large output generation in a single pass.
- **Responses API**: Recommended over Chat Completions for agentic workloads.
  Built-in support for tool calls, structured outputs, and reasoning control.
- **Structured outputs**: 100% schema adherence via constrained decoding.
  Define schemas with JSON Schema or Pydantic — no post-processing needed.
- **Tool use**: Native web search, computer use (browser/desktop navigation),
  hosted shell, and multi-step tool orchestration.
- **Prompt caching**: Cached input at $0.50/M tokens (10x cheaper than
  uncached).
- **Tool search**: Built-in tool discovery and selection for complex workflows.

## Changelog highlights

| Date | Change |
| :--- | :----- |
| Apr 23, 2026 | GPT-5.5 and GPT-5.5 Pro released |
| May 5, 2026 | GPT-5.5 Instant released (default for ChatGPT free tier) |
| May 12, 2026 | Older DALL·E snapshots and Realtime API Beta deprecated |
| May 28, 2026 | GPT-5.5 Instant updated — improved style/readability; canvas dropped from Instant/Thinking |

## Migration from GPT-4o

This is a significant migration — not just a model ID swap.

### Step 1: API surface

| Area | Change required |
| :--- | :-------------- |
| Endpoint | Migrate to **Responses API** for best results. Chat Completions still works but is not optimized for reasoning-heavy or agentic workloads. |
| Model ID | Change to `gpt-5.5` |
| Reasoning | New `reasoning.effort` parameter (default `medium`). GPT-4o had no equivalent — if you were using `o3` reasoning, effort levels map similarly. |
| Structured outputs | Now 100% schema-adherent via constrained decoding. Remove post-processing hacks for malformed JSON. |
| Tool schemas | Verify tool definitions — GPT-5.5 has stricter schema validation and better tool selection. |

### Step 2: Prompt strategy

| Area | Guidance |
| :--- | :------ |
| Over-prompting | GPT-5.5 follows instructions more literally and is more capable. Remove verbose scaffolding, hand-holding, and workarounds from GPT-4o prompts. |
| Outcome-first | Focus system messages on goals, success criteria, and output shape — not step-by-step process. The model plans its own execution. |
| Fresh baseline | Don't carry over legacy prompt hacks. Start with a clean prompt and add constraints only as needed. |
| Few-shot examples | Still effective for GPT-5.5 — use them for format/style calibration. |
| Chain-of-thought | For `gpt-5.5`, explicit CoT prompting ("think step-by-step") still helps. For `o3` models, avoid it — they handle reasoning internally. |

### Step 3: Operational changes

| Area | Notes |
| :--- | :---- |
| Latency | Higher than GPT-4o, especially at `high`/`xhigh` effort. Add loading indicators for user-facing apps. |
| Cost | Output tokens are more expensive ($30 vs GPT-4o's $15). Reasoning tokens add to output cost. Monitor spend during first week. |
| Output quality | Cleaner, more structured output. Update downstream parsers that expected "messy" GPT-4o responses. |
| Tokenizer | Different tokenizer — re-evaluate token counts and cost estimates. |
| Snapshot pinning | Use `gpt-5.5` for latest, or pin to a dated snapshot for stability. |

### Step 4: Parallel testing

- Run GPT-4o and GPT-5.5 side-by-side for critical workloads.
- Log response differences systematically.
- Compare on: correctness, format adherence, latency, cost, tool-call accuracy.
- Only cut over after evidence supports it.

## Migration from o3 / o3-mini

If migrating from o-series reasoning models:

| Area | Notes |
| :--- | :---- |
| Model ID | `gpt-5.5` or `gpt-5.5-pro` for hardest problems |
| Reasoning effort | Maps directly: `low`, `medium`, `high` work the same. `xhigh` is the new maximum. |
| Prompt style | GPT-5.5 benefits from more structured prompts than o3. Add explicit format/output constraints. |
| Tool use | GPT-5.5 has broader native tool support. Verify tool schemas still match. |
| Cost | GPT-5.5 is generally cheaper than o3-pro for equivalent quality on most tasks. |

## Quirks and best practices

- **Reasoning tokens are hidden by default**: Unlike o3's visible reasoning
  summaries, GPT-5.5's reasoning tokens are internal. Use the API's
  `reasoning` config to control depth, but don't expect to see the
  chain-of-thought unless you opt in.
- **Responses API is the future**: Chat Completions works but is a legacy
  surface. New features (tool search, computer use, hosted shell) are
  Responses API only.
- **Structured output strictness**: GPT-5.5's constrained decoding means your
  schema must be valid. Loose/partial schemas that "worked" on GPT-4o may
  cause errors.
- **Canvas deprecation**: Canvas is no longer available in GPT-5.5 Instant or
  Thinking variants. If your workflow depended on canvas, use legacy models
  temporarily.
- **Prompt caching ROI**: At $0.50/M for cached input (vs $5/M uncached),
  caching is a 10x cost reduction. Cache system prompts and static context
  aggressively.
- **Long-context pricing jump**: Above ~270k input tokens, pricing doubles for
  input. Chunk large contexts or use summarization if cost-sensitive.
- **Hybrid architecture**: Consider using GPT-5.5 for execution and o3 for
  planning/judgment in complex workflows. They complement each other well.

## Model ID reference

| Version | Model ID | Status |
| :------ | :------- | :----- |
| GPT-5.5 | `gpt-5.5` | Current (GA) |
| GPT-5.5 Pro | `gpt-5.5-pro` | Current (GA) |
| GPT-5.5 Instant | `gpt-5.5-instant` | Current (GA) |
| GPT-4o | `gpt-4o` | Active |
| o3 | `o3` | Active |
| o3-mini | `o3-mini` | Active |

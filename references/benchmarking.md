# Migration Benchmarking

Optional. Produces a pre/post evidence report that quantifies a migration —
both the raw model delta and the value the skill's enhancements added.

Read this when the user opts into benchmarking (asked once in Phase 0). If they
decline, skip all benchmark steps and omit the Benchmark Results report section.

## The three arms

A migration changes two things at once: the model *and* the system around it
(prompts, tool specs, params). To attribute gains correctly, measure three
configurations on the **same input set and same metrics**:

| Arm | Config | Isolates |
| :-- | :----- | :------- |
| A — baseline | old model + old prompts/system | starting point |
| B — naive swap | new model + old prompts/system | raw model delta |
| C — ModelPort-enhanced | new model + skill-enhanced system | skill's added value |

Arm B is the honest control: it shows what a search-and-replace upgrade alone
would have produced. C − B is the migration work's contribution.

## When to capture each arm

The phase pipeline produces the arms for free — capture at the boundaries:

- **Arm A** — Phase 0, *before any edit*. Once the repo is touched, the baseline
  is gone. If not captured here, it cannot be reconstructed.
- **Arm B** — Phase 4, after runtime/API compatibility edits (step 1) but
  *before* prompt/agent tuning (step 2). At this point it is new model + old
  prompts.
- **Arm C** — Phase 5, after all tuning is complete.

## Dimensions

Pick the subset that matters for the workload; do not pad with irrelevant
metrics. Default migration-relevant set:

| Dimension | Metric | How |
| :-------- | :----- | :-- |
| Quality / correctness | task success rate, eval pass@k | fixed eval set; LLM-as-judge or unit checks |
| Output contract | schema-valid / parse-success rate | run outputs through the real parser/validator |
| Tool calling | right-tool rate, valid-args rate, invocation rate | compare tool calls vs expected per case |
| Latency | TTFT, end-to-end p50/p95, tokens/sec | ≥20 runs/case; report percentiles, not means |
| Cost | input/output tokens, cost per request | token counts × current per-token price |
| Safety / behavior | refusal rate, hallucination rate | adversarial + factual probe set |
| Robustness | adversarial / injection / long-context pass rate | stress subset of the eval set |

LLM-as-a-judge: use a fixed rubric and a separate judge model; score all arms
with the *same* judge and rubric in the same run to keep scores comparable.

## Composite score

Optional single number for a leaderboard. Normalize each dimension to [0,1]
(higher = better; invert latency/cost/refusal), then weight by business
priority. Default weighting:

```text
composite = 0.50 * quality + 0.30 * cost_efficiency + 0.20 * speed
```

Always print the weights next to the score. Never report a composite without
the per-dimension rows behind it.

## Method (keep comparisons honest)

- Same eval set, same cases, same order across all three arms.
- Fix sampling: identical effort/decoding settings per arm where the API allows;
  note any forced differences (e.g. removed `temperature` on Opus 4.7+).
- Disable or warm caches identically; cold-cache latency and warm-cache latency
  are different measurements — label which one.
- Latency: multiple runs, report p50/p95, exclude the first (cold) run or label
  it.
- State sample size `n`. Small `n` → mark deltas as indicative, not significant.
- Numbers in this repo's examples are **illustrative**, not measured. Never
  present sample numbers as real results.

## Presentation

Leaderboard table, arms as columns, dimensions as rows, best cell per row called
out. Example shape (illustrative numbers):

```text
╭──────────────────────┬────────────┬────────────┬────────────╮
│ metric               │ baseline   │ naive swap │ ModelPort  │
│                      │ (old/old)  │ (new/old)  │ (new/enh.) │
├──────────────────────┼────────────┼────────────┼────────────┤
│  task success        │        82% │        84% │        91% │
│  output contract     │        93% │        89% │        98% │
│  tool-call accuracy  │        90% │        83% │        96% │
│  p95 latency         │       3.9s │       2.4s │       2.6s │
│  cost / req          │     $0.052 │     $0.047 │     $0.045 │
│  refusal / halluc.   │       2.8% │       2.1% │       1.4% │
├──────────────────────┼────────────┼────────────┼────────────┤
│  composite (50/30/20)│       0.80 │       0.83 │       0.91 │
╰──────────────────────┴────────────┴────────────┴────────────╯
```

Follow the table with one line of attribution: model delta (B − A), skill delta
(C − B), net (C − A).

## Cross-links

- Proof gates and diagnose-patch-retry: `validation-proof.md`
- Rollout metrics for staged deploys: `migration-patterns.md`
- Per-model cost/tokenizer notes for the cost dimension: `models/`

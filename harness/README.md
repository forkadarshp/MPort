# Migration Benchmark Harness

A runnable, closed-loop evaluator for the three-arm migration benchmark
described in [`../references/benchmarking.md`](../references/benchmarking.md).
Run a scenario, read the leaderboard and the failing cases, tighten the
enhanced system, and re-run — iterating until the migrated system measurably
beats both the baseline and a raw model swap.

## The three arms

| Arm | Config | Isolates |
| --- | --- | --- |
| A baseline | old model + baseline prompt | starting point |
| B naive swap | new model + baseline prompt | raw model delta |
| C ModelPort | new model + enhanced prompt | the skill's added value |

## Quickstart

```bash
# offline, deterministic — no API key needed
python3 run.py --provider sim

# real measured numbers — needs ANTHROPIC_API_KEY and `pip install anthropic`
python3 run.py --provider anthropic
```

Output: a leaderboard (task success, output-contract conformance, tool-call
accuracy, p95 latency, cost/req, weighted composite), an attribution line
(model delta B−A, skill delta C−B, net C−A), and the list of cases the
ModelPort arm still fails — your to-do list for the next iteration.

## The loop

1. Run the harness.
2. Read the leaderboard + failing cases.
3. Tighten the enhanced prompt/config for the failing dimension(s).
4. Re-run; confirm the composite and the skill delta (C−B) went up.

This is exactly how the bundled scenario was tuned: a vague enhanced prompt
scored a **negative** skill delta (it cost more without lifting quality); making
the contract explicit (JSON-only, enumerated schema, no prose) moved ModelPort
from last place to a clear win.

## Providers

- **`sim`** — offline and deterministic. Outputs are a *simulation* driven only
  by prompt explicitness and a per-model "literalness" knob (the documented
  Opus 4.7+ trait: newer models follow instructions more literally, punishing
  vague prompts and rewarding precise ones). The grading, scoring, and
  leaderboard pipeline is real; **the numbers are illustrative, not measured.**
- **`anthropic`** — real Messages API calls. Same graders, real numbers.

## Define your own scenario

Copy `scenarios/support_triage.json` and edit:

- `models` — old/new model IDs
- `prompts.baseline` / `prompts.enhanced` — the configs for arms A/B vs C
- `tools`, `categories` — the task surface
- `eval_cases` — inputs + expected `{category, tool, args}` and a `difficulty`
- `sim` — per-model knobs for the offline simulator (ignored by `--provider anthropic`)

## Files

- `run.py` — orchestrates the three arms, grades, prints the leaderboard
- `graders.py` — provider-agnostic scoring (contract, tool, task)
- `providers.py` — `SimProvider` (offline) + `AnthropicProvider` (real)
- `scenarios/` — scenario fixtures
- `tests/` — `python3 -m unittest discover -s tests`

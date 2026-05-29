#!/usr/bin/env python3
"""Run the three-arm migration benchmark and print a leaderboard.

Arms (same eval set, same graders):
  A baseline    = old model + baseline prompt
  B naive swap  = new model + baseline prompt   (raw model delta)
  C ModelPort   = new model + enhanced prompt    (skill's added value)

Usage:
  python run.py --scenario scenarios/support_triage.json --provider sim
  python run.py --provider anthropic   # real numbers; needs ANTHROPIC_API_KEY
"""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

from graders import grade_case
from providers import get_provider


def run_arm(provider, model, prompt, scenario, prices):
    cases, rows = scenario["eval_cases"], []
    lat, costs = [], []
    fails = []
    for case in cases:
        resp = provider.generate(model, prompt, case)
        scores = grade_case(resp, case["expected"])
        lat.append(resp.latency_ms)
        costs.append(resp.tokens_in * prices["price_in"] + resp.tokens_out * prices["price_out"])
        rows.append(scores)
        if not all(scores.values()):
            fails.append((case["id"], scores))
    n = len(cases)
    return {
        "task": sum(r["task"] for r in rows) / n,
        "contract": sum(r["contract"] for r in rows) / n,
        "tool": sum(r["tool"] for r in rows) / n,
        "p50_ms": statistics.median(lat),
        "p95_ms": sorted(lat)[max(0, int(0.95 * n) - 1)],
        "cost": sum(costs) / n,
        "fails": fails,
    }


def composite(arms):
    """0.50 quality + 0.30 cost-efficiency + 0.20 speed.

    quality = mean(task, contract, tool). cost/speed are scored *relative to the
    baseline arm* and bounded, so a small absolute cost/latency difference only
    moves the score a little — quality stays dominant. (Min-max normalization
    across arms is deliberately avoided: with near-equal costs it amplifies
    rounding into a full-weight swing and can rank a worse arm first.)
    """
    base = arms[0]

    def contrib(factor: float) -> float:  # factor > 1 == better than baseline
        return max(0.0, min(1.0, 0.5 + 0.5 * (factor - 1.0)))

    out = []
    for a in arms:
        quality = (a["task"] + a["contract"] + a["tool"]) / 3
        cost_factor = base["cost"] / a["cost"] if a["cost"] else 1.0
        speed_factor = base["p95_ms"] / a["p95_ms"] if a["p95_ms"] else 1.0
        out.append(0.5 * quality + 0.3 * contrib(cost_factor) + 0.2 * contrib(speed_factor))
    return out


def leaderboard(arms):
    M, V = 22, 12
    bar = lambda l, m, r: l + "─" * M + m + ("─" * V + m) * 2 + "─" * V + r
    def hrow(c0, c1, c2, c3):
        cells = [" " + c0.ljust(M - 1)] + [" " + c.ljust(V - 1) for c in (c1, c2, c3)]
        return "│" + cells[0] + "│" + cells[1] + "│" + cells[2] + "│" + cells[3] + "│"
    def row(label, a, b, c):
        cells = [label.ljust(M)] + [x.rjust(V - 1) + " " for x in (a, b, c)]
        return "│" + cells[0] + "│" + cells[1] + "│" + cells[2] + "│" + cells[3] + "│"

    pct = lambda x: f"{round(x * 100)}%"
    sec = lambda ms: f"{ms / 1000:.1f}s"
    usd = lambda c: f"${c:.4f}"
    comp = composite(arms)

    out = [bar("╭", "┬", "╮"),
           hrow("metric", "baseline", "naive swap", "ModelPort"),
           hrow("", "(old/old)", "(new/old)", "(new/enh.)"),
           bar("├", "┼", "┤"),
           row("  task success", *[pct(a["task"]) for a in arms]),
           row("  output contract", *[pct(a["contract"]) for a in arms]),
           row("  tool-call accuracy", *[pct(a["tool"]) for a in arms]),
           row("  p95 latency", *[sec(a["p95_ms"]) for a in arms]),
           row("  cost / req", *[usd(a["cost"]) for a in arms]),
           bar("├", "┼", "┤"),
           row("  composite (50/30/20)", *[f"{x:.2f}" for x in comp]),
           bar("╰", "┴", "╯")]
    return "\n".join(out), comp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", default=str(Path(__file__).parent / "scenarios/support_triage.json"))
    ap.add_argument("--provider", default="sim", choices=["sim", "anthropic"])
    ap.add_argument("--out", default=str(Path(__file__).parent / "results.json"))
    args = ap.parse_args()

    scenario = json.loads(Path(args.scenario).read_text())
    provider = get_provider(args.provider, scenario)
    old, new = scenario["models"]["old"], scenario["models"]["new"]
    base_p, enh_p = scenario["prompts"]["baseline"], scenario["prompts"]["enhanced"]

    arm_specs = [("A baseline", old, base_p), ("B naive swap", new, base_p), ("C ModelPort", new, enh_p)]
    arms = [run_arm(provider, m, p, scenario, scenario["sim"][m]) for _, m, p in arm_specs]

    table, comp = leaderboard(arms)
    print(f"\nScenario: {scenario['name']}  |  provider: {args.provider}  |  n={len(scenario['eval_cases'])}")
    if args.provider == "sim":
        print("(simulated numbers — illustrative; run --provider anthropic for measured results)")
    print(table)
    print(f"\nattribution:  model delta (B−A) {comp[1] - comp[0]:+.2f}   "
          f"skill delta (C−B) {comp[2] - comp[1]:+.2f}   net (C−A) {comp[2] - comp[0]:+.2f}")

    cfails = arms[2]["fails"]
    if cfails:
        broken = sorted({k for _, s in cfails for k, ok in s.items() if not ok})
        print(f"\nModelPort arm still failing {len(cfails)} case(s) on: {', '.join(broken)}")
        print("  cases: " + ", ".join(cid for cid, _ in cfails))
        print("  -> next iteration: tighten the enhanced prompt for the failing dimension(s).")
    else:
        print("\nModelPort arm passes every case. ")

    Path(args.out).write_text(json.dumps(
        {"scenario": scenario["name"], "provider": args.provider,
         "arms": {spec[0]: {k: v for k, v in a.items() if k != "fails"} for spec, a in zip(arm_specs, arms)},
         "composite": dict(zip([s[0] for s in arm_specs], comp))}, indent=2))


if __name__ == "__main__":
    main()

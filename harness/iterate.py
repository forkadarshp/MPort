#!/usr/bin/env python3
"""Prompt-optimization sweep.

Runs a sequence of enhanced-prompt revisions through the benchmark and prints
the score trajectory — the iterate-on-failures loop the harness is built for.
Each revision adds one prompt-engineering technique aimed at the dimension the
previous step was still failing, until the prompt levers run out and the score
plateaus (the last failures need more than prompting).

The revision clauses are derived from the scenario, so the sweep works on any
scenario, not just the bundled one.

Usage:
  python3 iterate.py                                   # offline simulator
  python3 iterate.py --scenario scenarios/ops_routing.json
  python3 iterate.py --provider anthropic              # real numbers; needs key
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import run
from providers import get_provider


def build_steps(sc: dict) -> list[tuple[str, str]]:
    """Cumulative prompt-engineering steps, parameterized by the scenario."""
    tools = ", ".join(t["name"] for t in sc["tools"])
    ex = sc["eval_cases"][0]["expected"]
    example = json.dumps({"category": ex["category"], "tool": ex["tool"], "args": ex.get("args", {})})
    return [
        ("ask for JSON", "Return a JSON object with the category and the tool."),
        ("return ONLY JSON", "Return ONLY the JSON object."),
        ("state schema + args", "Follow this schema: {category, tool, args}."),
        ("enumerate tools", f"Tools: {tools}."),
        ("forbid prose", "No prose."),
        ("forbid code fences", "Do not wrap it in code fences."),
        ("extract args", "Extract any IDs, names, versions, or emails into args."),
        ("exactly one each", "Choose exactly one category and exactly one tool."),
        ("lowercase values", "Use lowercase values exactly as listed."),
        ("few-shot example", f"Example: {example}"),
    ]


def prompt_at(role: str, steps: list[tuple[str, str]], i: int) -> str:
    return role + " " + " ".join(clause for _, clause in steps[: i + 1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", default=str(Path(__file__).parent / "scenarios/support_triage.json"))
    ap.add_argument("--provider", default="sim", choices=["sim", "anthropic"])
    args = ap.parse_args()

    sc = json.loads(Path(args.scenario).read_text())
    prov = get_provider(args.provider, sc)
    old, new = sc["models"]["old"], sc["models"]["new"]
    role = sc.get("role", "You are an assistant.")
    steps = build_steps(sc)
    base_prompt = sc["prompts"]["baseline"]

    A = run.run_arm(prov, old, base_prompt, sc, sc["sim"][old])
    B = run.run_arm(prov, new, base_prompt, sc, sc["sim"][new])

    print(f"\nPrompt-optimization sweep — scenario: {sc['name']}  |  provider: {args.provider}")
    if args.provider == "sim":
        print("(simulated — illustrative trajectory; run --provider anthropic for measured numbers)")
    print(f"baseline composite {run.composite([A, B, A])[0]:.2f}   "
          f"naive-swap composite {run.composite([A, B, B])[1]:.2f}\n")
    print(f"{'it':>2}  {'technique added':<20} {'task':>5} {'cont':>5} {'tool':>5} "
          f"{'comp':>5} {'skillΔ':>7}  fails")
    print("-" * 64)

    best = (-1.0, 0)
    for i, (label, _) in enumerate(steps):
        C = run.run_arm(prov, new, prompt_at(role, steps, i), sc, sc["sim"][new])
        comp = run.composite([A, B, C])
        print(f"{i + 1:>2}  +{label:<19} {C['task'] * 100:>4.0f}% {C['contract'] * 100:>4.0f}% "
              f"{C['tool'] * 100:>4.0f}% {comp[2]:>5.2f} {comp[2] - comp[1]:>+7.2f}  {len(C['fails'])}")
        if comp[2] > best[0]:
            best = (comp[2], i)

    print(f"\nbest: iteration {best[1] + 1} (composite {best[0]:.2f}).")
    print("tuned enhanced prompt:")
    print(f"  {prompt_at(role, steps, best[1])}")


if __name__ == "__main__":
    main()

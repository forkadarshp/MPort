#!/usr/bin/env python3
"""Prompt-optimization sweep.

Runs a sequence of enhanced-prompt revisions through the benchmark and prints
the score trajectory — the iterate-on-failures loop the harness is built for.
Each revision adds one prompt-engineering technique aimed at the dimension the
previous step was still failing, until the prompt levers run out and the score
plateaus (the last failures need more than prompting).

Usage:
  python3 iterate.py                 # offline simulator
  python3 iterate.py --provider anthropic   # real numbers; needs API key
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import run
from providers import get_provider

BASE = "You are a support-triage assistant. "

# Cumulative prompt-engineering steps. Each entry is (short label, clause added).
STEPS = [
    ("ask for JSON", "Return a JSON object with the category and the tool."),
    ("return ONLY JSON", "Return ONLY the JSON object."),
    ("state schema + args", "Follow this schema: {category, tool, args}."),
    ("enumerate tools", "Tools: lookup_order, issue_refund, reset_password, none."),
    ("forbid prose", "No prose."),
    ("forbid code fences", "Do not wrap it in code fences."),
    ("extract args", "Extract any order_id or email into args."),
    ("exactly one each", "Choose exactly one category and exactly one tool."),
    ("lowercase values", "Use lowercase values exactly as listed."),
    ("few-shot example", 'Example: {"category":"billing","tool":"issue_refund","args":{"order_id":"123"}}'),
]


def prompt_at(step: int) -> str:
    return BASE + " ".join(clause for _, clause in STEPS[: step + 1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", default=str(Path(__file__).parent / "scenarios/support_triage.json"))
    ap.add_argument("--provider", default="sim", choices=["sim", "anthropic"])
    args = ap.parse_args()

    sc = json.loads(Path(args.scenario).read_text())
    prov = get_provider(args.provider, sc)
    old, new = sc["models"]["old"], sc["models"]["new"]
    base_prompt = sc["prompts"]["baseline"]

    # Arms A and B are fixed; only the enhanced prompt (arm C) changes per step.
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
    for i, (label, _) in enumerate(STEPS):
        C = run.run_arm(prov, new, prompt_at(i), sc, sc["sim"][new])
        comp = run.composite([A, B, C])
        skill_delta = comp[2] - comp[1]
        nf = len(C["fails"])
        print(f"{i + 1:>2}  +{label:<19} {C['task'] * 100:>4.0f}% {C['contract'] * 100:>4.0f}% "
              f"{C['tool'] * 100:>4.0f}% {comp[2]:>5.2f} {skill_delta:>+7.2f}  {nf}")
        if comp[2] > best[0]:
            best = (comp[2], i)

    print(f"\nbest: iteration {best[1] + 1} (composite {best[0]:.2f}).")
    print("tuned enhanced prompt:")
    print(f"  {prompt_at(best[1])}")


if __name__ == "__main__":
    main()

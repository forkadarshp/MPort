"""Model providers for the benchmark harness.

A provider turns (model, system_prompt, tools, case) into a normalized
``Response``. The graders then score that Response, so the scoring pipeline is
identical regardless of provider.

- ``SimProvider``  : offline, deterministic. No API key. Its outputs are a
  *simulation* whose only inputs are prompt explicitness and a per-model
  "literalness" knob (the documented Opus 4.7+ trait: newer models follow
  instructions more literally, which punishes vague prompts and rewards precise
  ones). Numbers it produces are illustrative, not measured.
- ``AnthropicProvider`` : real Messages API calls. Produces real numbers. Needs
  ``ANTHROPIC_API_KEY`` and ``pip install anthropic``.
"""

from __future__ import annotations

import json
import time

from graders import Response

# Simulator formula constants (transparent, tunable). See module docstring.
_BOOST_EXPLICIT = 0.30      # precise prompt raises fidelity
_PENALTY_VAGUE = 0.20       # literal model * vague prompt lowers fidelity
_BONUS_LITERAL_EXPLICIT = 0.05  # literal model * precise prompt small bonus


def _clamp(x: float, lo: float = 0.02, hi: float = 0.95) -> float:
    return max(lo, min(hi, x))


def explicitness(prompt: str, scenario: dict) -> dict:
    """Score how precisely a prompt specifies the output contract and tools.

    The marker sets are intentionally granular so there is a long, realistic
    prompt-optimization path (see iterate.py): each technique a revision adds
    raises fidelity a little, until the prompt levers are exhausted and the
    score plateaus (the remaining failures need more than prompting).
    """
    p = prompt.lower()
    contract_markers = [
        "json", "only", "schema", "no prose", "do not wrap",
        "exactly one", "lowercase", "example",
    ]
    c = sum(m in p for m in contract_markers) / len(contract_markers)

    tool_names = [t["name"] for t in scenario["tools"] if t["name"] != "none"]
    enum = sum(name in p for name in tool_names) / max(1, len(tool_names))
    args_marker = 1.0 if "args" in p else 0.0
    extract_marker = 1.0 if "extract" in p else 0.0
    tool_e = 0.6 * enum + 0.2 * args_marker + 0.2 * extract_marker

    return {"contract": c, "tool": tool_e, "task": (c + tool_e) / 2}


class SimProvider:
    """Deterministic simulator. Same input -> same output, no network."""

    def __init__(self, scenario: dict):
        self.scenario = scenario
        self.sim = scenario["sim"]

    def _fidelity(self, e: float, literalness: float, base: float) -> float:
        return _clamp(
            base
            + _BOOST_EXPLICIT * e
            - _PENALTY_VAGUE * literalness * (1 - e)
            + _BONUS_LITERAL_EXPLICIT * literalness * e
        )

    def generate(self, model: str, system_prompt: str, case: dict) -> Response:
        params = self.sim[model]
        L, base = params["literalness"], params["base"]
        e = explicitness(system_prompt, self.scenario)
        d = case["difficulty"]
        expected = case["expected"]

        fid = {m: self._fidelity(e[m], L, base) for m in ("contract", "tool", "task")}
        contract_ok = d <= fid["contract"]
        tool_ok = d <= fid["tool"]
        task_ok = contract_ok and (d <= fid["task"])

        # craft text + tool-call consistent with the chosen outcomes, so the
        # real graders re-derive these scores from actual strings.
        category = expected["category"] if task_ok else _wrong_category(
            expected["category"], self.scenario["categories"]
        )
        if tool_ok:
            tool_name = None if expected["tool"] == "none" else expected["tool"]
            tool_args = dict(expected.get("args", {}))
        else:
            tool_name = None if expected["tool"] != "none" else "lookup_order"
            tool_args = {}

        payload = {"category": category, "tool": expected["tool"] if tool_ok else "none", "args": tool_args}
        if contract_ok:
            text = json.dumps(payload)
        else:
            # contract regression: prose around the JSON -> strict parse fails
            text = f"Sure! Based on the ticket, here's my take: {json.dumps(payload)} Hope that helps."

        tokens_in = max(1, (len(system_prompt) + len(case["input"])) // 4)
        tokens_out = max(1, len(text) // 4)
        # deterministic latency: model base + tiny difficulty-driven jitter
        latency_ms = params["latency_ms"] * (0.9 + 0.2 * d)

        return Response(
            text=text,
            tool_name=tool_name,
            tool_args=tool_args,
            latency_ms=latency_ms,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
        )


def _wrong_category(correct: str, categories: list[str]) -> str:
    for c in categories:
        if c != correct:
            return c
    return correct


class AnthropicProvider:
    """Real Anthropic Messages API backend. Requires ANTHROPIC_API_KEY."""

    def __init__(self, scenario: dict):
        import anthropic  # lazy: only needed for real runs

        self.scenario = scenario
        self.client = anthropic.Anthropic()

    def generate(self, model: str, system_prompt: str, case: dict) -> Response:
        tools = [
            {
                "name": t["name"],
                "description": f"{t['name']} tool",
                "input_schema": {
                    "type": "object",
                    "properties": {a: {"type": "string"} for a in t["args"]},
                    "required": t["args"],
                },
            }
            for t in self.scenario["tools"]
            if t["name"] != "none"
        ]
        start = time.time()
        msg = self.client.messages.create(
            model=model,
            max_tokens=512,
            system=system_prompt,
            tools=tools,
            messages=[{"role": "user", "content": case["input"]}],
        )
        latency_ms = (time.time() - start) * 1000

        text, tool_name, tool_args = "", None, {}
        for block in msg.content:
            if block.type == "text":
                text += block.text
            elif block.type == "tool_use":
                tool_name = block.name
                tool_args = dict(block.input)

        return Response(
            text=text,
            tool_name=tool_name,
            tool_args=tool_args,
            latency_ms=latency_ms,
            tokens_in=msg.usage.input_tokens,
            tokens_out=msg.usage.output_tokens,
        )


def get_provider(name: str, scenario: dict):
    if name == "sim":
        return SimProvider(scenario)
    if name == "anthropic":
        return AnthropicProvider(scenario)
    raise ValueError(f"unknown provider: {name!r} (use 'sim' or 'anthropic')")

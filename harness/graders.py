"""Provider-agnostic graders for the migration benchmark harness.

These score a model Response against a case's expected outcome. They run on the
real text/tool-call a model returns, so the same graders judge both the
simulated provider and the real Anthropic provider.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field


@dataclass
class Response:
    """Normalized model output, independent of which provider produced it."""

    text: str = ""
    tool_name: str | None = None
    tool_args: dict = field(default_factory=dict)
    latency_ms: float = 0.0
    tokens_in: int = 0
    tokens_out: int = 0


def _strip_fence(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        # drop the opening fence line and a trailing fence if present
        t = t.split("\n", 1)[1] if "\n" in t else ""
        if t.rstrip().endswith("```"):
            t = t.rstrip()[:-3]
    return t.strip()


def parse_contract(text: str) -> dict | None:
    """Strict parse: the whole message must be a single JSON object.

    Prose around the JSON (a common regression after a model swap) fails here,
    which is exactly the contract violation we want to catch.
    """
    candidate = _strip_fence(text)
    if not (candidate.startswith("{") and candidate.endswith("}")):
        return None
    try:
        obj = json.loads(candidate)
    except (ValueError, TypeError):
        return None
    return obj if isinstance(obj, dict) else None


def grade_contract(resp: Response) -> bool:
    obj = parse_contract(resp.text)
    if obj is None:
        return False
    return (
        isinstance(obj.get("category"), str)
        and isinstance(obj.get("tool"), str)
        and isinstance(obj.get("args"), dict)
    )


def grade_tool(resp: Response, expected: dict) -> bool:
    want_tool = expected.get("tool", "none")
    want_args = expected.get("args", {}) or {}
    got_tool = resp.tool_name if resp.tool_name is not None else "none"
    if got_tool != want_tool:
        return False
    # expected args must be a subset of what the model supplied
    return all(str(resp.tool_args.get(k)) == str(v) for k, v in want_args.items())


def grade_task(resp: Response, expected: dict) -> bool:
    """Overall success: valid contract AND the right category."""
    obj = parse_contract(resp.text)
    if obj is None:
        return False
    if not grade_contract(resp):
        return False
    return obj.get("category") == expected.get("category")


def grade_case(resp: Response, expected: dict) -> dict:
    return {
        "contract": grade_contract(resp),
        "tool": grade_tool(resp, expected),
        "task": grade_task(resp, expected),
    }

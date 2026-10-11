"""Unit + smoke tests for the benchmark harness. Run: python3 -m unittest."""

import json
import sys
import unittest
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HARNESS))

from graders import Response, grade_contract, grade_task, grade_tool  # noqa: E402
from providers import DEFAULT_MAX_TOKENS, AnthropicProvider, SimProvider, explicitness  # noqa: E402
import run  # noqa: E402


class TestGraders(unittest.TestCase):
    def test_strict_json_passes_contract(self):
        r = Response(text='{"category": "billing", "tool": "none", "args": {}}')
        self.assertTrue(grade_contract(r))

    def test_prose_wrapped_json_fails_contract(self):
        r = Response(text='Sure! Here you go: {"category": "billing", "tool": "none", "args": {}} thanks')
        self.assertFalse(grade_contract(r))

    def test_code_fenced_json_passes(self):
        r = Response(text='```json\n{"category": "account", "tool": "none", "args": {}}\n```')
        self.assertTrue(grade_contract(r))

    def test_tool_match_and_args_subset(self):
        r = Response(tool_name="issue_refund", tool_args={"order_id": "4471", "extra": "x"})
        self.assertTrue(grade_tool(r, {"tool": "issue_refund", "args": {"order_id": "4471"}}))

    def test_tool_name_mismatch_fails(self):
        r = Response(tool_name="lookup_order", tool_args={"order_id": "4471"})
        self.assertFalse(grade_tool(r, {"tool": "issue_refund", "args": {"order_id": "4471"}}))

    def test_tool_none_expected(self):
        r = Response(tool_name=None)
        self.assertTrue(grade_tool(r, {"tool": "none", "args": {}}))

    def test_task_requires_correct_category(self):
        ok = Response(text='{"category": "billing", "tool": "none", "args": {}}')
        wrong = Response(text='{"category": "technical", "tool": "none", "args": {}}')
        self.assertTrue(grade_task(ok, {"category": "billing"}))
        self.assertFalse(grade_task(wrong, {"category": "billing"}))


class TestSimAndLoop(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scenarios = [
            json.loads(p.read_text())
            for p in sorted((HARNESS / "scenarios").glob("*.json"))
        ]
        assert len(cls.scenarios) >= 2, "expected multiple scenario fixtures"

    def test_enhanced_prompt_is_more_explicit(self):
        for sc in self.scenarios:
            with self.subTest(scenario=sc["name"]):
                e_base = explicitness(sc["prompts"]["baseline"], sc)
                e_enh = explicitness(sc["prompts"]["enhanced"], sc)
                self.assertGreater(e_enh["contract"], e_base["contract"])
                self.assertGreater(e_enh["task"], e_base["task"])

    def test_modelport_arm_beats_baseline(self):
        for sc in self.scenarios:
            with self.subTest(scenario=sc["name"]):
                prov = SimProvider(sc)
                old, new = sc["models"]["old"], sc["models"]["new"]
                arms = [
                    run.run_arm(prov, old, sc["prompts"]["baseline"], sc, sc["sim"][old]),
                    run.run_arm(prov, new, sc["prompts"]["baseline"], sc, sc["sim"][new]),
                    run.run_arm(prov, new, sc["prompts"]["enhanced"], sc, sc["sim"][new]),
                ]
                comp = run.composite(arms)
                # enhanced arm should win on quality and on the composite
                self.assertGreater(arms[2]["task"], arms[0]["task"])
                self.assertGreater(comp[2], comp[0])
                self.assertGreater(comp[2], comp[1])


if __name__ == "__main__":
    unittest.main()


class _Block:
    def __init__(self, type, **kw):
        self.type = type
        self.__dict__.update(kw)


class _Msg:
    def __init__(self, content, stop_reason="end_turn"):
        self.content = content
        self.stop_reason = stop_reason
        self.usage = type("U", (), {"input_tokens": 10, "output_tokens": 5})()


class _FakeClient:
    """Records the request and returns a canned message (no network)."""

    def __init__(self, msg):
        self.calls = []
        self.messages = self
        self._msg = msg

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self._msg


def _provider(scenario_extra, msg):
    prov = AnthropicProvider.__new__(AnthropicProvider)  # skip the anthropic import
    prov.scenario = {"tools": [{"name": "lookup", "args": ["id"]}], **scenario_extra}
    prov.client = _FakeClient(msg)
    return prov


class TestAnthropicProviderNewModels(unittest.TestCase):
    CASE = {"input": "where is order 4471?"}

    def test_request_avoids_params_current_models_reject(self):
        prov = _provider({}, _Msg([_Block("text", text="{}")]))
        prov.generate("claude-opus-5-5", "sys", self.CASE)
        sent = prov.client.calls[0]
        for banned in ("temperature", "top_p", "top_k", "thinking", "tool_choice"):
            self.assertNotIn(banned, sent)
        self.assertEqual(sent["max_tokens"], DEFAULT_MAX_TOKENS)
        self.assertEqual(sent["messages"][-1]["role"], "user")  # no prefill

    def test_effort_is_sent_only_when_configured(self):
        prov = _provider({"request": {"effort": "low", "max_tokens": 2048}},
                         _Msg([_Block("text", text="{}")]))
        prov.generate("claude-haiku-5-5", "sys", self.CASE)
        sent = prov.client.calls[0]
        self.assertEqual(sent["output_config"], {"effort": "low"})
        self.assertEqual(sent["max_tokens"], 2048)

    def test_reads_blocks_by_type_after_leading_thinking_block(self):
        msg = _Msg([_Block("thinking", thinking=""),
                    _Block("tool_use", name="lookup", input={"id": "4471"})])
        resp = _provider({}, msg).generate("claude-opus-5-5", "sys", self.CASE)
        self.assertEqual(resp.tool_name, "lookup")
        self.assertEqual(resp.tool_args, {"id": "4471"})

    def test_refusal_grades_as_empty_response(self):
        resp = _provider({}, _Msg([], stop_reason="refusal")).generate(
            "claude-opus-5-5", "sys", self.CASE)
        self.assertEqual(resp.text, "")
        self.assertIsNone(resp.tool_name)

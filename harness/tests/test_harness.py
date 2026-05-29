"""Unit + smoke tests for the benchmark harness. Run: python3 -m unittest."""

import json
import sys
import unittest
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HARNESS))

from graders import Response, grade_contract, grade_task, grade_tool  # noqa: E402
from providers import SimProvider, explicitness  # noqa: E402
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

# Example Migration Report

## 1) Migration Summary

- Model A -> Model B
- `services/assistant`, `prompts/production`

## 2) Scope and Files Changed

- `services/assistant/client.py`
- `services/assistant/model_router.py`
- `prompts/production/system.md`
- `tests/assistant/test_model_config.py`

## 3) Existing Work and Remaining Work

- Existing: FF route for old/new model
- Remaining: Production dashboard (latency/tokens)

## 4) Required Compatibility Fixes

- `client.py`: Model ID -> Model B
- `client.py`: Deprecated param -> supported param
- `model_router.py`: Parser guard -> B contract

## 5) Prompt/Agent Behavior Tuning

- `system.md`: Reduced verbosity
- `system.md`: Tightened tool description

## 6) Validation Results

- Unit/Integration: PASS
- Smoke test: PASS
- Contract check: PASS

## 7) Proof Evidence

- `pytest tests/assistant/test_model_config.py` -> PASS
- Smoke request -> valid contract returned
- Gap: Canary not run locally

## 8) Risks and Follow-up Recommendations

- Risk: Higher token consumption
- Rec: 24h metric watch
- Rec: Keep dual-model fallback

## 9) Rollback Notes

- Toggle `USE_NEW_MODEL=false`
- Legacy prompts in `prompts/legacy/`

## 10) Benchmark Results (optional)

Requested: yes. Eval set `n=120`. Numbers below are **illustrative**.

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

- Model delta (B−A): +0.03 composite — faster, cheaper, but contract/tool regressions
- Skill delta (C−B): +0.08 composite — recovers contract + tool accuracy
- Net (C−A): +0.11 composite

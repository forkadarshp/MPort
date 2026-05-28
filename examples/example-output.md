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

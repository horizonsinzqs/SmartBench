# Anomaly Attribution

Minimal entry points for RQ2.

- `01_prepare_public_sets.py`
  - Flatten the public benchmark and select `100` anomaly samples for AB175 and `100` anomaly samples for TDCS.
- `02_run_judge.py`
  - Run the existing `gpt-5-mini` judge script on those public selections.

Typical usage:

```powershell
python SmartBench/experiments/anomaly_attribution/01_prepare_public_sets.py
python SmartBench/experiments/anomaly_attribution/02_run_judge.py --candidate-models gpt-5 gpt-5-mini deepseek-r1
```

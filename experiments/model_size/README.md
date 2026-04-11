# Model Size

Minimal entry points for RQ3.

- `01_prepare_public_sets.py`
  - Flatten public AB175 and TDCS views and select balanced evaluation subsets.
- `02_run_eval.py`
  - Run the official eval scripts on the selected public subsets for a list of model ids.

Typical usage:

```powershell
python SmartBench/experiments/model_size/01_prepare_public_sets.py
python SmartBench/experiments/model_size/02_run_eval.py --models qwen3-8b qwen3-32b meta-llama/llama-3.1-8b-instruct
```


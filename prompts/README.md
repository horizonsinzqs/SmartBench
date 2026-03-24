# SmartBench Evaluation Prompts

This directory documents the official prompts used when asking LLMs to predict anomaly labels and provide short judgment rationales on SmartBench.

Each prompt document includes:

- the system prompt
- the model-visible input template
- the output JSON schema
- notes on which dataset fields are hidden from the model

Prompt files:

- [context-independent-official-eval.md](context-independent-official-eval.md)
- [context-dependent-official-eval.md](context-dependent-official-eval.md)

Notes:

- In our evaluation, the model's "judgment reason" is represented by `analysis_chain`, a short sequence of observations ending with the final conclusion.
- Official runs also ask the model to return `evidence_devices`. If you only need label plus rationale, you can focus on `label` and `analysis_chain`.
- The public dataset stores ground-truth `label`, `reasoning`, and `evidence_devices` inside each sample file, but these fields are excluded from model input during evaluation.

# SmartBench

SmartBench is a benchmark for evaluating LLM anomaly understanding in smart home environments.

## Experiment Entry Points

Minimal small-experiment scripts are organized under `experiments/`.

## Prompt Templates

Prompt templates for the released benchmark are available in:

- `prompts/context-independent_prompt.txt`
- `prompts/context-dependent_prompt.txt`

These templates are written to match the public benchmark schema released in this repository.

- The context-independent prompt is intended for samples with `environment_context` and `device_states`.
- The context-dependent prompt is intended for samples with `description`, `context`, and `events`.
- The expected model output is a single JSON object with `reasoning`, `label`, and `evidence_devices`.

For inference, ground-truth annotation fields such as `label`, `reasoning`, and `evidence_devices` should not be provided to the model.

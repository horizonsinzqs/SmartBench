# SmartBench

SmartBench is a public benchmark for evaluating LLM perception and reasoning in smart-home anomaly detection.

This repository currently contains:

- `context-independent/`: snapshot-style samples with environment context, device states, ground-truth labels, ground-truth reasoning, and evidence devices.
- `context-dependent/`: event-sequence samples from ARGUS-style traces and TDCS/RBE-style long-context traces.
- `prompts/`: the official evaluation prompts used to ask LLMs to output a label and a short judgment rationale.

## Evaluation Prompt Docs

For reproducibility, the official prompt documentation is included here:

- [prompts/README.md](prompts/README.md)
- [prompts/context-independent-official-eval.md](prompts/context-independent-official-eval.md)
- [prompts/context-dependent-official-eval.md](prompts/context-dependent-official-eval.md)

## Important Note

Public sample JSON files contain ground-truth fields such as `label`, `reasoning`, and `evidence_devices`.
During evaluation, these fields are not shown to the model. The model only sees the model-visible input described in the prompt docs above.

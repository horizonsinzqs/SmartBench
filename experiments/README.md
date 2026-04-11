# SmartBench Experiments

This directory keeps only the minimal code paths needed to run the paper-side and rebuttal-side small experiments.

- `anomaly_attribution/`
  - RQ2. Judge model-generated anomaly explanations with `gpt-5-mini`.
- `model_size/`
  - RQ3. Run the size-scaling evaluation on public `SmartBench` views.
- `context_compression/`
  - RQ4 and rebuttal compression reruns.
- `in_context_learning/`
  - RQ5 few-shot prompt construction and evaluation.
- `rag_bm25/`
  - Rebuttal RAG experiment with split anomaly-only knowledge bases.
- `fusion_dual_anomaly/`
  - Rebuttal dual-anomaly benchmark construction and evaluation.
- `common/`
  - Small shared helpers only.

The public benchmark files under `SmartBench/context-independent/`, `SmartBench/context-dependent/`, and `SmartBench/prompts/` are not modified by these scripts. Derived files are written under each experiment folder's local `artifacts/` directory.


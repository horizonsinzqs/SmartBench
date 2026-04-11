from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from SmartBench.experiments.common.paths import run_python


HERE = Path(__file__).resolve().parent
ARTIFACTS = HERE / "artifacts"


def main() -> int:
    ap = argparse.ArgumentParser(description="Run model-size evaluation on public SmartBench subsets.")
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--api-base-url", default="")
    ap.add_argument("--max-workers", type=int, default=2)
    ap.add_argument("--single-shot", action="store_true")
    ap.add_argument("--omit-description", action="store_true")
    args = ap.parse_args()

    public_views = ARTIFACTS / "public_views"
    selection = ARTIFACTS / "selection"

    run_python(
        "scripts/run_official_eval.py",
        "--benchmark", str(public_views / "ab175_public_flat.json"),
        "--sample-ids-file", str(selection / "ab175_sample100_ids.json"),
        "--system-prompt-file", str(Path("SmartBench/prompts/context-independent_prompt.txt")),
        "--output-dir", str(ARTIFACTS / "runs" / "partA"),
        "--max-workers", str(args.max_workers),
        "--models", *args.models,
        *(["--api-base-url", str(args.api_base_url)] if args.api_base_url else []),
    )

    cmd = [
        "--benchmark", str(public_views / "tdcs_public_flat.json"),
        "--ground-truth", str(public_views / "tdcs_public_ground_truth.json"),
        "--sample-ids-file", str(selection / "tdcs_sample100_ids.json"),
        "--system-prompt-file", str(Path("SmartBench/prompts/context-dependent_prompt.txt")),
        "--output-dir", str(ARTIFACTS / "runs" / "partB_tdcs"),
        "--max-workers", str(args.max_workers),
        "--max-tokens", "8000",
        "--models", *args.models,
    ]
    if args.api_base_url:
        cmd.extend(["--api-base-url", str(args.api_base_url)])
    if args.single_shot:
        cmd.append("--single-shot")
    if args.omit_description:
        cmd.append("--omit-description")

    run_python("scripts/run_official_eval_context_dependent.py", *cmd)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

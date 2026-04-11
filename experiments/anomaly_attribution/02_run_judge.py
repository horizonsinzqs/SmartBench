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
    ap = argparse.ArgumentParser(description="Run anomaly-attribution judge on public SmartBench selections.")
    ap.add_argument("--candidate-models", nargs="+", required=True)
    ap.add_argument("--judge-model", default="gpt-5-mini")
    ap.add_argument("--api-base-url", default="")
    ap.add_argument("--max-items", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    public_views = ARTIFACTS / "public_views"
    run_dir = ARTIFACTS / "judge_runs"

    cmd = [
        "--ab175-benchmark", str(public_views / "ab175_public_flat.json"),
        "--ab175-ids", str(ARTIFACTS / "selection" / "ab175_anomaly100_ids.json"),
        "--tdcs-gt", str(public_views / "tdcs_public_ground_truth.json"),
        "--tdcs-ids", str(ARTIFACTS / "selection" / "tdcs_anomaly100_ids.json"),
        "--judge-model", str(args.judge_model),
        "--out-dir", str(run_dir),
        "--candidate-models", *args.candidate_models,
    ]
    if args.api_base_url:
        cmd.extend(["--api-base-url", str(args.api_base_url)])
    if args.max_items > 0:
        cmd.extend(["--max-items", str(args.max_items)])
    if args.dry_run:
        cmd.append("--dry-run")

    run_python("scripts/run_task3_gpt5mini_judge.py", *cmd)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

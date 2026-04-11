from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from SmartBench.experiments.common.paths import run_powershell


def main() -> int:
    ap = argparse.ArgumentParser(description="Run fusion evaluation.")
    ap.add_argument("--profile", default="full")
    ap.add_argument("--task", default="both")
    ap.add_argument("--models", nargs="+", required=True)
    args = ap.parse_args()

    run_powershell(
        "rebuttal/fusion_dual_anomaly/02_run_eval.ps1",
        "-Profile", str(args.profile),
        "-Task", str(args.task),
        "-ModelPreset", "custom",
        "-Models", *args.models,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from SmartBench.experiments.common.paths import run_python


def main() -> int:
    ap = argparse.ArgumentParser(description="Build fusion benchmarks.")
    ap.add_argument("--profile", default="full")
    args = ap.parse_args()

    run_python("rebuttal/fusion_dual_anomaly/01_build_fusion_benchmarks.py", "--profile", str(args.profile))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


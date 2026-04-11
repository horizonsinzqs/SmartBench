from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from SmartBench.experiments.common.paths import run_powershell


def main() -> int:
    ap = argparse.ArgumentParser(description="Run compression evaluation.")
    ap.add_argument("--set-name", default="github600_true_compressed_226")
    ap.add_argument("--variant", default="all")
    ap.add_argument("--models", nargs="+", required=True)
    args = ap.parse_args()

    run_powershell(
        "rebuttal/compression_public_prompt/03_run_eval.ps1",
        "-SetName", str(args.set_name),
        "-Variant", str(args.variant),
        "-ModelPreset", "custom",
        "-Models", *args.models,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from SmartBench.experiments.common.paths import run_python


def main() -> int:
    ap = argparse.ArgumentParser(description="Build RAW/RBE compression benchmarks.")
    ap.add_argument("--windowed-output-name", default="raw_128k.json")
    ap.add_argument("--windowed-user-tokens", type=int, default=128000)
    args = ap.parse_args()

    run_python(
        "rebuttal/compression_public_prompt/02_build_benchmarks.py",
        "--windowed-output-name", str(args.windowed_output_name),
        "--windowed-user-tokens", str(args.windowed_user_tokens),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

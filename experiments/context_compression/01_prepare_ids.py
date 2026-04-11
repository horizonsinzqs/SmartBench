from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from SmartBench.experiments.common.paths import run_python


def main() -> int:
    run_python("rebuttal/compression_public_prompt/01_prepare_ids.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

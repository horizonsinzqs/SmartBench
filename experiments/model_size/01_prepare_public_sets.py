from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from SmartBench.experiments.common.public_benchmark import (
    build_public_views,
    cf_group_key,
    cd_group_key,
    load_context_independent,
    load_tdcs,
    normalize_label,
    round_robin_sample,
    sample_id,
    write_json,
)


HERE = Path(__file__).resolve().parent
ARTIFACTS = HERE / "artifacts"


def _balanced(samples, total: int, key_fn, seed: int):
    half = total // 2
    normals = [s for s in samples if normalize_label(s.get("label")) == "normal"]
    anomalies = [s for s in samples if normalize_label(s.get("label")) == "anomaly"]
    picked = round_robin_sample(normals, total=half, key_fn=lambda _: "normal", seed=seed)
    picked += round_robin_sample(anomalies, total=half, key_fn=key_fn, seed=seed)
    return picked


def main() -> int:
    views = build_public_views(ARTIFACTS / "public_views")
    cf_pick = _balanced(load_context_independent(), total=100, key_fn=cf_group_key, seed=42)
    tdcs_pick = _balanced(load_tdcs(), total=100, key_fn=cd_group_key, seed=42)

    write_json(ARTIFACTS / "selection" / "ab175_sample100_ids.json", [sample_id(s) for s in cf_pick])
    write_json(ARTIFACTS / "selection" / "tdcs_sample100_ids.json", [sample_id(s) for s in tdcs_pick])
    write_json(ARTIFACTS / "selection" / "public_views.json", {k: str(v) for k, v in views.items()})
    print(f"Wrote selection files under: {ARTIFACTS / 'selection'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

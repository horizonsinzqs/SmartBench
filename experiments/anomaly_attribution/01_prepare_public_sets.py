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


def main() -> int:
    views = build_public_views(ARTIFACTS / "public_views")

    cf_anomalies = [s for s in load_context_independent() if normalize_label(s.get("label")) == "anomaly"]
    tdcs_anomalies = [s for s in load_tdcs() if normalize_label(s.get("label")) == "anomaly"]

    cf_pick = round_robin_sample(cf_anomalies, total=100, key_fn=cf_group_key, seed=42)
    tdcs_pick = round_robin_sample(tdcs_anomalies, total=100, key_fn=cd_group_key, seed=42)

    write_json(ARTIFACTS / "selection" / "ab175_anomaly100_ids.json", [sample_id(s) for s in cf_pick])
    write_json(ARTIFACTS / "selection" / "tdcs_anomaly100_ids.json", [sample_id(s) for s in tdcs_pick])
    write_json(ARTIFACTS / "selection" / "public_views.json", {k: str(v) for k, v in views.items()})
    print(f"Wrote selection files under: {ARTIFACTS / 'selection'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable, Dict, List, Sequence

from .paths import REPO_ROOT, SMARTBENCH_ROOT


CF_ROOT = SMARTBENCH_ROOT / "context-independent"
TDCS_ROOT = SMARTBENCH_ROOT / "context-dependent" / "tdcs_rbe"
ARGUS_ROOT = SMARTBENCH_ROOT / "context-dependent" / "argus_prime"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def sample_id(sample: Dict[str, Any]) -> str:
    for key in ("id", "eval_id", "sample_id"):
        value = str(sample.get(key) or "").strip()
        if value:
            return value
    return ""


def normalize_label(value: Any) -> str:
    return str(value or "").strip().lower()


def _walk_samples(root: Path, source_name: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for path in sorted(root.rglob("*.json")):
        sample = load_json(path)
        sid = sample_id(sample)
        if not sid:
            raise ValueError(f"Missing sample id in {path}")
        copied = dict(sample)
        copied["_source"] = source_name
        copied["_source_file"] = path.relative_to(REPO_ROOT).as_posix()
        out.append(copied)
    return out


def load_context_independent() -> List[Dict[str, Any]]:
    return _walk_samples(CF_ROOT, "ab175")


def load_tdcs() -> List[Dict[str, Any]]:
    return _walk_samples(TDCS_ROOT, "tdcs_rbe")


def load_argus() -> List[Dict[str, Any]]:
    return _walk_samples(ARGUS_ROOT, "argus_prime")


def cf_group_key(sample: Dict[str, Any]) -> str:
    info = sample.get("anomaly_info") if isinstance(sample.get("anomaly_info"), dict) else {}
    return str(info.get("anomaly_subtype") or info.get("anomaly_type") or "normal")


def cd_group_key(sample: Dict[str, Any]) -> str:
    details = sample.get("anomaly_details")
    if isinstance(details, list) and details:
        first = details[0]
        if isinstance(first, dict):
            return str(first.get("type") or sample.get("_source") or "normal")
    anomaly_types = sample.get("anomaly_types")
    if isinstance(anomaly_types, list) and anomaly_types:
        return str(anomaly_types[0])
    return str(sample.get("_source") or "normal")


def round_robin_sample(
    samples: Sequence[Dict[str, Any]],
    total: int,
    key_fn: Callable[[Dict[str, Any]], str],
    seed: int,
) -> List[Dict[str, Any]]:
    rng = random.Random(int(seed))
    buckets: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for sample in samples:
        buckets[str(key_fn(sample))].append(sample)
    ordered = []
    for key, items in buckets.items():
        xs = list(items)
        rng.shuffle(xs)
        ordered.append((key, xs))
    rng.shuffle(ordered)

    out: List[Dict[str, Any]] = []
    while len(out) < int(total):
        progressed = False
        for _, items in ordered:
            if not items:
                continue
            out.append(items.pop())
            progressed = True
            if len(out) >= int(total):
                break
        if not progressed:
            break
    if len(out) != int(total):
        raise ValueError(f"Could not sample enough items: {len(out)} < {total}")
    return out


def build_public_views(out_dir: Path) -> Dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)

    cf_samples = sorted(load_context_independent(), key=sample_id)
    tdcs_samples = sorted(load_tdcs(), key=sample_id)
    argus_samples = sorted(load_argus(), key=sample_id)

    cf_path = write_json(out_dir / "ab175_public_flat.json", {"samples": cf_samples})
    tdcs_bench_path = write_json(out_dir / "tdcs_public_flat.json", {"samples": tdcs_samples})
    argus_bench_path = write_json(out_dir / "argus_public_flat.json", {"samples": argus_samples})

    tdcs_gt_entries = []
    for sample in tdcs_samples:
        tdcs_gt_entries.append(
            {
                "eval_id": sample_id(sample),
                "id": sample_id(sample),
                "label": sample.get("label"),
                "reasoning": sample.get("reasoning"),
                "evidence_devices": sample.get("evidence_devices") or [],
                "anomaly_types": sample.get("anomaly_types") or [],
                "anomaly_details": sample.get("anomaly_details") or [],
                "pair_id": sample.get("pair_id"),
                "paired_id": sample.get("paired_id"),
            }
        )
    tdcs_gt_path = write_json(out_dir / "tdcs_public_ground_truth.json", {"entries": tdcs_gt_entries})

    return {
        "ab175": cf_path,
        "tdcs": tdcs_bench_path,
        "argus": argus_bench_path,
        "tdcs_gt": tdcs_gt_path,
    }


from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Iterable


EXPERIMENTS_ROOT = Path(__file__).resolve().parents[1]
SMARTBENCH_ROOT = EXPERIMENTS_ROOT.parent
REPO_ROOT = SMARTBENCH_ROOT.parent


def python_exe() -> str:
    return sys.executable


def run_python(script: str | Path, *args: str, cwd: Path | None = None) -> None:
    script_path = Path(script)
    if not script_path.is_absolute():
        script_path = (REPO_ROOT / script_path).resolve()
    cmd = [python_exe(), str(script_path), *[str(x) for x in args]]
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=str(cwd or REPO_ROOT), check=True)


def run_powershell(script: str | Path, *args: str, cwd: Path | None = None) -> None:
    script_path = Path(script)
    if not script_path.is_absolute():
        script_path = (REPO_ROOT / script_path).resolve()
    cmd = [
        "powershell",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script_path),
        *[str(x) for x in args],
    ]
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=str(cwd or REPO_ROOT), check=True)


def ensure_dir(path: str | Path) -> Path:
    out = Path(path)
    if not out.is_absolute():
        out = (REPO_ROOT / out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    return out


def repo_rel(path: str | Path) -> str:
    p = Path(path)
    if not p.is_absolute():
        p = (REPO_ROOT / p).resolve()
    return p.relative_to(REPO_ROOT).as_posix()

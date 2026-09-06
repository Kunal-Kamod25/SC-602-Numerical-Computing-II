from __future__ import annotations

from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def input_dir(assignment_name: str) -> Path:
    return project_root() / "inputs" / assignment_name


def output_dir(assignment_name: str) -> Path:
    path = project_root() / "outputs" / assignment_name
    path.mkdir(parents=True, exist_ok=True)
    return path

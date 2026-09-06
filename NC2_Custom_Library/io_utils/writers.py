from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, Sequence


def write_csv(file_path: Path, headers: Sequence[str], rows: Iterable[Sequence]) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)


def write_text_report(file_path: Path, lines: Sequence[str]) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

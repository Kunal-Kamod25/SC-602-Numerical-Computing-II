from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import List, Tuple

from core.exceptions import DataFileError


def _safe_float(value: str) -> float:
    return float(str(value).strip())


def load_step_sizes(file_path: Path) -> List[float]:
    if not file_path.exists():
        raise DataFileError(f"Step size file not found: {file_path}")
    values: List[float] = []
    for line in file_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped:
            values.append(_safe_float(stripped))
    if not values:
        raise DataFileError(f"No step sizes found in file: {file_path}")
    return values


def _parse_pair_line(line: str) -> Tuple[float, float]:
    parts = re.split(r"[\s,]+", line.strip())
    if len(parts) < 2:
        raise ValueError(f"Invalid pair line: {line!r}")
    return _safe_float(parts[0]), _safe_float(parts[1])


def load_points_from_text(file_path: str) -> Tuple[List[float], List[float], List[float]]:
    path = Path(file_path)
    if not path.exists():
        raise DataFileError(f"File not found: {file_path}")

    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise DataFileError(f"No data found in: {file_path}")

    x_values: List[float] = []
    y_values: List[float] = []
    query_values: List[float] = []

    start_index = 0
    pair_count = None
    try:
        pair_count = int(float(lines[0]))
        start_index = 1
    except ValueError:
        pair_count = None

    if pair_count is not None:
        if len(lines) < start_index + pair_count:
            raise DataFileError(f"Expected {pair_count} pairs but file is shorter: {file_path}")
        for i in range(pair_count):
            x, y = _parse_pair_line(lines[start_index + i])
            x_values.append(x)
            y_values.append(y)
        for line in lines[start_index + pair_count:]:
            query_values.append(_safe_float(line))
        return x_values, y_values, query_values

    for line in lines:
        try:
            x, y = _parse_pair_line(line)
            x_values.append(x)
            y_values.append(y)
        except ValueError:
            query_values.append(_safe_float(line))

    if not x_values:
        raise DataFileError(f"No x/y pairs found in: {file_path}")
    return x_values, y_values, query_values


def load_points_from_csv(file_path: str, x_column: str = "x", y_column: str = "y") -> Tuple[List[float], List[float], List[float]]:
    path = Path(file_path)
    if not path.exists():
        raise DataFileError(f"File not found: {file_path}")

    with open(path, "r", encoding="utf-8", newline="") as handle:
        rows = [row for row in csv.reader(handle) if any(cell.strip() for cell in row)]
    if not rows:
        raise DataFileError(f"No data found in: {file_path}")

    query_values: List[float] = []
    x_values: List[float] = []
    y_values: List[float] = []
    header = [cell.strip().lower() for cell in rows[0]]

    if x_column.lower() in header and y_column.lower() in header:
        x_idx = header.index(x_column.lower())
        y_idx = header.index(y_column.lower())
        data_rows = rows[1:]
    else:
        x_idx, y_idx = 0, 1
        data_rows = rows

    for row in data_rows:
        if len(row) == 1:
            query_values.append(_safe_float(row[0]))
            continue
        if len(row) <= max(x_idx, y_idx):
            continue
        x_values.append(_safe_float(row[x_idx]))
        y_values.append(_safe_float(row[y_idx]))

    if not x_values:
        raise DataFileError(f"No x/y pairs found in: {file_path}")
    return x_values, y_values, query_values


def load_points_from_file(file_path: str, x_column: str = "x", y_column: str = "y") -> Tuple[List[float], List[float], List[float]]:
    path = Path(file_path)
    if path.suffix.lower() == ".csv":
        return load_points_from_csv(file_path, x_column=x_column, y_column=y_column)
    return load_points_from_text(file_path)


def load_config_n_values(file_path: Path) -> List[int]:
    if not file_path.exists():
        raise DataFileError(f"Config file not found: {file_path}")
    n_values: List[int] = []
    with open(file_path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if "n" in row and row["n"].strip():
                n_values.append(int(float(row["n"])))
    if not n_values:
        raise DataFileError(f"No 'n' values found in: {file_path}")
    return n_values

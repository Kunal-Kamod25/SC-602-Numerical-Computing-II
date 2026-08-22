"""
data_loader.py
---------------
Handles getting (x, y) data into the program.

This project needs to work with both:
- small handwritten datasets used in Assignment 4
- larger files used later, either as CSV or simple text input

The generic load_points_from_file() function detects the file type and
returns the data points plus any evaluation points found in the file.
"""

import csv
import re
from pathlib import Path
from typing import List, Sequence, Tuple

from .exceptions import DataFileError


def load_points_from_lists(x_values: List[float], y_values: List[float]) -> Tuple[List[float], List[float]]:
    """Wrap plain lists as (x, y) values."""
    return list(x_values), list(y_values)


def _safe_float(value: str) -> float:
    return float(str(value).strip())


def _parse_pair_line(line: str) -> Tuple[float, float]:
    cleaned = line.strip()
    if not cleaned:
        raise ValueError("empty line")

    candidate = re.split(r"[\s,]+", cleaned)
    if len(candidate) < 2:
        raise ValueError(f"Not a valid pair: {line!r}")

    return _safe_float(candidate[0]), _safe_float(candidate[1])


def load_points_from_text(file_path: str) -> Tuple[List[float], List[float], List[float]]:
    """Read a text file containing point pairs and optional evaluation points.

    Accepted format:
        n
        x0 y0
        x1 y1
        ...
        xq
        xq2

    The first line may optionally contain the number of data points. Any
    remaining numeric values that are not part of a pair are treated as
    query/evaluation points.
    """
    path = Path(file_path)
    if not path.exists():
        raise DataFileError(f"Could not find the file: {file_path}")

    try:
        with open(path, mode="r", encoding="utf-8") as f:
            raw_lines = [line.strip() for line in f if line.strip()]
    except OSError as e:
        raise DataFileError(f"Could not open file '{file_path}': {e}")

    if not raw_lines:
        raise DataFileError(f"No usable rows found in '{file_path}'.")

    x_values: List[float] = []
    y_values: List[float] = []
    query_points: List[float] = []

    try:
        first_value = float(raw_lines[0])
        count = int(first_value)
        lines_after_header = raw_lines[1:]
    except ValueError:
        count = None
        lines_after_header = raw_lines

    if count is not None:
        data_lines = []
        remaining_lines = []

        for line in lines_after_header:
            if len(data_lines) < count:
                try:
                    x_val, y_val = _parse_pair_line(line)
                    data_lines.append(line)
                    x_values.append(x_val)
                    y_values.append(y_val)
                except ValueError:
                    try:
                        query_points.append(float(line))
                    except ValueError as exc:
                        raise DataFileError(f"Could not parse data row '{line}' in '{file_path}': {exc}")
            else:
                remaining_lines.append(line)
    else:
        data_lines = []
        remaining_lines = lines_after_header

    for line in remaining_lines:
        try:
            query_points.append(float(line))
        except ValueError:
            try:
                x_val, y_val = _parse_pair_line(line)
                x_values.append(x_val)
                y_values.append(y_val)
            except ValueError as exc:
                raise DataFileError(f"Could not parse query row '{line}' in '{file_path}': {exc}")

    if not x_values:
        # flexible fallback: if the file contains only pairs without a count,
        # parse every pair in order and treat the last value of each pair as y.
        for line in raw_lines:
            try:
                x_val, y_val = _parse_pair_line(line)
                x_values.append(x_val)
                y_values.append(y_val)
            except ValueError:
                try:
                    query_points.append(float(line))
                except ValueError:
                    pass

    if not x_values:
        raise DataFileError(f"No usable x/y data found in '{file_path}'.")

    return x_values, y_values, query_points


def load_points_from_csv(
    file_path: str,
    x_column: str = "x",
    y_column: str = "y",
) -> Tuple[List[float], List[float], List[float]]:
    """Read (x, y) points out of a CSV file.

    The function supports an optional trailing set of evaluation points:
    a single numeric value in a row is treated as a query point.
    """
    path = Path(file_path)
    if not path.exists():
        raise DataFileError(f"Could not find the file: {file_path}")

    try:
        with open(path, mode="r", newline="", encoding="utf-8") as f:
            rows = [row for row in csv.reader(f) if any(cell.strip() for cell in row)]
    except OSError as e:
        raise DataFileError(f"Could not open file '{file_path}': {e}")

    if not rows:
        raise DataFileError(f"No usable rows found in '{file_path}'.")

    x_values: List[float] = []
    y_values: List[float] = []
    query_points: List[float] = []

    header = [cell.strip() for cell in rows[0]]
    if header and any(cell.lower() == x_column.lower() for cell in header) and any(cell.lower() == y_column.lower() for cell in header):
        x_index = next(i for i, cell in enumerate(header) if cell.lower() == x_column.lower())
        y_index = next(i for i, cell in enumerate(header) if cell.lower() == y_column.lower())
        data_rows = rows[1:]
    else:
        x_index = 0
        y_index = 1
        data_rows = rows

    for row_number, row in enumerate(data_rows, start=2):
        if len(row) <= max(x_index, y_index):
            if len(row) == 1:
                try:
                    query_points.append(float(row[0]))
                except ValueError:
                    pass
            continue

        try:
            x_values.append(float(row[x_index]))
            y_values.append(float(row[y_index]))
        except ValueError:
            if len(row) == 1:
                try:
                    query_points.append(float(row[0]))
                except ValueError:
                    raise DataFileError(
                        f"Row {row_number} has a non-numeric value and was skipped: {row}"
                    )
            else:
                raise DataFileError(
                    f"Row {row_number} has a non-numeric value and was skipped: {row}"
                )

    if not x_values:
        raise DataFileError(f"No usable x/y data found in '{file_path}'.")

    return x_values, y_values, query_points


def load_points_from_file(file_path: str, x_column: str = "x", y_column: str = "y") -> Tuple[List[float], List[float], List[float]]:
    """Auto-detect the file type and load x/y data plus query points.

    Supports .txt and .csv inputs and keeps the interface the same for both
    small and larger datasets.
    """
    path = Path(file_path)
    if not path.exists():
        raise DataFileError(f"Could not find the file: {file_path}")

    suffix = path.suffix.lower()
    if suffix == ".csv":
        return load_points_from_csv(str(path), x_column=x_column, y_column=y_column)
    return load_points_from_text(str(path))

"""
data_loader.py

Handles getting (x, y) data into the program robustly, mimicking
the assignment 4 implementation. Throws DataFileError on failure.
"""

import csv
import re
from pathlib import Path
from typing import List, Tuple

from .exceptions import DataFileError

def _safe_float(value: str) -> float:
    return float(str(value).strip())

def load_points_from_file(file_path: str, x_column: str = "x", y_column: str = "y") -> Tuple[List[float], List[float]]:
    """Reads a CSV file containing point pairs.
    
    If anything goes wrong (missing file, bad parsing), throws DataFileError.
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

    x_values = []
    y_values = []

    header = [cell.strip().lower() for cell in rows[0]]
    if x_column.lower() in header and y_column.lower() in header:
        x_index = header.index(x_column.lower())
        y_index = header.index(y_column.lower())
        data_rows = rows[1:]
    else:
        x_index = 0
        y_index = 1
        data_rows = rows

    for row_number, row in enumerate(data_rows, start=2):
        if len(row) <= max(x_index, y_index):
            continue
        try:
            x_values.append(float(row[x_index]))
            y_values.append(float(row[y_index]))
        except ValueError:
            raise DataFileError(f"Row {row_number} has a non-numeric value: {row}")

    if not x_values:
        raise DataFileError(f"No usable x/y data found in '{file_path}'.")

    return x_values, y_values

"""
utils.py

Helper methods for plotting and saving files.
"""

import os
import csv
import matplotlib.pyplot as plt

def ensure_outputs_dir(subfolder: str) -> str:
    path = f"outputs/{subfolder}"
    os.makedirs(path, exist_ok=True)
    return path

def write_table_csv(filepath: str, headers: list, rows: list):
    """Writes tabular data to a CSV file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

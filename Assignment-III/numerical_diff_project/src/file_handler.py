"""
file_handler.py
----------------
Encapsulates all file I/O for the project (CSV results, text report,
directory management) so that no other module needs to touch the
filesystem directly.  This keeps disk access in one well-tested place
(single-responsibility principle).
"""

import csv
import os
from typing import List
from .analysis import ResultRecord


class FileHandler:
    """Handles reading and writing of project output files."""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        self.results_dir = os.path.join(output_dir, "results")
        self.plots_dir = os.path.join(output_dir, "plots")
        self._ensure_dirs()

    def _ensure_dirs(self) -> None:
        for d in (self.output_dir, self.results_dir, self.plots_dir):
            os.makedirs(d, exist_ok=True)

    # ------------------------------------------------------------------ #
    # CSV handling
    # ------------------------------------------------------------------ #
    def save_results_csv(self, results: List[ResultRecord], filename: str = "results.csv") -> str:
        """Write all ResultRecord rows to a single CSV file. Returns path."""
        path = os.path.join(self.results_dir, filename)
        fieldnames = ["function_name", "x", "h", "D_h", "R_h", "exact", "error_D", "error_R"]
        with open(path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in results:
                writer.writerow(r.as_dict())
        return path

    def load_results_csv(self, filename: str = "results.csv") -> List[dict]:
        """Read back a results CSV as a list of dicts (utility for re-analysis)."""
        path = os.path.join(self.results_dir, filename)
        rows = []
        with open(path, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        return rows

    def save_slopes_csv(self, slopes_by_function: dict, filename: str = "convergence_slopes.csv") -> str:
        """Save the observed log-log slopes per function to CSV."""
        path = os.path.join(self.results_dir, filename)
        with open(path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "function_name",
                "slope_D_truncation_region", "slope_R_truncation_region",
                "theoretical_D", "theoretical_R",
                "slope_D_full_range", "slope_R_full_range",
            ])
            for name, slopes in slopes_by_function.items():
                writer.writerow([
                    name,
                    f"{slopes['slope_D']:.4f}", f"{slopes['slope_R']:.4f}",
                    2, 4,
                    f"{slopes['slope_D_full']:.4f}", f"{slopes['slope_R_full']:.4f}",
                ])
        return path

    # ------------------------------------------------------------------ #
    # Text report handling
    # ------------------------------------------------------------------ #
    def save_text_report(self, text: str, filename: str = "report.txt") -> str:
        path = os.path.join(self.output_dir, filename)
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(text)
        return path

    def plot_path(self, filename: str) -> str:
        """Return the full path for a plot file inside the plots directory."""
        return os.path.join(self.plots_dir, filename)

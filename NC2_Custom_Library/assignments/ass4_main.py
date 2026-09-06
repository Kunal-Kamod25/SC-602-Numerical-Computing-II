from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt
import numpy as np

from core import LagrangeInterpolator
from io_utils import input_dir, output_dir, load_points_from_text, write_csv, write_text_report


def run_assignment_4() -> None:
    print("\n[ASS4] Running Lagrange interpolation question set...")
    in_dir = input_dir("ass4")
    out_dir = output_dir("ass4")

    for file_path in sorted(in_dir.glob("q*.txt")):
        x_vals, y_vals, query_points = load_points_from_text(str(file_path))
        model = LagrangeInterpolator(x_vals, y_vals)

        rows = []
        for qx in query_points:
            qy = model.evaluate(qx)
            rows.append([qx, qy])

        if not rows:
            rows = [["no query point", "n/a"]]

        write_csv(out_dir / f"{file_path.stem}_estimates.csv", ["x_query", "y_estimate"], rows)

        x_arr = np.asarray(x_vals, dtype=float)
        y_arr = np.asarray(y_vals, dtype=float)
        x_grid = np.linspace(float(np.min(x_arr)), float(np.max(x_arr)), 250)
        y_grid = model.evaluate(x_grid)

        plt.figure(figsize=(7, 4))
        plt.plot(x_grid, y_grid, "b-", label="Lagrange polynomial")
        plt.plot(x_arr, y_arr, "ro", label="data points")
        if query_points:
            yq = model.evaluate(query_points)
            plt.plot(query_points, yq, "g*", markersize=11, label="query point(s)")
        plt.title(f"ASS4 - {file_path.stem}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(out_dir / f"{file_path.stem}_plot.png", dpi=140)
        plt.close()

    write_text_report(
        out_dir / "report.txt",
        [
            "Assignment IV Summary",
            "All q1..q5 text files were processed using LagrangeInterpolator.",
            "Outputs: per-file CSV estimates and interpolation plots.",
        ],
    )


if __name__ == "__main__":
    run_assignment_4()

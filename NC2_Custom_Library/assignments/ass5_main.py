from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt
import numpy as np

from core import LagrangeInterpolator
from io_utils import input_dir, output_dir, load_points_from_csv, write_csv, write_text_report


def run_assignment_5() -> None:
    print("\n[ASS5] Running big-dataset interpolation (150-point student dataset)...")
    out_dir = output_dir("ass5")
    data_file = input_dir("ass5") / "student_academic_stress_interpolation_150.csv"
    x_vals, y_vals, _ = load_points_from_csv(
        str(data_file),
        x_column="Study_Hours",
        y_column="Academic_Stress_Score",
    )

    pairs = sorted(zip(x_vals, y_vals))
    x_sorted = np.array([p[0] for p in pairs], dtype=float)
    y_sorted = np.array([p[1] for p in pairs], dtype=float)

    sizes = [5, 20, 50, 100, 150]
    rows = []
    x_grid = np.linspace(float(np.min(x_sorted)), float(np.max(x_sorted)), 500)

    fig, axs = plt.subplots(2, 3, figsize=(13, 7))
    axs = axs.flatten()
    for idx, n in enumerate(sizes):
        indices = np.linspace(0, len(x_sorted) - 1, n).round().astype(int)
        x_sub = x_sorted[indices]
        y_sub = y_sorted[indices]
        model = LagrangeInterpolator(x_sub, y_sub)
        y_hat_grid = model.evaluate(x_grid)
        y_hat_train = model.evaluate(x_sub)
        max_train_error = float(np.max(np.abs(y_sub - y_hat_train)))
        rows.append([n, max_train_error])

        ax = axs[idx]
        ax.scatter(x_sorted, y_sorted, s=7, alpha=0.45, color="gray", label="full dataset")
        ax.plot(x_grid, y_hat_grid, "r-", linewidth=1.2, label=f"Lagrange N={n}")
        ax.set_title(f"N={n}")
        ax.grid(True, alpha=0.2)
        if idx == 0:
            ax.legend(fontsize=8)

    axs[-1].axis("off")
    fig.suptitle("ASS5: Barycentric Lagrange progression on 150-point dataset", fontsize=12)
    fig.tight_layout()
    fig.savefig(out_dir / "assignment5_progression.png", dpi=145)
    plt.close(fig)

    write_csv(out_dir / "subset_fit_summary.csv", ["subset_size", "max_training_error"], rows)
    write_text_report(
        out_dir / "report.txt",
        [
            "Assignment V Summary",
            "Used the provided 150-point dataset.",
            "Generated progression plots for N = 5, 20, 50, 100, 150.",
            "Barycentric Lagrange is used for better numerical stability on larger data.",
        ],
    )


if __name__ == "__main__":
    run_assignment_5()

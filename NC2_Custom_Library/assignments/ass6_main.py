from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt
import numpy as np

from core import CentralDifference, LagrangeInterpolator, NewtonInterpolator
from io_utils import input_dir, output_dir, load_config_n_values, load_points_from_csv, write_csv, write_text_report


def _run_q1_to_q4(out_dir):
    for name in ["q1_data.csv", "q2_data.csv", "q3_data.csv", "q4_data.csv"]:
        x, y, _ = load_points_from_csv(str(input_dir("ass6") / name))
        n_model = NewtonInterpolator(x, y)
        l_model = LagrangeInterpolator(x, y)

        x_grid = np.linspace(min(x), max(x), 260)
        n_vals = n_model.evaluate(x_grid)
        l_vals = l_model.evaluate(x_grid)
        diff = np.abs(n_vals - l_vals)

        write_csv(
            out_dir / f"{name.replace('.csv', '')}_comparison.csv",
            ["x", "newton", "lagrange", "abs_diff"],
            [[xg, nv, lv, dv] for xg, nv, lv, dv in zip(x_grid, n_vals, l_vals, diff)],
        )

        plt.figure(figsize=(7, 4))
        plt.plot(x_grid, n_vals, "b--", label="Newton")
        plt.plot(x_grid, l_vals, "r:", label="Lagrange")
        plt.scatter(x, y, c="black", s=25, label="data points")
        plt.title(f"ASS6 {name}: Newton vs Lagrange")
        plt.grid(True, alpha=0.25)
        plt.legend()
        plt.tight_layout()
        plt.savefig(out_dir / f"{name.replace('.csv', '')}_plot.png", dpi=140)
        plt.close()


def _run_q5_runge(out_dir):
    n_values = load_config_n_values(input_dir("ass6") / "q5_config.csv")
    x_grid = np.linspace(-1, 1, 450)
    exact = 1.0 / (1.0 + 25.0 * x_grid**2)
    rows = []
    for n in n_values:
        x_nodes = np.linspace(-1, 1, n + 1)
        y_nodes = 1.0 / (1.0 + 25.0 * x_nodes**2)
        n_model = NewtonInterpolator(x_nodes, y_nodes)
        approx = n_model.evaluate(x_grid)
        max_err = float(np.max(np.abs(exact - approx)))
        rows.append([n, n + 1, max_err])
    write_csv(out_dir / "q5_runge_max_error.csv", ["degree_n", "points", "max_error"], rows)


def _run_q6_derivative_comparison(out_dir):
    x, y, _ = load_points_from_csv(str(input_dir("ass6") / "q6_data.csv"))
    newton = NewtonInterpolator(x, y)
    lagrange = LagrangeInterpolator(x, y)
    central = CentralDifference()
    eval_points = [0.4, 0.8, 1.2]

    rows = []
    for xv in eval_points:
        dn = newton.derivative(xv)
        dl = lagrange.derivative(xv)
        dc = central.derivative(math.sin, xv, 1e-3)
        exact = math.cos(xv)
        rows.append([xv, dn, dl, dc, exact, abs(exact - dn), abs(exact - dl), abs(exact - dc)])

    write_csv(
        out_dir / "q6_three_method_comparison.csv",
        [
            "x",
            "newton_derivative",
            "lagrange_derivative",
            "central_difference",
            "exact_cos_x",
            "err_newton",
            "err_lagrange",
            "err_central",
        ],
        rows,
    )


def run_assignment_6() -> None:
    print("\n[ASS6] Running Newton interpolation package tasks...")
    out_dir = output_dir("ass6")
    _run_q1_to_q4(out_dir)
    _run_q5_runge(out_dir)
    _run_q6_derivative_comparison(out_dir)
    write_text_report(
        out_dir / "report.txt",
        [
            "Assignment VI Summary",
            "Implemented Newton + Lagrange interpolation comparisons.",
            "Included Runge error growth table and derivative method comparison.",
        ],
    )


if __name__ == "__main__":
    run_assignment_6()

from __future__ import annotations

import sys
from pathlib import Path

# Student note: this makes standalone execution work from assignment file too.
sys.path.append(str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt
import numpy as np

from core import BackwardDifference, CentralDifference, ForwardDifference, get_default_test_functions
from io_utils import input_dir, output_dir, load_step_sizes, write_csv, write_text_report


def run_assignment_2() -> None:
    print("\n[ASS2] Running finite-difference comparison...")
    h_values = load_step_sizes(input_dir("ass2") / "h_values.txt")
    methods = [ForwardDifference(), BackwardDifference(), CentralDifference()]
    x_eval = 1.0
    rows = []

    for test_fn in get_default_test_functions():
        exact = test_fn.exact_derivative(x_eval)
        for h in h_values:
            for method in methods:
                approx = method.derivative(test_fn.evaluate, x_eval, h)
                err = abs(exact - approx)
                rows.append([test_fn.name, method.name, h, approx, exact, err])

    out_dir = output_dir("ass2")
    write_csv(
        out_dir / "method_comparison.csv",
        ["function", "method", "h", "approx_derivative", "exact_derivative", "abs_error"],
        rows,
    )

    report_lines = [
        "Assignment II Summary",
        "We compared Forward, Backward, and Central difference methods.",
        "Central difference should usually have the lowest truncation error (O(h^2)).",
        f"Total rows saved: {len(rows)}",
    ]
    write_text_report(out_dir / "report.txt", report_lines)

    # Student-style quick plot for one representative function.
    exp_rows = [r for r in rows if r[0] == "f(x)=e^x"]
    plt.figure(figsize=(7, 4))
    for method_name in ["Forward Difference", "Backward Difference", "Central Difference"]:
        xs = [r[2] for r in exp_rows if r[1] == method_name]
        ys = [r[5] for r in exp_rows if r[1] == method_name]
        plt.loglog(xs, ys, marker="o", label=method_name)
    plt.title("ASS2 Error vs h for f(x)=e^x at x=1")
    plt.xlabel("h")
    plt.ylabel("absolute error")
    plt.grid(True, which="both")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "error_plot_exp.png", dpi=140)
    plt.close()


if __name__ == "__main__":
    run_assignment_2()

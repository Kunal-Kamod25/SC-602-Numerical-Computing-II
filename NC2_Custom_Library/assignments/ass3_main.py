from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt

from core import CentralDifference, RichardsonExtrapolation, get_default_test_functions
from core.metrics import loglog_slope
from io_utils import output_dir, write_csv, write_text_report


def run_assignment_3() -> None:
    print("\n[ASS3] Running Richardson extrapolation study...")
    out_dir = output_dir("ass3")
    h_values = [10 ** (-k) for k in range(1, 13)]
    x_eval = 1.0
    central = CentralDifference()
    richardson = RichardsonExtrapolation()
    rows = []
    slope_rows = []

    for test_fn in get_default_test_functions():
        err_c = []
        err_r = []
        for h in h_values:
            exact = test_fn.exact_derivative(x_eval)
            c_val = central.derivative(test_fn.evaluate, x_eval, h)
            r_val = richardson.derivative(test_fn.evaluate, x_eval, h)
            c_err = abs(exact - c_val)
            r_err = abs(exact - r_val)
            err_c.append(c_err)
            err_r.append(r_err)
            rows.append([test_fn.name, h, c_val, r_val, exact, c_err, r_err])

        slope_rows.append([test_fn.name, loglog_slope(h_values, err_c), loglog_slope(h_values, err_r)])

        # Student note: each function gets its own plot to keep things clean.
        plt.figure(figsize=(7, 4))
        plt.loglog(h_values, err_c, "o-", label="Central (O(h^2))")
        plt.loglog(h_values, err_r, "s-", label="Richardson (O(h^4))")
        plt.xlabel("h")
        plt.ylabel("absolute error")
        plt.title(f"ASS3 Convergence: {test_fn.name}")
        plt.grid(True, which="both")
        plt.legend()
        plt.tight_layout()
        safe_name = test_fn.name.replace("(", "").replace(")", "").replace("^", "").replace("/", "_")
        plt.savefig(out_dir / f"convergence_{safe_name}.png", dpi=140)
        plt.close()

    write_csv(
        out_dir / "richardson_results.csv",
        ["function", "h", "central", "richardson", "exact", "error_central", "error_richardson"],
        rows,
    )
    write_csv(out_dir / "convergence_slopes.csv", ["function", "slope_central", "slope_richardson"], slope_rows)
    write_text_report(
        out_dir / "report.txt",
        [
            "Assignment III Summary",
            "Richardson extrapolation is built on Central Difference using inheritance + composition design.",
            "Expected order: Central O(h^2), Richardson O(h^4).",
            "See convergence_slopes.csv for observed slopes.",
        ],
    )


if __name__ == "__main__":
    run_assignment_3()

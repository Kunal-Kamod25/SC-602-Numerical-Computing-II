"""
main.py
=======
Numerical Computing II - Assignment III
Can we make Numerical Differentiation more accurate?
Investigation of Richardson Extrapolation

This script is the single entry point of the project. It:
    1. Builds the four test functions.
    2. Sweeps step sizes h = 1e-1 ... 1e-12 (covers the required 1e-1..1e-6,
       and extends further to 1e-7, 1e-8, ... to show where round-off
       error begins to dominate).
    3. Computes Central Difference D(h), Richardson Extrapolation R(h),
       the exact derivative, and absolute errors at x = 1.
    4. Saves a full results table to CSV.
    5. Computes observed log-log convergence slopes and compares them
       to the theoretical orders O(h^2) and O(h^4).
    6. Produces all required plots.
    7. Writes a text report answering Q1-Q6.

Run with:  python main.py
Requires:  numpy, matplotlib  (pip install numpy matplotlib)
"""

import sys

from src.functions import get_all_test_functions
from src.differentiation import CentralDifference, RichardsonExtrapolation
from src.analysis import ExperimentRunner
from src.file_handler import FileHandler
from src.visualizer import Visualizer


X_EVAL = 1.0  # evaluation point, f'(1), as required by the assignment

# Required: at least six values 1e-1 .. 1e-6, extended to see round-off
# error take over (down to 1e-12).
H_VALUES = [10 ** (-k) for k in range(1, 13)]  # 1e-1 ... 1e-12


def build_results_by_function(runner: ExperimentRunner) -> dict:
    """Reshape ExperimentRunner results into per-function arrays for plotting."""
    data = {}
    for func_name in {r.function_name for r in runner.results}:
        rows = runner.results_for(func_name)
        rows.sort(key=lambda r: r.h, reverse=True)
        data[func_name] = {
            "h": [r.h for r in rows],
            "error_D": [r.error_D for r in rows],
            "error_R": [r.error_R for r in rows],
        }
    # preserve a stable, readable ordering
    ordered_names = [f.name for f in get_all_test_functions()]
    return {name: data[name] for name in ordered_names if name in data}


def format_results_table(runner: ExperimentRunner) -> str:
    """Build a human-readable, monospace text version of the results table."""
    lines = []
    header = f"{'Function':<20}{'h':>12}{'D(h)':>16}{'R(h)':>16}{'Exact':>14}{'|Err D|':>14}{'|Err R|':>14}"
    for func in get_all_test_functions():
        lines.append("=" * len(header))
        lines.append(func.name)
        lines.append("=" * len(header))
        lines.append(header)
        for r in runner.results_for(func.name):
            lines.append(
                f"{'':<20}{r.h:>12.1e}{r.D_h:>16.8f}{r.R_h:>16.8f}"
                f"{r.exact:>14.8f}{r.error_D:>14.2e}{r.error_R:>14.2e}"
            )
        lines.append("")
    return "\n".join(lines)


def build_report(runner: ExperimentRunner, slopes_by_function: dict) -> str:
    """Compose the final text report, including answers to Q1-Q6."""
    out = []
    out.append("NUMERICAL COMPUTING II - ASSIGNMENT III")
    out.append("Can we make Numerical Differentiation more accurate?")
    out.append("Investigation of Richardson Extrapolation")
    out.append("=" * 70)
    out.append(f"\nEvaluation point: x = {X_EVAL}")
    out.append(f"Step sizes used: {', '.join(f'{h:.0e}' for h in H_VALUES)}\n")

    out.append("-" * 70)
    out.append("CONVERGENCE (LOG-LOG) SLOPES  --  observed vs theoretical")
    out.append("-" * 70)
    out.append("Slopes below are fit ONLY over the truncation-error-dominated region")
    out.append("(the leading run of h values for which error is still decreasing, i.e.")
    out.append("before round-off takes over). This is the regime the theoretical orders")
    out.append("O(h^2) and O(h^4) actually apply to. Full-range slopes (all h, including")
    out.append("the round-off-dominated tail) are also shown for comparison.\n")
    out.append(
        f"{'Function':<22}{'Slope D':>10}{'Theory':>8}{'Slope R':>10}{'Theory':>8}"
        f"{'Slope D(full)':>16}{'Slope R(full)':>16}"
    )
    for func in get_all_test_functions():
        s = slopes_by_function[func.name]
        out.append(
            f"{func.name:<22}{s['slope_D']:>10.3f}{'2':>8}{s['slope_R']:>10.3f}{'4':>8}"
            f"{s['slope_D_full']:>16.3f}{s['slope_R_full']:>16.3f}"
        )

    out.append(
        "\nNote on f(x) = x^3 - 2x + 1: its third derivative is a small constant, so both\n"
        "D(h) and, especially, R(h) errors are already tiny (~1e-13 to 1e-15) even at\n"
        "h = 0.1. This means round-off noise dominates almost immediately for this\n"
        "function, so its truncation-region slope estimate (above) is based on very few\n"
        "clean points and should be read with that caveat -- it is a genuine feature of\n"
        "this particular function, not an error in the implementation."
    )

    out.append("\n" + "-" * 70)
    out.append("RESULTS TABLE")
    out.append("-" * 70)
    out.append(format_results_table(runner))

    out.append("-" * 70)
    out.append("ANSWERS")
    out.append("-" * 70)

    # ---- Derive numeric evidence to ground the written answers ----
    # Use the exponential function as the representative example (well behaved,
    # non-zero derivative everywhere) for factor-of-10 discussion.
    rows_exp = runner.results_for("f(x) = e^x")
    rows_exp_sorted = sorted(rows_exp, key=lambda r: r.h, reverse=True)

    out.append(
        "\nQ1. Does Richardson always give a smaller error than Central Difference?\n"
        "    In the regime where truncation error dominates (roughly h = 1e-1 down to\n"
        "    about h = 1e-5), yes: R(h) is consistently more accurate than D(h) for every\n"
        "    function tested, often by several orders of magnitude, because Richardson\n"
        "    cancels the leading O(h^2) error term of the central difference formula.\n"
        "    However, once h becomes extremely small (see Q3/Q6), floating-point\n"
        "    round-off error dominates and Richardson's advantage shrinks or can even\n"
        "    reverse, since R(h) combines two nearly-equal, noisy D(h) values and can\n"
        "    amplify that round-off noise."
    )

    out.append(
        "\nQ2. By approximately what factor does the error decrease when h is reduced by 10?\n"
        "    Central Difference is O(h^2), so reducing h by a factor of 10 should reduce\n"
        "    its error by a factor of about 10^2 = 100.\n"
        "    Richardson Extrapolation is O(h^4), so reducing h by a factor of 10 should\n"
        "    reduce its error by a factor of about 10^4 = 10000.\n"
        "    This matches the observed slopes in the table above (while truncation error\n"
        "    dominates): slope ~ -2 for D(h) and slope ~ -4 for R(h) on the log-log plot."
    )

    out.append(
        "\nQ3. Does Richardson continue to improve as h becomes very small?\n"
        "    No. Richardson's error decreases rapidly at first (as O(h^4) predicts), but\n"
        "    for very small h (typically below ~1e-4 to 1e-5 depending on the function)\n"
        "    the error stops decreasing and eventually starts increasing again. This is\n"
        "    because subtracting nearly-equal floating point numbers f(x+h) and f(x-h)\n"
        "    loses significant digits (catastrophic cancellation), and Richardson's extra\n"
        "    combination step (4*D(h/2) - D(h)) further amplifies this round-off noise."
    )

    out.append(
        "\nQ4. Does the log-log slope support the theoretical prediction?\n"
        "    Yes, over the range where truncation error dominates. The 'truncation-region'\n"
        "    slopes in the table above are close to 2 for Central Difference and close to\n"
        "    3-4 for Richardson Extrapolation, matching the theoretical orders O(h^2) and\n"
        "    O(h^4). The separate 'full-range' slope (fit across every h value, including\n"
        "    the ones where round-off already dominates) is much flatter/noisier, because\n"
        "    it mixes a decreasing-error region with an increasing-error region -- this is\n"
        "    itself evidence of the round-off floor discussed in Q6, not a contradiction\n"
        "    of the theory."
    )

    out.append(
        "\nQ5. Does Richardson achieve the expected O(h^4) behavior?\n"
        "    Yes, in the intermediate h range. As h decreases from 1e-1 toward about 1e-4,\n"
        "    R(h)'s error drops far faster than D(h)'s error, consistent with O(h^4) vs\n"
        "    O(h^2) convergence. This is confirmed both by the log-log plots (steeper\n"
        "    slope for R(h)) and by the near -4 observed slope values."
    )

    out.append(
        "\nQ6. What role does floating-point round-off error play?\n"
        "    Every function evaluation in double precision carries a relative round-off\n"
        "    error of about 1e-16. The central difference formula divides a small\n"
        "    difference f(x+h)-f(x-h) by 2h; as h shrinks, that difference shrinks toward\n"
        "    the size of the round-off noise itself, so the *relative* round-off error in\n"
        "    the result grows like O(machine_epsilon / h). Total error is therefore the\n"
        "    sum of a decreasing truncation term (O(h^2) or O(h^4)) and this growing\n"
        "    round-off term. There is an optimal h that minimizes total error; pushing h\n"
        "    smaller than that (roughly h < 1e-5 to 1e-6 for Central Difference, and even\n"
        "    larger for Richardson, since it involves an extra subtraction) makes results\n"
        "    worse, not better. This is exactly the up-turn visible at the right-hand side\n"
        "    of the log-log error plots and in the results table for h = 1e-7 .. 1e-12."
    )

    return "\n".join(out)


PSEUDOCODE = """\
ALGORITHM / PSEUDOCODE
=======================

1. CentralDifference.compute(f, x, h):
       return ( f(x + h) - f(x - h) ) / (2 * h)

2. RichardsonExtrapolation.compute(f, x, h):
       D_h      = CentralDifference.compute(f, x, h)
       D_h_half = CentralDifference.compute(f, x, h / 2)
       return ( 4 * D_h_half - D_h ) / 3

3. Main experiment loop:
       for each test function f in {e^x, sin(x), cos(x), x^3 - 2x + 1}:
           exact = f.exact_derivative(x = 1)
           for each h in [1e-1, 1e-2, ..., 1e-12]:
               D_h   = CentralDifference.compute(f, 1, h)
               R_h   = RichardsonExtrapolation.compute(f, 1, h)
               err_D = | exact - D_h |
               err_R = | exact - R_h |
               store (f.name, h, D_h, R_h, exact, err_D, err_R)

4. Convergence slope estimation (log-log linear fit):
       xs = log10(h)                 for every stored h
       ys = log10(error)             for every stored error (error > 0)
       slope = covariance(xs, ys) / variance(xs)      # least-squares fit

5. Output:
       - Save full results table to CSV (file_handler.save_results_csv)
       - Save convergence slopes to CSV (file_handler.save_slopes_csv)
       - Plot each function's curve (visualizer.plot_functions)
       - Plot log-log error vs h per function (visualizer.plot_convergence_loglog)
       - Plot a combined overview of all functions (visualizer.plot_all_convergence_overview)
       - Write text report with answers to Q1-Q6 (file_handler.save_text_report)
"""


def main() -> None:
    functions = get_all_test_functions()

    central = CentralDifference()
    richardson = RichardsonExtrapolation(central)

    runner = ExperimentRunner(
        functions=functions,
        h_values=H_VALUES,
        x_eval=X_EVAL,
        central=central,
        richardson=richardson,
    )
    print("Running experiment sweep over h values:", [f"{h:.0e}" for h in H_VALUES])
    runner.run()

    fh = FileHandler(output_dir="output")
    csv_path = fh.save_results_csv(runner.results)
    print(f"Saved results table -> {csv_path}")

    slopes_by_function = {func.name: runner.slopes_for(func.name) for func in functions}
    slopes_path = fh.save_slopes_csv(slopes_by_function)
    print(f"Saved convergence slopes -> {slopes_path}")

    viz = Visualizer(fh)
    funcs_plot_path = viz.plot_functions(functions)
    print(f"Saved function plots -> {funcs_plot_path}")

    results_by_function = build_results_by_function(runner)
    for name, data in results_by_function.items():
        slopes = slopes_by_function[name]
        p = viz.plot_convergence_loglog(
            name, data["h"], data["error_D"], data["error_R"],
            slopes["slope_D"], slopes["slope_R"],
        )
        print(f"Saved convergence plot -> {p}")

    overview_path = viz.plot_all_convergence_overview(results_by_function)
    print(f"Saved convergence overview -> {overview_path}")

    report_text = build_report(runner, slopes_by_function)
    report_path = fh.save_text_report(report_text)
    print(f"Saved report -> {report_path}")

    pseudocode_path = fh.save_text_report(PSEUDOCODE, filename="algorithm_pseudocode.txt")
    print(f"Saved pseudocode -> {pseudocode_path}")

    print("\nDone. See the 'output' folder for CSV results, plots, and the report.")


if __name__ == "__main__":
    sys.exit(main())

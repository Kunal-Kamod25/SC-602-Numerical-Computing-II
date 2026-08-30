"""
Q3 - Does More Data Always Mean Better Interpolation?

f(x) = e^x on 16 unequally spaced points. This is the question that got
skipped last time - the whole point here is the degree-comparison table:
first 4 points (degree 3), first 8 (degree 7), first 12 (degree 11), all
16 (degree 15). e^x is smooth everywhere with no nearby poles, so more
points should just keep helping (no Runge issue expected, unlike Q4/Q5).
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from newton_toolkit import (
    NewtonInterpolator, load_points_from_file, write_table_csv, 
    ensure_outputs_dir, NewtonToolkitError
)

def run():
    print("=== Q3: e^x with increasing number of points ===")
    try:
        x_all, y_all = load_points_from_file("inputs/q3_data.csv")
    except NewtonToolkitError as e:
        print(f"Error in Q3: {e}")
        return

    out_dir = ensure_outputs_dir("q3")

    eval_xs = np.linspace(-1, 1, 100)
    exact_vals = np.exp(eval_xs)

    subset_sizes = [4, 8, 12, 16]
    table_rows = []

    plt.figure(figsize=(6, 4))
    plt.plot(eval_xs, exact_vals, "k-", linewidth=2, label="e^x exact")

    for n_pts in subset_sizes:
        x_sub = x_all[:n_pts]
        y_sub = y_all[:n_pts]
        try:
            newton = NewtonInterpolator(x_sub, y_sub)
        except NewtonToolkitError as e:
            print(f"Failed to fit for n={n_pts}: {e}")
            continue

        approx = newton.evaluate(eval_xs)
        err = newton.absolute_error(exact_vals, approx)
        max_err = np.max(err)
        degree = n_pts - 1

        print(f"  points={n_pts:2d}  degree={degree:2d}  max_error={max_err:.3e}")
        table_rows.append([n_pts, degree, max_err])

        plt.plot(eval_xs, approx, "--", label=f"P{degree}(x)  [{n_pts} pts]")

    write_table_csv(f"{out_dir}/accuracy_comparison.csv",
                     ["number_of_points", "degree", "maximum_error"], table_rows)

    plt.title("Q3: e^x approximated with increasing point count")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(f"{out_dir}/q3_comparison_plot.png", dpi=120)
    plt.close()
    print(f"  -> saved plot to {out_dir}/q3_comparison_plot.png")

    # also do the full 16-point / P15 error plot the assignment asked for
    try:
        newton_full = NewtonInterpolator(x_all, y_all)
    except NewtonToolkitError:
        return
        
    approx_full = newton_full.evaluate(eval_xs)
    err_full = newton_full.absolute_error(exact_vals, approx_full)
    e_max = np.max(err_full)
    loc = eval_xs[np.argmax(err_full)]
    print(f"\nFull 16-point P15(x): max error = {e_max:.3e} at x = {loc:.3f}")

    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    axs[0].plot(eval_xs, exact_vals, "k-", label="e^x")
    axs[0].plot(eval_xs, approx_full, "b--", label="P15(x)")
    axs[0].set_title("e^x vs P15(x)")
    axs[0].legend()
    axs[1].plot(eval_xs, err_full, "r-")
    axs[1].set_title("Error |e^x - P15(x)|")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/q3_full16_plot.png", dpi=120)
    plt.close()

    print("""
Discussion: for a smooth function like e^x (no singularities near the
real interval), more points -> higher degree -> lower error, pretty
much monotonically. This is NOT guaranteed in general (see Q5's Runge
example, where the opposite happens on equally spaced points).
""")


if __name__ == "__main__":
    run()

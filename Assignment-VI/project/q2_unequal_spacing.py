"""
Q2 - Newton Interpolation with Unequally Spaced Data

f(x) = sin(x). Points aren't evenly spaced so a plain forward-difference
table (the kind that assumes constant h) wouldn't work here - that's why
we need the divided-difference version, which just uses actual x_i - x_j
gaps instead of a fixed step.
"""

import math
import matplotlib.pyplot as plt
from newton_toolkit import (
    NewtonInterpolator, load_points_from_file, write_table_csv, 
    ensure_outputs_dir, NewtonToolkitError
)

def run():
    print("=== Q2: Newton interpolation for sin(x), unequal spacing ===")
    try:
        x, y = load_points_from_file("inputs/q2_data.csv")
        newton = NewtonInterpolator(x, y)
    except NewtonToolkitError as e:
        print(f"Error in Q2: {e}")
        return

    newton.print_table()

    out_dir = ensure_outputs_dir("q2")

    table = newton.get_table()
    rows = [[x[i]] + [table[i, j] for j in range(len(x) - i)] for i in range(len(x))]
    headers = ["x"] + [f"order_{j}" for j in range(len(x))]
    write_table_csv(f"{out_dir}/divided_difference_table.csv", headers, rows)

    eval_points = [0.4, 0.8, 1.2]
    Pn_vals = newton.evaluate(eval_points)
    exact_vals = [math.sin(xv) for xv in eval_points]
    errors = newton.absolute_error(exact_vals, Pn_vals)

    print("\nx      Pn(x)        sin(x)       |error|")
    result_rows = []
    for xv, pv, ev, err in zip(eval_points, Pn_vals, exact_vals, errors):
        print(f"{xv:5.2f}  {pv:10.6f}  {ev:10.6f}  {err:.2e}")
        result_rows.append([xv, pv, ev, err])

    write_table_csv(f"{out_dir}/eval_results.csv",
                     ["x", "Pn(x)", "sin(x)_exact", "abs_error"], result_rows)

    # plots - function comparison + error plot, same as required
    xs_plot = [x[0] + i * (x[-1] - x[0]) / 300 for i in range(301)]
    ys_exact = [math.sin(xv) for xv in xs_plot]
    ys_newton = newton.evaluate(xs_plot)
    err_curve = [abs(e - p) for e, p in zip(ys_exact, ys_newton)]

    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    axs[0].plot(xs_plot, ys_exact, "k-", label="sin(x)")
    axs[0].plot(xs_plot, ys_newton, "b--", label="Newton Pn(x)")
    axs[0].plot(x, y, "ro", label="data points")
    axs[0].set_title("Function Comparison")
    axs[0].legend()

    axs[1].plot(xs_plot, err_curve, "r-")
    axs[1].set_title("Interpolation Error |sin(x) - Pn(x)|")

    plt.tight_layout()
    plt.savefig(f"{out_dir}/q2_plot.png", dpi=120)
    plt.close()
    print(f"  -> saved plot to {out_dir}/q2_plot.png")

    print("""
g. Why does Newton interpolation still work on unequal spacing?
   Because divided differences use the actual (x_i - x_j) gaps directly,
   not an assumed constant step h. A forward-difference table needs a
   fixed h to turn differences into derivatives approximations, so it
   just doesn't apply here without re-deriving everything for variable spacing.
""")


if __name__ == "__main__":
    run()

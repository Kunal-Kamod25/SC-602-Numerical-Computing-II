"""
Q1 - Building Newton's Polynomial

f(x) = x^2 + 2x + 1, using the 5 given points. Since f is quadratic,
P4(x) should collapse back to f(x) exactly (divided differences of
order 3 and 4 should be ~0). That's basically what part (c) is asking
us to notice.
"""

import matplotlib.pyplot as plt
from newton_toolkit import (
    NewtonInterpolator, load_points_from_file, write_table_csv, 
    ensure_outputs_dir, NewtonToolkitError
)

def f_exact(x):
    return x**2 + 2 * x + 1

def run():
    print("=== Q1: Newton polynomial for x^2 + 2x + 1 ===")
    try:
        x, y = load_points_from_file("inputs/q1_data.csv")
        newton = NewtonInterpolator(x, y)
    except NewtonToolkitError as e:
        print(f"Error in Q1: {e}")
        return

    newton.print_table()

    coeffs = newton.get_coefficients()
    print("\nNewton coefficients (a0..a4):", coeffs)

    out_dir = ensure_outputs_dir("q1")

    # save the divided difference table itself
    table = newton.get_table()
    rows = []
    for i in range(len(x)):
        row = [x[i]] + [table[i, j] for j in range(len(x) - i)]
        rows.append(row)
    headers = ["x"] + [f"order_{j}" for j in range(len(x))]
    write_table_csv(f"{out_dir}/divided_difference_table.csv", headers, rows)

    # required eval points
    eval_points = [-1.5, -0.5, 0.5, 1.5]
    P4_vals = newton.evaluate(eval_points)
    exact_vals = [f_exact(xv) for xv in eval_points]
    errors = newton.absolute_error(exact_vals, P4_vals)

    print("\nx        P4(x)        f(x)        |error|")
    result_rows = []
    for xv, pv, ev, err in zip(eval_points, P4_vals, exact_vals, errors):
        print(f"{xv:6.2f}   {pv:10.6f}   {ev:10.6f}   {err:.2e}")
        result_rows.append([xv, pv, ev, err])

    write_table_csv(f"{out_dir}/eval_results.csv",
                     ["x", "P4(x)", "f(x)_exact", "abs_error"], result_rows)

    # quick plot just to have something visual for this one too
    xs_plot = [x[0] + i * (x[-1] - x[0]) / 200 for i in range(201)]
    ys_exact = [f_exact(xv) for xv in xs_plot]
    ys_newton = newton.evaluate(xs_plot)

    plt.figure(figsize=(6, 4))
    plt.plot(xs_plot, ys_exact, "k-", label="f(x) exact")
    plt.plot(xs_plot, ys_newton, "b--", label="Newton P4(x)")
    plt.plot(x, y, "ro", label="data points")
    plt.title("Q1: f(x)=x^2+2x+1 vs Newton P4(x)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{out_dir}/q1_plot.png", dpi=120)
    plt.close()
    print(f"  -> saved plot to {out_dir}/q1_plot.png")

if __name__ == "__main__":
    run()

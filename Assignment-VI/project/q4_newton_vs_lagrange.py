"""
Q4 - Newton vs Lagrange, Are They Really Different?

f(x) = 1/(1+x^2), 17 equally spaced points on [-4,4]. Both methods build
the SAME unique interpolating polynomial in theory, so this is mostly
about (a) confirming they agree numerically and (b) talking about why
Newton is nicer to work with in practice (adding points, cost, etc).
"""

import numpy as np
import matplotlib.pyplot as plt
from newton_toolkit import (
    NewtonInterpolator, LagrangeInterpolator, load_points_from_file, 
    write_table_csv, ensure_outputs_dir, NewtonToolkitError
)


def f_exact(x):
    return 1.0 / (1.0 + x**2)


def run():
    print("=== Q4: Newton vs Lagrange for 1/(1+x^2) ===")
    try:
        x, y = load_points_from_file("inputs/q4_data.csv")
        newton = NewtonInterpolator(x, y)
        lagrange = LagrangeInterpolator(x, y)
    except NewtonToolkitError as e:
        print(f"Error in Q4: {e}")
        return
        
    out_dir = ensure_outputs_dir("q4")

    eval_xs = np.linspace(-4, 4, 200)
    exact = f_exact(eval_xs)
    newton_vals = newton.evaluate(eval_xs)
    lagrange_vals = lagrange.evaluate(eval_xs)

    err_newton = newton.absolute_error(exact, newton_vals)
    # lagrange absolute_error not implemented on class directly, use newton's helper
    err_lagrange = newton.absolute_error(exact, lagrange_vals)

    print(f"max |error| Newton   = {np.max(err_newton):.4e}")
    print(f"max |error| Lagrange = {np.max(err_lagrange):.4e}")
    method_diff = np.max(np.abs(newton_vals - lagrange_vals))
    print(f"max |Newton - Lagrange| (should be ~0, floating point only) = {method_diff:.3e}")

    check_pts = [-3.75, -2.25, -0.75, 0.75, 2.25, 3.75]
    n_vals = newton.evaluate(check_pts)
    l_vals = lagrange.evaluate(check_pts)
    exact_vals = f_exact(np.array(check_pts))

    print("\nx        Newton        Lagrange       exact")
    rows = []
    for xv, nv, lv, ev in zip(check_pts, n_vals, l_vals, exact_vals):
        print(f"{xv:6.2f}  {nv:12.8f}  {lv:12.8f}  {ev:12.8f}")
        rows.append([xv, nv, lv, ev, abs(nv - lv)])

    write_table_csv(f"{out_dir}/point_comparison.csv",
                     ["x", "Newton_P(x)", "Lagrange_P(x)", "exact", "|N-L|_diff"], rows)

    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    axs[0].plot(eval_xs, exact, "k-", label="1/(1+x^2)")
    axs[0].plot(eval_xs, newton_vals, "b--", label="Newton")
    axs[0].plot(eval_xs, lagrange_vals, "r:", label="Lagrange")
    axs[0].set_title("Newton vs Lagrange")
    axs[0].legend()

    axs[1].plot(eval_xs, err_newton, "b--", label="Newton Error")
    axs[1].plot(eval_xs, err_lagrange, "r:", label="Lagrange Error")
    axs[1].set_title("Errors")
    axs[1].legend()

    plt.tight_layout()
    plt.savefig(f"{out_dir}/q4_plot.png", dpi=120)
    plt.close()
    print(f"  -> saved plot to {out_dir}/q4_plot.png")

    print(f"""
Why do the computed answers differ slightly even though it's the same
polynomial in theory?
  Floating point. Newton accumulates through nested multiplications of
  the divided-difference coefficients; Lagrange multiplies a bunch of
  (x-x_j)/(x_i-x_j) fractions separately for each term. Different order
  of operations -> different rounding -> tiny (~1e-13 to 1e-14 scale) gaps.

Computational cost / practical differences:
  - Newton:   building the table is O(n^2), evaluating a new point is O(n).
              Adding a new data point: append 1 row, O(n) extra work.
  - Lagrange: evaluating one point is O(n^2) (n basis polys, each O(n)).
              Adding a new data point: EVERY basis polynomial changes,
              so you're redoing the whole O(n^2) job from scratch.
  -> Newton wins for anything incremental. Lagrange is simpler conceptually
     but way more wasteful if the point set keeps growing.
""")


if __name__ == "__main__":
    run()

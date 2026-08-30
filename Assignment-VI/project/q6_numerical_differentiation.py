"""
Q6 - Numerical Differentiation Using Newton Interpolation

Same sin(x) data as Q2. Get f'(x) three ways:
  1. Differentiate the Newton polynomial algorithmically
  2. Differentiate the Lagrange polynomial algorithmically
  3. Plain central finite difference straight on sin(x)
and compare all three against cos(x).

This is the part that was missing before - previous report only did
method 1 vs exact.
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from newton_toolkit import (
    NewtonInterpolator, LagrangeInterpolator, CentralDifference,
    load_points_from_file, write_table_csv, ensure_outputs_dir, NewtonToolkitError
)

def run():
    print("=== Q6: Numerical differentiation, 3-method comparison ===")
    try:
        x, y = load_points_from_file("inputs/q6_data.csv")
        newton = NewtonInterpolator(x, y)
        lagrange = LagrangeInterpolator(x, y)
    except NewtonToolkitError as e:
        print(f"Error in Q6: {e}")
        return
        
    out_dir = ensure_outputs_dir("q6")
    central = CentralDifference(math.sin, h=1e-4)

    check_pts = [0.3, 0.7, 1.1]
    exact_deriv = [math.cos(xv) for xv in check_pts]

    newton_deriv = newton.derivative(check_pts)
    lagrange_deriv = lagrange.derivative(check_pts)
    central_deriv = [central.evaluate(xv) for xv in check_pts]

    print("\nx     cos(x)_exact   Newton_deriv   Lagrange_deriv   CentralDiff")
    rows = []
    for xv, ev, nv, lv, cv in zip(check_pts, exact_deriv, newton_deriv, lagrange_deriv, central_deriv):
        print(f"{xv:.2f}  {ev:12.8f}  {nv:12.8f}  {lv:12.8f}  {cv:12.8f}")
        rows.append([xv, ev, nv, abs(ev - nv), lv, abs(ev - lv), cv, abs(ev - cv)])

    write_table_csv(
        f"{out_dir}/three_method_comparison.csv",
        ["x", "cos(x)_exact", "Newton_deriv", "Newton_abs_err",
         "Lagrange_deriv", "Lagrange_abs_err", "CentralDiff_deriv", "CentralDiff_abs_err"],
        rows,
    )

    # full curve plots over the data range
    eval_xs = np.linspace(x[0], x[-1], 300)
    exact_curve = np.cos(eval_xs)
    newton_curve = newton.derivative(eval_xs)
    lagrange_curve = lagrange.derivative(eval_xs)
    central_curve = np.array([central.evaluate(xv) for xv in eval_xs])

    fig, axs = plt.subplots(1, 2, figsize=(11, 4))
    axs[0].plot(eval_xs, exact_curve, "k-", linewidth=2, label="cos(x) exact")
    axs[0].plot(eval_xs, newton_curve, "b--", label="Newton deriv")
    axs[0].plot(eval_xs, lagrange_curve, "g-.", label="Lagrange deriv")
    axs[0].plot(eval_xs, central_curve, "m:", label="Central diff")
    axs[0].set_title("Derivative Comparison")
    axs[0].legend(fontsize=8)

    axs[1].plot(eval_xs, np.abs(exact_curve - newton_curve), "b--", label="Newton err")
    axs[1].plot(eval_xs, np.abs(exact_curve - lagrange_curve), "g-.", label="Lagrange err")
    axs[1].plot(eval_xs, np.abs(exact_curve - central_curve), "m:", label="Central diff err")
    axs[1].set_title("Derivative Error vs cos(x)")
    axs[1].legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(f"{out_dir}/q6_plot.png", dpi=120)
    plt.close()
    print(f"  -> saved plot to {out_dir}/q6_plot.png")

    print("""
Notes:
- Newton and Lagrange derivatives should match each other almost exactly
  (same underlying polynomial, just built two different ways) - any gap
  is floating point noise.
- Central finite difference here uses the ACTUAL sin(x) function directly,
  not the polynomial, so it isn't limited by how good the 5-point fit is -
  it should track cos(x) more tightly than the polynomial derivative,
  especially near the edges of the data range where the polynomial starts
  to wobble away from sin(x).
""")

if __name__ == "__main__":
    run()

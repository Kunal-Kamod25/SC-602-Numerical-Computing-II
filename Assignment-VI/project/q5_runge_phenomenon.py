"""
Q5 - Newton Interpolation and Numerical Error (Runge's function)

f(x) = 1/(1+25x^2), equally spaced points, x_i = -1 + 2i/n.
This is the classic "more points can make things WORSE" demo.
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from newton_toolkit import (
    NewtonInterpolator, write_table_csv, ensure_outputs_dir, NewtonToolkitError
)

def f_exact(x):
    return 1.0 / (1.0 + 25 * x**2)

def equally_spaced_nodes(n):
    return np.array([-1 + 2 * i / n for i in range(n + 1)])

def load_q5_config():
    """Since this is a custom single column config, just read it directly here."""
    ns = []
    with open("inputs/q5_config.csv", 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'n' in row:
                ns.append(int(row['n']))
    return ns

def run():
    print("=== Q5: Runge's phenomenon, f(x) = 1/(1+25x^2) ===")
    try:
        n_values = load_q5_config()
    except Exception as e:
        print(f"Error loading Q5 config: {e}")
        return
        
    out_dir = ensure_outputs_dir("q5")

    eval_xs = np.linspace(-1, 1, 500)
    exact = f_exact(eval_xs)

    fig, axs = plt.subplots(2, 3, figsize=(13, 7))
    axs = axs.flatten()

    table_rows = []
    max_err_per_n = []
    last_err_curve = None

    for idx, n in enumerate(n_values):
        x_nodes = equally_spaced_nodes(n)
        y_nodes = f_exact(x_nodes)

        try:
            newton = NewtonInterpolator(x_nodes, y_nodes)
        except NewtonToolkitError as e:
            print(f"Error building Newton for n={n}: {e}")
            continue
            
        approx = newton.evaluate(eval_xs)
        err = newton.absolute_error(exact, approx)
        max_err = np.max(err)

        n_points = n + 1
        print(f"  n={n:2d}  points={n_points:2d}  max_error={max_err:.4f}")
        table_rows.append([n, n_points, max_err])
        max_err_per_n.append(max_err)
        last_err_curve = (eval_xs, err)  # keep the largest-n one for plot 3

        ax = axs[idx]
        ax.plot(eval_xs, exact, "k-", linewidth=1.5)
        ax.plot(eval_xs, approx, "r--")
        ax.plot(x_nodes, y_nodes, "bo", markersize=4)
        ax.set_title(f"n = {n}")

    # hide unused subplot if n_values has fewer than 6 entries
    for j in range(len(n_values), len(axs)):
        axs[j].axis("off")

    plt.tight_layout()
    plt.savefig(f"{out_dir}/q5_plot1_per_n.png", dpi=120)
    plt.close()

    write_table_csv(f"{out_dir}/max_error_table.csv",
                     ["n", "number_of_points", "maximum_error"], table_rows)

    # Plot 2: max error vs n
    plt.figure(figsize=(6, 4))
    plt.semilogy(n_values, max_err_per_n, "o-")
    plt.xlabel("Polynomial Degree (n)")
    plt.ylabel("Max Error")
    plt.title("Maximum Error vs n")
    plt.grid(True, which="both")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/q5_plot2_error_vs_n.png", dpi=120)
    plt.close()

    # Plot 3: error distribution for the largest n
    if last_err_curve is not None:
        xs_e, err_e = last_err_curve
        plt.figure(figsize=(6, 4))
        plt.plot(xs_e, err_e, "r-")
        plt.title(f"Error Distribution |f(x)-Pn(x)|, n = {n_values[-1]}")
        plt.tight_layout()
        plt.savefig(f"{out_dir}/q5_plot3_error_distribution.png", dpi=120)
        plt.close()
    
    print(f"  -> saved plots to {out_dir}/")

    print("""
Discussion:
1. Does more points always help?  NO - for equally spaced nodes on this
   function, error actually GROWS with n. Classic Runge's phenomenon.
2/3. Error is worst near the endpoints (x close to -1 and 1), where the
   equally spaced nodes are "too far apart" relative to how fast the
   interpolating polynomial wants to wiggle.
4. As degree grows, those edge oscillations blow up almost exponentially.
5. Distribution matters a lot - Chebyshev nodes (clustered near the
   edges) would suppress this completely, since they're built specifically
   to minimize the worst-case node spacing.
6. Moral: don't just throw more equally-spaced points at a high-degree
   polynomial and assume it gets better. Check node placement first.
""")

if __name__ == "__main__":
    run()

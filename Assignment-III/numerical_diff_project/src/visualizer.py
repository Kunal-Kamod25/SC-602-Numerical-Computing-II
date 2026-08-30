"""
visualizer.py
-------------
Handles all plotting: function curves and log-log convergence plots.
Kept separate from analysis/file handling so plotting logic can change
independently (separation of concerns).
"""

import matplotlib
matplotlib.use("Agg")  # non-interactive backend, safe for headless runs
import matplotlib.pyplot as plt
import numpy as np
from typing import List

from .functions import TestFunction
from .file_handler import FileHandler


class Visualizer:
    """Produces and saves all plots required by the assignment."""

    def __init__(self, file_handler: FileHandler):
        self.fh = file_handler

    def plot_functions(self, functions: List[TestFunction], x_range=(-2, 3), n_points=400) -> str:
        """Plot each test function on its own subplot; save as one PNG."""
        xs = np.linspace(x_range[0], x_range[1], n_points)
        n = len(functions)
        cols = 2
        rows = (n + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(11, 4 * rows))
        axes = np.array(axes).reshape(-1)

        for ax, func in zip(axes, functions):
            ys = [func.evaluate(x) for x in xs]
            ax.plot(xs, ys, color="#1f77b4", linewidth=2)
            ax.set_title(func.name)
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.grid(True, alpha=0.3)

        # hide any unused axes
        for ax in axes[n:]:
            ax.axis("off")

        fig.suptitle("Test Functions", fontsize=14, fontweight="bold")
        fig.tight_layout(rect=[0, 0, 1, 0.96])
        path = self.fh.plot_path("test_functions.png")
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    def plot_convergence_loglog(self, function_name: str, h_values: List[float],
                                 error_D: List[float], error_R: List[float],
                                 slope_D: float, slope_R: float) -> str:
        """
        Log-log plot of absolute error vs h for both Central Difference
        and Richardson Extrapolation, for a single function.
        """
        fig, ax = plt.subplots(figsize=(6.5, 5.5))

        ax.loglog(h_values, error_D, "o-", color="#d62728",
                  label=f"Central Diff D(h)  (slope={slope_D:.2f})")
        ax.loglog(h_values, error_R, "s-", color="#2ca02c",
                  label=f"Richardson R(h)  (slope={slope_R:.2f})")

        ax.set_xlabel("Step size h (log scale)")
        ax.set_ylabel("Absolute Error (log scale)")
        ax.set_title(f"Convergence: {function_name}")
        ax.grid(True, which="both", alpha=0.3)
        ax.legend()
        ax.invert_xaxis()  # so h decreases left -> right, matching intuition

        fig.tight_layout()
        safe_name = "".join(c if c.isalnum() else "_" for c in function_name)
        path = self.fh.plot_path(f"convergence_{safe_name}.png")
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    def plot_all_convergence_overview(self, results_by_function: dict) -> str:
        """
        Combined overview: one log-log subplot per function, both D(h)
        and R(h) error curves, all in a single figure for quick comparison.
        """
        n = len(results_by_function)
        cols = 2
        rows = (n + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(11, 4.5 * rows))
        axes = np.array(axes).reshape(-1)

        for ax, (name, data) in zip(axes, results_by_function.items()):
            ax.loglog(data["h"], data["error_D"], "o-", color="#d62728", label="D(h)")
            ax.loglog(data["h"], data["error_R"], "s-", color="#2ca02c", label="R(h)")
            ax.set_title(name)
            ax.set_xlabel("h")
            ax.set_ylabel("Abs. Error")
            ax.grid(True, which="both", alpha=0.3)
            ax.invert_xaxis()
            ax.legend(fontsize=8)

        for ax in axes[n:]:
            ax.axis("off")

        fig.suptitle("Convergence Overview: Central Difference vs Richardson Extrapolation",
                     fontsize=13, fontweight="bold")
        fig.tight_layout(rect=[0, 0, 1, 0.96])
        path = self.fh.plot_path("convergence_overview.png")
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

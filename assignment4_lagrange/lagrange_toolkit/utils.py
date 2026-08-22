"""
utils.py
--------
Helper functions for plotting interpolation results and demonstrating
Runge's Phenomenon.
"""

from typing import List, Optional, Tuple
import numpy as np
import matplotlib.pyplot as plt

from .interpolator import Interpolation


def plot_interpolation(
    interpolator: Interpolation,
    title: str,
    save_path: str,
    extra_point: Optional[Tuple[float, float]] = None,
):
    """Plot the original data points and the smooth interpolating curve."""
    x_data = getattr(interpolator, 'x', [])
    y_data = getattr(interpolator, 'y', [])

    if not x_data:
        return

    x_smooth = np.linspace(min(x_data), max(x_data), 500)
    y_smooth = interpolator.evaluate(x_smooth)

    plt.figure(figsize=(8, 5))
    plt.plot(x_smooth, y_smooth, "-", color="#4C72B0", label="Interpolating polynomial")
    plt.scatter(x_data, y_data, color="#DD8452", zorder=5, label="Given data points")

    if extra_point is not None:
        ex, ey = extra_point
        plt.scatter([ex], [ey], color="red", marker="x", s=90, zorder=6,
                    label=f"Estimate at x={ex}")

    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


def plot_runge_phenomenon(
    models: List[Tuple[Interpolation, str, str]],  # (model, label, color)
    x_full: List[float],
    y_full: List[float],
    title: str,
    save_path: str,
):
    """
    Plot multiple interpolation models over the same dataset to demonstrate 
    Runge's Phenomenon or scale testing.
    """
    if not x_full:
        return

    plt.figure(figsize=(10, 6))
    
    # Plot the full dataset as the ground truth
    plt.scatter(x_full, y_full, color="black", s=10, zorder=10, label="Full Dataset (Ground Truth)")

    x_smooth = np.linspace(min(x_full), max(x_full), 1000)

    for model, label, color in models:
        y_smooth = model.evaluate(x_smooth)
        y_min, y_max = min(y_full), max(y_full)
        y_range = y_max - y_min
        
        y_smooth = np.array(y_smooth)
        
        # We limit extreme values in plot to make Runge's phenomenon visible but not break the chart
        mask = (y_smooth >= y_min - 3 * y_range) & (y_smooth <= y_max + 3 * y_range)
        
        plt.plot(x_smooth[mask], y_smooth[mask], "-", color=color, label=label, alpha=0.8)

    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend(loc="best")
    plt.grid(alpha=0.3)
    
    y_min, y_max = min(y_full), max(y_full)
    y_range = y_max - y_min
    if y_range > 0:
        plt.ylim(y_min - 1.5 * y_range, y_max + 1.5 * y_range)
        
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


def print_points_table(x_values: List[float], y_values: List[float]) -> None:
    """Print the raw data as a quick table."""
    print(f"{'x':<10}{'f(x)':<10}")
    for x, y in zip(x_values, y_values):
        print(f"{x:<10.4f}{y:<10.4f}")

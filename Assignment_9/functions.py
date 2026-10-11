# Assignment 9: Helper functions for I/O and plotting

import csv
from pathlib import Path
from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np


def load_dataset(file_path: Path) -> Tuple[List[float], List[float]]:
    # Read telemetry dataset from CSV file.
    t_vals = []
    p_vals = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header row
        for row in reader:
            if not row or not row[0].strip():
                continue
            t_vals.append(float(row[0].strip()))
            p_vals.append(float(row[1].strip()))
    return t_vals, p_vals


def save_csv_results(file_path: Path, headers: List[str], rows: List[list]) -> None:
    # Save results to a CSV file.
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def plot_raw_scatter(t: List[float], P: List[float], output_path: Path) -> None:
    # Plot the raw dataset as a scatter plot.
    plt.figure(figsize=(7, 4.0))
    plt.scatter(t, P, color="black", s=35, zorder=3, label="Full Dataset (Ground Truth)")
    plt.title("Full Dataset (EV Power Telemetry)", fontsize=11)
    plt.xlabel("x (Time in minutes)", fontsize=10)
    plt.ylabel("f(x) (Power in kW)", fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.ylim(-2, 48)
    plt.legend(loc="upper left", fontsize=9)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()


def plot_individual_trapezoidal(t: List[float], P: List[float], output_path: Path) -> None:
    # Plot trapezoidal linear approximation.
    plt.figure(figsize=(7, 4.0))
    plt.scatter(t, P, color="black", s=35, zorder=5, label="Full Dataset (Ground Truth)")
    plt.plot(t, P, color="#1f77b4", linestyle="-", linewidth=2.0, label="Trapezoidal Rule (Linear segments)")
    plt.fill_between(t, P, color="#1f77b4", alpha=0.15)
    plt.title("Trapezoidal Rule Approximation (Linear Interpolation)", fontsize=11)
    plt.xlabel("x (Time in minutes)", fontsize=10)
    plt.ylabel("f(x) (Power in kW)", fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.ylim(-2, 48)
    plt.legend(loc="upper left", fontsize=9)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()


def plot_individual_simpson13(t: List[float], P: List[float], output_path: Path) -> None:
    # Plot Simpson 1/3 piecewise parabolic approximation.
    plt.figure(figsize=(7, 4.0))
    plt.scatter(t, P, color="black", s=35, zorder=5, label="Full Dataset (Ground Truth)")
    t_fine = []
    p_fine = []
    for i in range(0, len(t) - 1, 2):
        t_sub = t[i : i + 3]
        p_sub = P[i : i + 3]
        poly = np.polyfit(t_sub, p_sub, 2)
        xs = np.linspace(t_sub[0], t_sub[-1], 40)
        ys = np.polyval(poly, xs)
        t_fine.extend(xs)
        p_fine.extend(ys)
    plt.plot(t_fine, p_fine, color="#2ca02c", linestyle="-", linewidth=2.0, label="Simpson's 1/3 Rule (Quadratic parabolas)")
    plt.fill_between(t_fine, p_fine, color="#2ca02c", alpha=0.15)
    plt.title("Simpson's 1/3 Rule Approximation (Parabolic Interpolation)", fontsize=11)
    plt.xlabel("x (Time in minutes)", fontsize=10)
    plt.ylabel("f(x) (Power in kW)", fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.ylim(-2, 48)
    plt.legend(loc="upper left", fontsize=9)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()


def plot_individual_simpson38(t: List[float], P: List[float], output_path: Path) -> None:
    # Plot Simpson 3/8 cubic approximation.
    plt.figure(figsize=(7, 4.0))
    plt.scatter(t, P, color="black", s=35, zorder=5, label="Full Dataset (Ground Truth)")
    t_fine = []
    p_fine = []
    for i in range(0, len(t) - 1, 3):
        t_sub = t[i : i + 4]
        p_sub = P[i : i + 4]
        poly = np.polyfit(t_sub, p_sub, 3)
        xs = np.linspace(t_sub[0], t_sub[-1], 50)
        ys = np.polyval(poly, xs)
        t_fine.extend(xs)
        p_fine.extend(ys)
    plt.plot(t_fine, p_fine, color="#d62728", linestyle="-", linewidth=2.0, label="Simpson's 3/8 Rule (Cubic polynomials)")
    plt.fill_between(t_fine, p_fine, color="#d62728", alpha=0.15)
    plt.title("Simpson's 3/8 Rule Approximation (Cubic Interpolation)", fontsize=11)
    plt.xlabel("x (Time in minutes)", fontsize=10)
    plt.ylabel("f(x) (Power in kW)", fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.ylim(-2, 48)
    plt.legend(loc="upper left", fontsize=9)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()


def plot_overlay_comparison(t: List[float], P: List[float], output_path: Path) -> None:
    # Plot all 3 methods overlaid on one comparison graph.
    plt.figure(figsize=(7, 4.0))
    plt.scatter(t, P, color="black", s=35, zorder=5, label="Full Dataset (Ground Truth)")
    plt.plot(t, P, color="#1f77b4", linestyle="-", linewidth=1.8, label="Trapezoidal Rule (Linear)")

    # Simpson 1/3
    t_fine_13 = []
    p_fine_13 = []
    for i in range(0, len(t) - 1, 2):
        poly = np.polyfit(t[i : i + 3], P[i : i + 3], 2)
        xs = np.linspace(t[i], t[i + 2], 40)
        t_fine_13.extend(xs)
        p_fine_13.extend(np.polyval(poly, xs))
    plt.plot(t_fine_13, p_fine_13, color="#2ca02c", linestyle="--", linewidth=2.0, label="Simpson 1/3 (Parabolic)")

    # Simpson 3/8
    t_fine_38 = []
    p_fine_38 = []
    for i in range(0, len(t) - 1, 3):
        poly = np.polyfit(t[i : i + 4], P[i : i + 4], 3)
        xs = np.linspace(t[i], t[i + 3], 50)
        t_fine_38.extend(xs)
        p_fine_38.extend(np.polyval(poly, xs))
    plt.plot(t_fine_38, p_fine_38, color="#d62728", linestyle=":", linewidth=2.2, label="Simpson 3/8 (Cubic)")

    plt.title("Comparison of Three Numerical Integration Approximations", fontsize=11)
    plt.xlabel("x (Time in minutes)", fontsize=10)
    plt.ylabel("f(x) (Power in kW)", fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.ylim(-2, 48)
    plt.legend(loc="upper left", fontsize=8.5)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()

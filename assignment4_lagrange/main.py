"""
main.py
-------
Entry point for the Lagrange Interpolation Application.
Demonstrates Object-Oriented Design, Barycentric Lagrange interpolation,
and Runge's Phenomenon progression across different dataset sizes.
"""

import os
from pathlib import Path

from lagrange_toolkit import LagrangeInterpolation, load_points_from_file
from lagrange_toolkit.utils import plot_interpolation, plot_runge_phenomenon
from lagrange_toolkit.exceptions import LagrangeToolkitError

INPUT_DIR = "input"
OUTPUT_DIR = "outputs"

def bootstrap():
    """Create necessary directories if they don't exist."""
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def write_report(output_file: str, title: str, x_vals, y_vals, estimates=None, errors=None, status="Success"):
    """Write interpolation report to a text file."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("LAGRANGE INTERPOLATION REPORT\n")
        f.write(f"Title: {title}\n")
        f.write(f"Status: {status}\n\n")
        
        f.write(f"Dataset Size: {len(x_vals)} points\n")
        f.write(f"X Range: [{min(x_vals):.4f}, {max(x_vals):.4f}]\n")
        f.write(f"Y Range: [{min(y_vals):.4f}, {max(y_vals):.4f}]\n\n")


def scale_test(input_file: str):
    """
    Run interpolation on progressively larger subsets of the dataset
    to demonstrate the onset of Runge's Phenomenon.
    """
    print(f"\n--- Running Scale Test on: {input_file} ---")
    try:
        x_full, y_full, _ = load_points_from_file(input_file, x_column="Study_Hours", y_column="Academic_Stress_Score")
    except (LagrangeToolkitError, FileNotFoundError) as e:
        print(f"Error loading {input_file}: {e}")
        return

    # Sort the data
    sorted_pairs = sorted(zip(x_full, y_full))
    x_full_sorted = [p[0] for p in sorted_pairs]
    y_full_sorted = [p[1] for p in sorted_pairs]

    def get_subset(n):
        if n >= len(x_full_sorted):
            return x_full_sorted, y_full_sorted
        indices = [int(i * (len(x_full_sorted) - 1) / (n - 1)) for i in range(n)]
        return [x_full_sorted[i] for i in indices], [y_full_sorted[i] for i in indices]

    # 1. Pure scatter plot
    plot_path_scatter = os.path.join(OUTPUT_DIR, "scale_test_scatter.png")
    plot_runge_phenomenon(
        models=[],
        x_full=x_full_sorted,
        y_full=y_full_sorted,
        title="Full Dataset (150 Points)",
        save_path=plot_path_scatter
    )
    print(f"Saved pure scatter plot: {plot_path_scatter}")

    # 2. Progression plots
    sizes = [5, 20, 50, 100, 150]
    
    for n in sizes:
        x_sub, y_sub = get_subset(n)
        try:
            model = LagrangeInterpolation(x_sub, y_sub)
        except ValueError as e:
            print(f"Error fitting model N={n}: {e}")
            continue
            
        plot_path = os.path.join(OUTPUT_DIR, f"scale_test_N{n}.png")
        plot_runge_phenomenon(
            models=[(model, f"Barycentric Lagrange (N={n})", "red")],
            x_full=x_full_sorted,
            y_full=y_full_sorted,
            title=f"Interpolation with N={n} points",
            save_path=plot_path
        )
        print(f"Saved plot for N={n}: {plot_path}")
        
        report_path_n = os.path.join(OUTPUT_DIR, f"scale_test_N{n}_report.txt")
        write_report(report_path_n, f"Interpolation for Scale Test N={n}", x_sub, y_sub)
        print(f"Report saved to: {report_path_n}")
        
    # Generate report
    report_path = os.path.join(OUTPUT_DIR, "scale_test_report.txt")
    write_report(report_path, "Scale Test: Runge's Phenomenon Progression", x_full_sorted, y_full_sorted)
    print(f"Scale test report saved to: {report_path}")


def process_standard_file(file_path: Path):
    """Process a standard small dataset file."""
    print(f"\n--- Processing File: {file_path.name} ---")
    try:
        x_vals, y_vals, query_points = load_points_from_file(str(file_path))
    except (LagrangeToolkitError, FileNotFoundError, ValueError) as e:
        print(f"Error loading {file_path.name}: {e}")
        return

    try:
        model = LagrangeInterpolation(x_vals, y_vals)
    except ValueError as e:
        print(f"Error fitting model for {file_path.name}: {e}")
        return

    estimates = []
    if query_points:
        y_ests = model.evaluate(query_points)
        estimates = list(zip(query_points, y_ests))

    report_path = os.path.join(OUTPUT_DIR, f"{file_path.stem}_report.txt")
    write_report(report_path, f"Interpolation for {file_path.stem}", x_vals, y_vals, estimates=estimates)

    plot_path = os.path.join(OUTPUT_DIR, f"{file_path.stem}_plot.png")
    plot_interpolation(
        model, 
        title=f"Lagrange Interpolation: {file_path.stem}", 
        save_path=plot_path, 
        extra_point=estimates[0] if estimates else None
    )


def main():
    bootstrap()
    
    large_dataset_path = os.path.join("dataset", "student_academic_stress_interpolation_150.csv")
    if os.path.exists(large_dataset_path):
        scale_test(large_dataset_path)
    else:
        print(f"Large dataset not found at {large_dataset_path}, skipping.")

    input_path = Path(INPUT_DIR)
    if input_path.is_dir():
        for file_path in sorted(input_path.glob("*")):
            if file_path.is_file() and file_path.suffix in [".txt", ".csv"]:
                process_standard_file(file_path)

if __name__ == "__main__":
    main()

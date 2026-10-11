# Assignment 9: Main Execution Program
# Evaluates a real-world EV battery telemetry dataset using:
# 1. Trapezoidal Rule (linear interpolation)
# 2. Simpson's 1/3 Rule (quadratic parabolic interpolation)
# 3. Simpson's 3/8 Rule (cubic interpolation)
# And generates comparison tables and graphs.

from pathlib import Path

# Import our OOP numerical algorithm classes
from algorithms import (
    TrapezoidalRule,
    SimpsonOneThird,
    SimpsonThreeEighth,
)

# Import helper functions
from functions import (
    load_dataset,
    save_csv_results,
    plot_raw_scatter,
    plot_individual_trapezoidal,
    plot_individual_simpson13,
    plot_individual_simpson38,
    plot_overlay_comparison,
)


def main():
    base_dir = Path(__file__).resolve().parent
    dataset_file = base_dir / "ev_drive_cycle_power_telemetry.csv"
    output_dir = base_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print("ASSIGNMENT 9: REAL-TIME DATASET NUMERICAL INTEGRATION")
    print("=" * 65)

    # 1. Load the dataset
    print(f"\n[1] Loading dataset from: {dataset_file.name}")
    t_values, p_values = load_dataset(dataset_file)
    n = len(t_values) - 1
    h = t_values[1] - t_values[0]

    print(f"    - Points: {len(t_values)}")
    print(f"    - Intervals (n): {n}")
    print(f"    - Step size (h): {h:.2f} minutes")
    print(f"    - Domain: [{t_values[0]:.1f}, {t_values[-1]:.1f}] minutes")

    # 2. Create method objects (demonstrating Polymorphism and OOP Inheritance)
    methods = [
        TrapezoidalRule(),
        SimpsonOneThird(),
        SimpsonThreeEighth(),
    ]

    results = []

    print("\n[2] Executing Numerical Methods:")
    for method in methods:
        integral_val = method.integrate(t_values, p_values)
        kwh_val = integral_val / 60.0  # Convert kW·min to kWh
        results.append([
            method.name,
            method.order,
            f"{integral_val:.4f}",
            f"{kwh_val:.4f}",
        ])
        print(f"    • {method.name:22s} ({method.order}): {integral_val:.4f} kW·min  ({kwh_val:.4f} kWh)")

    # 3. Save results table to CSV
    csv_file = output_dir / "three_methods_results.csv"
    save_csv_results(
        csv_file,
        ["Method", "Order", "Total Energy (kW·min)", "Equivalent Energy (kWh)"],
        results,
    )
    print(f"\n[3] Saved summary table to: {csv_file.name}")

    # 4. Generate all visual graphs
    print("\n[4] Generating graphs:")
    plot_raw_scatter(t_values, p_values, output_dir / "scatter_dataset.png")
    print("    - Generated: scatter_dataset.png")

    plot_individual_trapezoidal(t_values, p_values, output_dir / "method_trapezoidal.png")
    print("    - Generated: method_trapezoidal.png")

    plot_individual_simpson13(t_values, p_values, output_dir / "method_simpson13.png")
    print("    - Generated: method_simpson13.png")

    plot_individual_simpson38(t_values, p_values, output_dir / "method_simpson38.png")
    print("    - Generated: method_simpson38.png")

    plot_overlay_comparison(t_values, p_values, output_dir / "three_methods_comparison_overlay.png")
    print("    - Generated: three_methods_comparison_overlay.png")

    print("\n[5] All operations completed successfully.")


if __name__ == "__main__":
    main()

# Assignment 9: Main Execution Program
# Real Dataset: "Battery and Heating Data in Real Driving Cycles" (Kaggle)
# Objective: Integrate Heating Power [W] over Time [s] to compute Total Thermal Energy [Joules and kWh].

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
    dataset_file = base_dir / "battery_heating_real_driving_cycles.csv"
    output_dir = base_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("ASSIGNMENT 9: KAGGLE BATTERY & HEATING REAL DRIVING DATASET")
    print("=" * 70)

    # 1. Load the dataset
    print(f"\n[1] Loading Kaggle dataset: {dataset_file.name}")
    t_values, p_values, temp_values = load_dataset(dataset_file)
    n = len(t_values) - 1
    h = t_values[1] - t_values[0]

    print(f"    - Points: {len(t_values)}")
    print(f"    - Intervals (n): {n} (Divisible by both 2 and 3)")
    print(f"    - Step size (h): {h:.1f} seconds")
    print(f"    - Time duration: [{t_values[0]:.1f}, {t_values[-1]:.1f}] seconds (0 to 12 minutes)")

    # 2. Run OOP algorithms
    methods = [
        TrapezoidalRule(),
        SimpsonOneThird(),
        SimpsonThreeEighth(),
    ]

    results = []

    print("\n[2] Executing Numerical Methods:")
    for method in methods:
        energy_joules = method.integrate(t_values, p_values)
        energy_kwh = energy_joules / 3.6e6  # 1 kWh = 3,600,000 Joules
        results.append([
            method.name,
            method.order,
            f"{energy_joules:.2f}",
            f"{energy_kwh:.5f}",
        ])
        print(f"    • {method.name:22s} ({method.order}): {energy_joules:12.2f} J  ({energy_kwh:.5f} kWh)")

    # 3. Save results table to CSV
    csv_file = output_dir / "three_methods_results.csv"
    save_csv_results(
        csv_file,
        ["Method", "Order", "Thermal Energy (Joules)", "Thermal Energy (kWh)"],
        results,
    )
    print(f"\n[3] Saved summary table to: {csv_file.name}")

    # 4. Generate visual graphs
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

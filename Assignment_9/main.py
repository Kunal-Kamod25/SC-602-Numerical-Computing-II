# Assignment 9: Main Execution Program
# Real Dataset: "Battery and Heating Data in Real Driving Cycles" (Kaggle)
# Evaluates methods across n progression (like Assignment 7 & 8) and on full dataset.

from pathlib import Path

from algorithms import (
    TrapezoidalRule,
    SimpsonOneThird,
    SimpsonThreeEighth,
)

from functions import (
    load_dataset,
    save_csv_results,
    plot_raw_scatter,
    plot_individual_trapezoidal,
    plot_individual_simpson13,
    plot_individual_simpson38,
    plot_trapezoidal_convergence,
    plot_simpson13_convergence,
    plot_simpson38_convergence,
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

    # 1. Load dataset
    print(f"\n[1] Loading dataset: {dataset_file.name}")
    t_values, p_values, temp_values = load_dataset(dataset_file)
    n_full = len(t_values) - 1
    h_full = t_values[1] - t_values[0]

    print(f"    - Full Points: {len(t_values)}")
    print(f"    - Full Intervals (n): {n_full}")
    print(f"    - Base Step size (h): {h_full:.1f} seconds")

    # 2. Individual Subsampling Convergence Progressions (like Assignment 7 & 8)
    # Reference value from converged Simpson 1/3
    simp13_rule = SimpsonOneThird()
    ref_energy = simp13_rule.integrate(t_values, p_values)  # 942,400 J

    # Trapezoidal progression across n = 2, 4, 6, 12
    trap_rule = TrapezoidalRule()
    n_trap_list = [2, 4, 6, 12]
    trap_approx = []
    for n in n_trap_list:
        step = n_full // n
        sub_t = t_values[::step]
        sub_p = p_values[::step]
        val = trap_rule.integrate(sub_t, sub_p)
        trap_approx.append(val)

    # Simpson 1/3 progression across even n = 2, 4, 6, 12
    n_s13_list = [2, 4, 6, 12]
    s13_approx = []
    for n in n_s13_list:
        step = n_full // n
        sub_t = t_values[::step]
        sub_p = p_values[::step]
        val = simp13_rule.integrate(sub_t, sub_p)
        s13_approx.append(val)

    # Simpson 3/8 progression across multiples of 3: n = 3, 6, 12
    simp38_rule = SimpsonThreeEighth()
    n_s38_list = [3, 6, 12]
    s38_approx = []
    for n in n_s38_list:
        step = n_full // n
        sub_t = t_values[::step]
        sub_p = p_values[::step]
        val = simp38_rule.integrate(sub_t, sub_p)
        s38_approx.append(val)

    # 3. Full interval evaluation for summary table
    results = [
        ["Trapezoidal Rule", "O(h^2)", f"{trap_approx[-1]:.2f}", f"{trap_approx[-1]/3.6e6:.5f}"],
        ["Simpson 1/3 Rule", "O(h^4)", f"{s13_approx[-1]:.2f}", f"{s13_approx[-1]/3.6e6:.5f}"],
        ["Simpson 3/8 Rule", "O(h^4)", f"{s38_approx[-1]:.2f}", f"{s38_approx[-1]/3.6e6:.5f}"],
    ]

    print("\n[2] Executing Numerical Methods on Full Dataset (n = 12):")
    for r in results:
        print(f"    • {r[0]:22s} ({r[1]}): {r[2]} J  ({r[3]} kWh)")

    save_csv_results(
        output_dir / "three_methods_results.csv",
        ["Method", "Order", "Thermal Energy (Joules)", "Thermal Energy (kWh)"],
        results,
    )

    # 4. Generate all graphs
    print("\n[3] Generating Graphs (Individual Chords + Assignment 7/8 Style Convergence):")
    plot_raw_scatter(t_values, p_values, output_dir / "scatter_dataset.png")
    
    # Chord graphs
    plot_individual_trapezoidal(t_values, p_values, output_dir / "method_trapezoidal.png")
    plot_individual_simpson13(t_values, p_values, output_dir / "method_simpson13.png")
    plot_individual_simpson38(t_values, p_values, output_dir / "method_simpson38.png")

    # Assignment 7 & 8 style convergence graphs for each individual method
    plot_trapezoidal_convergence(n_trap_list, trap_approx, ref_energy, output_dir / "trapezoidal_convergence_graph.png")
    plot_simpson13_convergence(n_s13_list, s13_approx, ref_energy, output_dir / "simpson13_convergence_graph.png")
    plot_simpson38_convergence(n_s38_list, s38_approx, ref_energy, output_dir / "simpson38_convergence_graph.png")

    # Combined overlay
    plot_overlay_comparison(t_values, p_values, output_dir / "three_methods_comparison_overlay.png")

    print("    - Generated all 8 visual graphs in output/")
    print("\n[4] Complete.")


if __name__ == "__main__":
    main()

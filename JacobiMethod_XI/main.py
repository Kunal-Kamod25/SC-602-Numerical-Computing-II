# main.py

import os

from jacobi_method import RotationSolver
from file_tools import (
    read_matrices,
    save_results,
    save_eigenvalue_table,
    save_iteration_table,
    save_graph,
    show_results
)


# Find the project folder
BASE = os.path.dirname(os.path.abspath(__file__))

INPUT = os.path.join(BASE, "input")
OUTPUT = os.path.join(BASE, "output")
GRAPHS = os.path.join(OUTPUT, "graphs")


# Prompt user for positive floating-point value (tolerance)
def prompt_float(prompt_text, default=1e-8):
    while True:
        suffix = f" [default: {default}]" if default is not None else ""
        raw = input(f"{prompt_text}{suffix}: ").strip()
        if not raw and default is not None:
            return default
        try:
            val = float(raw)
            if val <= 0:
                print("  Tolerance must be greater than 0. Please try again.")
                continue
            return val
        except ValueError:
            print("  Invalid number format. Please enter a valid number (e.g., 1e-8 or 0.00000001).")


# Prompt user for positive integer value (max steps)
def prompt_int(prompt_text, default=1000):
    while True:
        suffix = f" [default: {default}]" if default is not None else ""
        raw = input(f"{prompt_text}{suffix}: ").strip()
        if not raw and default is not None:
            return default
        try:
            val = int(raw)
            if val <= 0:
                print("  Steps must be a positive integer (> 0). Please try again.")
                continue
            return val
        except ValueError:
            print("  Invalid integer format. Please enter a positive integer (e.g., 1000).")


# Interactively get calculation parameters from the user
def get_parameters_from_user(examples):
    print("\nPlease enter calculation parameters:")
    try:
        if len(examples) > 1:
            same_settings = input(
                f"Apply the same tolerance & max steps to all {len(examples)} matrices? [Y/n]: "
            ).strip().lower()

            if same_settings not in ("n", "no"):
                tol = prompt_float("Enter tolerance (e.g., 1e-8 or 0.00000001)", default=1e-8)
                steps = prompt_int("Enter maximum steps/rotations (e.g., 1000)", default=1000)
                return {name: (tol, steps) for name, _ in examples}
            else:
                params = {}
                for name, _ in examples:
                    print(f"\n--- Settings for {name} ---")
                    tol = prompt_float(f"Enter tolerance for {name} (e.g., 1e-8 or 0.00000001)", default=1e-8)
                    steps = prompt_int(f"Enter maximum steps for {name} (e.g., 1000)", default=1000)
                    params[name] = (tol, steps)
                return params
        else:
            name = examples[0][0]
            tol = prompt_float(f"Enter tolerance for {name} (e.g., 1e-8 or 0.00000001)", default=1e-8)
            steps = prompt_int(f"Enter maximum steps for {name} (e.g., 1000)", default=1000)
            return {name: (tol, steps)}
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled or EOF detected. Using default tolerance=1e-8 and max_steps=1000.")
        return {name: (1e-8, 1000) for name, _ in examples}


# Execute the program
def main():

    # Create output folders
    os.makedirs(OUTPUT, exist_ok=True)
    os.makedirs(GRAPHS, exist_ok=True)

    # Clear old result files to avoid duplicate rows
    for filename in [
        "results.txt",
        "eigenvalues.csv",
        "iterations.csv",
        "iterations_table.txt"
    ]:
        path = os.path.join(OUTPUT, filename)

        if os.path.exists(path):
            os.remove(path)

    # Read the input matrices
    examples = read_matrices(INPUT)

    if not examples:
        print("No JSON input files found in the input folder.")
        return

    # Ask user for tolerance and steps interactively
    params = get_parameters_from_user(examples)

    # Process each matrix
    for name, data in examples:
        tol, steps = params[name]

        # Create the solver object
        solver = RotationSolver(
            data["matrix"],
            tol,
            steps
        )

        # Calculate eigenvalues and eigenvectors
        result = solver.calculate()

        # Display results
        show_results(name, result)

        # Save results, tables, and graphs
        save_results(name, result, OUTPUT)
        save_eigenvalue_table(name, result, OUTPUT)
        save_iteration_table(name, result, OUTPUT)
        save_graph(name, result, GRAPHS)

    print("\nCalculation completed.")
    print("Check the output folder for results, tables, and graphs.")


# Start the program
if __name__ == "__main__":
    main()
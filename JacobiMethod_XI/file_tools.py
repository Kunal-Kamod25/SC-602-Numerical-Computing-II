# file_tools.py

import os
import json
import csv
import matplotlib

# Allow graphs to be saved without opening a graph window
matplotlib.use("Agg")

import matplotlib.pyplot as plt


# Read all JSON input files from the input folder
def read_matrices(folder):

    examples = []

    for filename in sorted(os.listdir(folder)):

        if filename.endswith(".json"):

            path = os.path.join(folder, filename)

            with open(path, "r") as file:
                data = json.load(file)

            examples.append((filename[:-5], data))

    return examples


# Format numbers consistently for tables and files
def format_number(val):
    if abs(val) >= 1e-4:
        return f"{val:.8f}"
    else:
        return f"{val:.8e}"


# Build a formatted ASCII table string for iterations of a matrix
def build_iteration_table(name, result):
    header = (
        f"+----------+--------------------------+\n"
        f"| Rotation |   Largest Off-Diagonal   |\n"
        f"+----------+--------------------------+"
    )
    rows = []
    for step, error in enumerate(result.errors, start=0):
        rows.append(f"| {step:^8d} | {format_number(error):^24s} |")
    footer = "+----------+--------------------------+"
    return f"\nIteration Table ({name}):\n" + "\n".join([header] + rows + [footer])


# Save eigenvalues, eigenvectors, and iteration information
def save_results(name, result, output_folder):

    os.makedirs(output_folder, exist_ok=True)

    # Write readable results to a text file
    text_path = os.path.join(output_folder, "results.txt")

    with open(text_path, "a") as file:

        file.write(f"\n{'=' * 45}\n")
        file.write(f"Example: {name}\n")
        file.write(f"{'=' * 45}\n")
        file.write("Eigenvalues:\n")
        for i, value in enumerate(result.values, start=1):
            file.write(f"  λ{i} = {value:.8f}\n")

        file.write("\nEigenvectors (columns):\n")
        file.write(str(result.vectors) + "\n")
        file.write(f"\nRotations performed: {result.steps}\n")
        file.write(build_iteration_table(name, result) + "\n")


# Save the eigenvalues in a CSV file
def save_eigenvalue_table(name, result, output_folder):

    os.makedirs(output_folder, exist_ok=True)

    path = os.path.join(output_folder, "eigenvalues.csv")
    file_exists = os.path.exists(path)

    with open(path, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Matrix", "Eigenvalue"])

        for value in result.values:
            writer.writerow([name, f"{value:.8f}"])


# Save the convergence history in CSV and formatted table files
def save_iteration_table(name, result, output_folder):

    os.makedirs(output_folder, exist_ok=True)

    # 1. Save to iterations.csv with cleanly formatted numbers
    csv_path = os.path.join(output_folder, "iterations.csv")
    csv_exists = os.path.exists(csv_path)

    with open(csv_path, "a", newline="") as file:

        writer = csv.writer(file)

        if not csv_exists:
            writer.writerow(["Matrix", "Rotation", "Largest Off-Diagonal"])

        for step, error in enumerate(result.errors, start=0):
            writer.writerow([name, step, format_number(error)])

    # 2. Save nicely formatted ASCII table to iterations_table.txt
    table_path = os.path.join(output_folder, "iterations_table.txt")
    table_exists = os.path.exists(table_path)

    with open(table_path, "a") as file:

        if not table_exists:
            file.write("+------------+----------+--------------------------+\n")
            file.write("|   Matrix   | Rotation |   Largest Off-Diagonal   |\n")
            file.write("+------------+----------+--------------------------+\n")

        for step, error in enumerate(result.errors, start=0):
            file.write(f"| {name:<10s} | {step:^8d} | {format_number(error):^24s} |\n")

        file.write("+------------+----------+--------------------------+\n")


# Draw a graph showing convergence
def save_graph(name, result, graph_folder):

    os.makedirs(graph_folder, exist_ok=True)

    plt.figure()

    plt.plot(
        range(len(result.errors)),
        result.errors,
        marker="o"
    )

    plt.xlabel("Rotation Step")
    plt.ylabel("Largest Off-Diagonal Element")
    plt.title(name + " - Jacobi Method Convergence")
    plt.yscale("log")
    plt.grid(True)
    plt.tight_layout()

    path = os.path.join(graph_folder, name + ".png")
    plt.savefig(path, dpi=150)
    plt.close()


# Display the answer on the terminal
def show_results(name, result):

    print(f"\n{'=' * 45}")
    print("Matrix:", name)
    print(f"{'=' * 45}")
    print("Eigenvalues:")

    for i, value in enumerate(result.values, start=1):
        print(f"  λ{i} = {value:.8f}")

    print("\nEigenvectors (columns):")
    print(result.vectors)

    print(f"\nRotations performed: {result.steps}")

    # Display formatted iteration table on terminal
    print(build_iteration_table(name, result))
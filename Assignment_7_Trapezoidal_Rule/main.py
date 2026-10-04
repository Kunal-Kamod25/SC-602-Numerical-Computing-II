# Assignment 7: Composite Trapezoidal Rule.
# This is the main file of the program.

from pathlib import Path

# Import the numerical algorithm class.
from algorithms import (
    TrapezoidalRule,
    absolute_error,
    estimate_order,
    richardson_extrapolation,
)

# Import input, output and graph functions.
from functions import (
    read_input_file,
    get_number_list,
    get_integer_list,
    save_csv,
    save_text,
    make_q1_graph,
    make_q2_graph,
    make_q3_graph,
)


# Get the folder where this program is saved.
BASE_FOLDER = Path(__file__).resolve().parent

# Set the input file path.
INPUT_FILE = BASE_FOLDER / "input.txt"

# Create the output folder.
OUTPUT_FOLDER = BASE_FOLDER / "output"
OUTPUT_FOLDER.mkdir(exist_ok=True)


def question1(data):
    # Get Question 1 input values.
    section = data["QUESTION1"]

    # Create the x^2 function object.
    rule = TrapezoidalRule(section["function"])

    # Read lower and upper limits.
    a = float(section["a"])
    b = float(section["b"])

    # Read all n values.
    n_values = get_integer_list(section["n_values"])

    # Read the exact integral value.
    exact_value = float(section["exact_value"])

    # Create an empty list for table rows.
    rows = []

    # Create lists for graph values.
    h_values = []
    error_values = []
    approximation_values = []

    # Calculate the result for every n.
    for n in n_values:
        # Calculate h.
        h = rule.step_size(a, b, n)

        # Calculate trapezoidal approximation.
        approximation = rule.integrate(a, b, n)

        # Calculate absolute error.
        error = absolute_error(approximation, exact_value)

        # Store values for the graph.
        h_values.append(h)
        error_values.append(error)
        approximation_values.append(approximation)

        # Store the first result without an order value.
        if len(rows) == 0:
            order = "-"

        # Calculate order after two error values are available.
        else:
            order = f"{estimate_order(error_values[-2], error):.6f}"

        # Add one row to the table.
        rows.append([
            n,
            f"{h:.6f}",
            f"{approximation:.10f}",
            f"{error:.10f}",
            order,
        ])

    # Print Question 1 table.
    print("\nQUESTION 1")
    print("n\th\t\tApproximation\tAbsolute Error\tOrder")
    for row in rows:
        print("\t".join(str(value) for value in row))

    # Perform Richardson extrapolation.
    richardson_rows = []

    # Use consecutive n values for Richardson calculation.
    for i in range(len(n_values) - 1):
        # Get old and new trapezoidal results.
        old_result = approximation_values[i]
        new_result = approximation_values[i + 1]

        # Calculate Richardson result.
        richardson = richardson_extrapolation(old_result, new_result)

        # Calculate its error.
        richardson_error = absolute_error(richardson, exact_value)

        # Store Richardson values.
        richardson_rows.append([
            n_values[i],
            n_values[i + 1],
            f"{richardson:.10f}",
            f"{richardson_error:.10f}",
        ])

    # Save the main Question 1 table.
    save_csv(
        OUTPUT_FOLDER / "question1_table.csv",
        ["n", "h", "Approximation", "Absolute Error", "Order"],
        rows,
    )

    # Save Richardson table.
    save_csv(
        OUTPUT_FOLDER / "question1_richardson.csv",
        ["Old n", "New n", "Richardson Value", "Richardson Error"],
        richardson_rows,
    )

    # Create the Question 1 graph.
    make_q1_graph(
        h_values,
        error_values,
        OUTPUT_FOLDER / "question1_error_graph.png",
    )

    # Return values for the final report.
    return rows, richardson_rows


def question2(data):
    # Get Question 2 input values.
    section = data["QUESTION2"]

    # Create the e^(-x^2) function object.
    rule = TrapezoidalRule(section["function"])

    # Read lower and upper limits.
    a = float(section["a"])
    b = float(section["b"])

    # Read n values.
    n_values = get_integer_list(section["n_values"])

    # Read the reference value.
    reference_value = float(section["reference_value"])

    # Create an empty result table.
    rows = []

    # Create a list for graph approximations.
    approximation_values = []

    # Calculate each approximation.
    for n in n_values:
        # Calculate h.
        h = rule.step_size(a, b, n)

        # Calculate numerical integral.
        approximation = rule.integrate(a, b, n)

        # Calculate error from reference value.
        error = absolute_error(approximation, reference_value)

        # Store approximation for the graph.
        approximation_values.append(approximation)

        # Add result to the table.
        rows.append([
            n,
            f"{h:.6f}",
            f"{approximation:.10f}",
            f"{error:.10f}",
        ])

    # Print Question 2 table.
    print("\nQUESTION 2")
    print("n\th\t\tApproximation\tAbsolute Error")
    for row in rows:
        print("\t".join(str(value) for value in row))

    # Save Question 2 table.
    save_csv(
        OUTPUT_FOLDER / "question2_table.csv",
        ["n", "h", "Approximation", "Absolute Error"],
        rows,
    )

    # Create Question 2 graph.
    make_q2_graph(
        n_values,
        approximation_values,
        reference_value,
        OUTPUT_FOLDER / "question2_graph.png",
    )

    # Return the table.
    return rows


def question3(data):
    # Get Question 3 input values.
    section = data["QUESTION3"]

    # Read x values from the file.
    x_values = get_number_list(section["x_values"])

    # Read f(x) values from the file.
    f_values = get_number_list(section["f_values"])

    # Use the first and last x values as limits.
    a = x_values[0]
    b = x_values[-1]

    # Calculate the number of intervals.
    n = len(x_values) - 1

    # Calculate the step size.
    h = (b - a) / n

    # Start the trapezoidal sum.
    total = 0.5 * (f_values[0] + f_values[-1])

    # Add all middle values.
    for value in f_values[1:-1]:
        total = total + value

    # Calculate the integral.
    approximation = h * total

    # Print Question 3 table.
    print("\nQUESTION 3")
    print("x\t\tf(x)")
    for x, value in zip(x_values, f_values):
        print(f"{x:.2f}\t\t{value:.2f}")

    # Print the final answer.
    print(f"Trapezoidal integral = {approximation:.10f}")

    # Save Question 3 data.
    save_csv(
        OUTPUT_FOLDER / "question3_table.csv",
        ["x", "f(x)"],
        [[x, value] for x, value in zip(x_values, f_values)],
    )

    # Create Question 3 graph.
    make_q3_graph(
        x_values,
        f_values,
        OUTPUT_FOLDER / "question3_graph.png",
    )

    # Return the answer.
    return approximation


def main():
    # Read all input from input.txt.
    data = read_input_file(INPUT_FILE)

    # Run Question 1.
    q1_rows, richardson_rows = question1(data)

    # Run Question 2.
    q2_rows = question2(data)

    # Run Question 3.
    q3_answer = question3(data)

    # Create a simple final report.
    report = []
    report.append("ASSIGNMENT 7 - COMPOSITE TRAPEZOIDAL RULE")
    report.append("=" * 50)
    report.append("")
    report.append("Question 1 exact value = 2.666666666666667")
    report.append("Question 1 shows that the trapezoidal rule has approximately second-order accuracy.")
    report.append("Richardson extrapolation gives a much better result.")
    report.append("")
    report.append("Question 2 reference value = 0.746824132812427")
    report.append("Increasing n gives smaller errors for this example.")
    report.append("")
    report.append(f"Question 3 estimated integral = {q3_answer:.10f}")
    report.append("")
    report.append("Generated files are available in the output folder.")

    # Save the final report.
    save_text(
        OUTPUT_FOLDER / "final_report.txt",
        "\n".join(report),
    )

    # Tell the student that the program finished.
    print("\nAll questions completed.")
    print("Check the output folder for tables, graphs and the final report.")


# Run main only when this file is executed directly.
if __name__ == "__main__":
    main()

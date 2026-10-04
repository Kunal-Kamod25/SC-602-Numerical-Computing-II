# Assignment 8: Simpson 1/3 and Simpson 3/8 Rules.
# This is the main file of the program.

from pathlib import Path

# Import both Simpson classes.
from algorithms import (
    SimpsonOneThird,
    SimpsonThreeEighth,
    absolute_error,
    estimate_order,
)

# Import input, output and graph functions.
from functions import (
    read_input_file,
    get_number_list,
    get_integer_list,
    save_csv,
    save_text,
    make_error_graph,
    make_comparison_graph,
    make_data_graph,
)


# Get the folder where this file is located.
BASE_FOLDER = Path(__file__).resolve().parent

# Create input folders and set file path.
INPUT_FOLDER = BASE_FOLDER / "input"
INPUT_FOLDER.mkdir(exist_ok=True)

INPUT_13_FOLDER = INPUT_FOLDER / "simpson_1_3rd"
INPUT_13_FOLDER.mkdir(exist_ok=True)

INPUT_38_FOLDER = INPUT_FOLDER / "simpson_3_8th"
INPUT_38_FOLDER.mkdir(exist_ok=True)

INPUT_FILE = INPUT_FOLDER / "input.txt"

# Create output folders.
OUTPUT_FOLDER = BASE_FOLDER / "output"
OUTPUT_FOLDER.mkdir(exist_ok=True)

OUTPUT_13_FOLDER = OUTPUT_FOLDER / "simpson_1_3rd"
OUTPUT_13_FOLDER.mkdir(exist_ok=True)

OUTPUT_38_FOLDER = OUTPUT_FOLDER / "simpson_3_8th"
OUTPUT_38_FOLDER.mkdir(exist_ok=True)


def run_method(rule, a, b, n_values, exact_value):
    # Create an empty result table.
    rows = []

    # Store graph values.
    h_values = []
    error_values = []
    approximation_values = []

    # Calculate each n value.
    for n in n_values:
        # Calculate h.
        h = rule.step_size(a, b, n)

        # Calculate Simpson approximation.
        approximation = rule.integrate(a, b, n)

        # Calculate absolute error.
        error = absolute_error(approximation, exact_value)

        # Store graph values.
        h_values.append(h)
        error_values.append(error)
        approximation_values.append(approximation)

        # Calculate experimental order after the first result.
        if len(error_values) == 1:
            order = "-"

        # If both errors are almost zero, the function is integrated
        # exactly for the given test case, so order is not meaningful.
        elif error_values[-2] < 1e-14 or error < 1e-14:
            order = "Exact"

        else:
            # Simpson rules are fourth-order accurate.
            order = f"{estimate_order(error_values[-2], error):.6f}"

        # Add the row.
        rows.append([
            n,
            f"{h:.6f}",
            f"{approximation:.10f}",
            f"{error:.10f}",
            order,
        ])

    # Return all calculated values.
    return rows, h_values, error_values, approximation_values


def print_table(title, rows, show_order=True):
    # Print the table title.
    print("\n" + title)

    # Print headings.
    if show_order:
        print("n\th\t\tApproximation\tAbsolute Error\tOrder")

    else:
        print("n\th\t\tApproximation\tAbsolute Error")

    # Print each row.
    for row in rows:
        print("\t".join(str(value) for value in row))


def question1(data):
    # Get Question 1 data.
    section = data["QUESTION1"]

    # Read limits.
    a = float(section["a"])
    b = float(section["b"])

    # Read n values for both methods.
    n_values_13 = get_integer_list(section["n_values_13"])
    n_values_38 = get_integer_list(section["n_values_38"])

    # Read exact value.
    exact_value = float(section["exact_value"])

    # Create the two OOP objects.
    rule_13 = SimpsonOneThird(section["function"])
    rule_38 = SimpsonThreeEighth(section["function"])

    # Run Simpson 1/3.
    rows_13, h_13, errors_13, values_13 = run_method(
        rule_13, a, b, n_values_13, exact_value
    )

    # Run Simpson 3/8.
    rows_38, h_38, errors_38, values_38 = run_method(
        rule_38, a, b, n_values_38, exact_value
    )

    # Print both tables.
    print_table("QUESTION 1 - SIMPSON 1/3", rows_13)
    print_table("QUESTION 1 - SIMPSON 3/8", rows_38)

    # Save both tables.
    save_csv(
        OUTPUT_13_FOLDER / "question1_simpson_13.csv",
        ["n", "h", "Approximation", "Absolute Error", "Order"],
        rows_13,
    )

    save_csv(
        OUTPUT_38_FOLDER / "question1_simpson_38.csv",
        ["n", "h", "Approximation", "Absolute Error", "Order"],
        rows_38,
    )

    # Create error graphs.
    make_error_graph(
        h_13,
        errors_13,
        "Question 1: Simpson 1/3 Error",
        OUTPUT_13_FOLDER / "question1_simpson_13_error.png",
    )

    make_error_graph(
        h_38,
        errors_38,
        "Question 1: Simpson 3/8 Error",
        OUTPUT_38_FOLDER / "question1_simpson_38_error.png",
    )

    # Create a comparison graph.
    make_comparison_graph(
        n_values_13,
        values_13,
        n_values_38,
        values_38,
        exact_value,
        OUTPUT_FOLDER / "question1_comparison.png",
    )

    # Return results.
    return rows_13, rows_38


def question2(data):
    # Get Question 2 data.
    section = data["QUESTION2"]

    # Read limits.
    a = float(section["a"])
    b = float(section["b"])

    # Read n values.
    n_values_13 = get_integer_list(section["n_values_13"])
    n_values_38 = get_integer_list(section["n_values_38"])

    # Read reference value.
    reference_value = float(section["reference_value"])

    # Create Simpson objects.
    rule_13 = SimpsonOneThird(section["function"])
    rule_38 = SimpsonThreeEighth(section["function"])

    # Run both methods.
    rows_13, h_13, errors_13, values_13 = run_method(
        rule_13, a, b, n_values_13, reference_value
    )

    rows_38, h_38, errors_38, values_38 = run_method(
        rule_38, a, b, n_values_38, reference_value
    )

    # Print tables.
    print_table("QUESTION 2 - SIMPSON 1/3", rows_13)
    print_table("QUESTION 2 - SIMPSON 3/8", rows_38)

    # Save tables.
    save_csv(
        OUTPUT_13_FOLDER / "question2_simpson_13.csv",
        ["n", "h", "Approximation", "Absolute Error", "Order"],
        rows_13,
    )

    save_csv(
        OUTPUT_38_FOLDER / "question2_simpson_38.csv",
        ["n", "h", "Approximation", "Absolute Error", "Order"],
        rows_38,
    )

    # Create error graphs.
    make_error_graph(
        h_13,
        errors_13,
        "Question 2: Simpson 1/3 Error",
        OUTPUT_13_FOLDER / "question2_simpson_13_error.png",
    )

    make_error_graph(
        h_38,
        errors_38,
        "Question 2: Simpson 3/8 Error",
        OUTPUT_38_FOLDER / "question2_simpson_38_error.png",
    )

    # Create comparison graph.
    make_comparison_graph(
        n_values_13,
        values_13,
        n_values_38,
        values_38,
        reference_value,
        OUTPUT_FOLDER / "question2_comparison.png",
    )

    # Return results.
    return rows_13, rows_38


def question3(data):
    # Get Question 3 data.
    section = data["QUESTION3"]

    # Read x and f(x) values.
    x_values = get_number_list(section["x_values"])
    f_values = get_number_list(section["f_values"])

    # Calculate number of intervals.
    n = len(x_values) - 1

    # Calculate h.
    h = x_values[1] - x_values[0]

    # Simpson 1/3 works because n = 4 is even.
    rule_13 = SimpsonOneThird("x^2")

    # Use the given f(x) values directly for data integration.
    total_13 = f_values[0] + f_values[-1]

    # Add Simpson 1/3 middle terms.
    for i in range(1, n):
        # Odd index has weight 4.
        if i % 2 == 1:
            total_13 = total_13 + 4 * f_values[i]

        # Even index has weight 2.
        else:
            total_13 = total_13 + 2 * f_values[i]

    # Calculate Simpson 1/3 result.
    answer_13 = (h / 3) * total_13

    # Simpson 3/8 requires n to be a multiple of 3.
    # Here n = 4, so pure 3/8 cannot cover the complete 0 to 2 interval.
    # We therefore clearly report that restriction instead of giving
    # an incorrect full-interval Simpson 3/8 result.
    answer_38 = None

    # Print the data table.
    print("\nQUESTION 3 - GIVEN DATA")
    print("x\t\tf(x)")
    for x, value in zip(x_values, f_values):
        print(f"{x:.2f}\t\t{value:.2f}")

    # Print Simpson 1/3 answer.
    print(f"Simpson 1/3 integral = {answer_13:.10f}")

    # Explain the Simpson 3/8 restriction.
    print("Simpson 3/8: n = 4 is not a multiple of 3, so pure 3/8 cannot")
    print("be directly applied to the complete interval [0, 2].")

    # Save data table.
    save_csv(
        OUTPUT_FOLDER / "question3_data.csv",
        ["x", "f(x)"],
        [[x, value] for x, value in zip(x_values, f_values)],
    )

    # Save Question 3 explanation.
    save_text(
        OUTPUT_FOLDER / "question3_note.txt",
        "Simpson 1/3 result = "
        + f"{answer_13:.10f}"
        + "\n\nSimpson 3/8 requires n to be a multiple of 3. "
        + "The given data has n = 4 intervals, so pure Simpson 3/8 "
        + "cannot be directly applied over the complete interval [0, 2].",
    )

    # Create data graph.
    make_data_graph(
        x_values,
        f_values,
        OUTPUT_FOLDER / "question3_data_graph.png",
    )

    # Return results.
    return answer_13, answer_38


def main():
    # Read all input values.
    data = read_input_file(INPUT_FILE)

    # Run Question 1.
    q1_13, q1_38 = question1(data)

    # Run Question 2.
    q2_13, q2_38 = question2(data)

    # Run Question 3.
    q3_13, q3_38 = question3(data)

    # Create final report text.
    report = []
    report.append("ASSIGNMENT 8 - SIMPSON 1/3 AND SIMPSON 3/8 RULES")
    report.append("=" * 55)
    report.append("")
    report.append("Simpson 1/3 rule requires an even number of intervals.")
    report.append("Simpson 3/8 rule requires the number of intervals to be a multiple of 3.")
    report.append("")
    report.append("Both Simpson rules have approximately fourth-order accuracy, O(h^4).")
    report.append("")
    report.append("Question 1 uses f(x) = x^2 and exact value 2.666666666666667.")
    report.append("Question 2 uses f(x) = exp(-x^2) and reference value 0.746824132812427.")
    report.append("")
    report.append(f"Question 3 Simpson 1/3 result = {q3_13:.10f}")
    report.append("Question 3 pure Simpson 3/8 is not directly applicable because n = 4.")
    report.append("")
    report.append("All tables and graphs are available in the output folder.")

    # Save final report.
    save_text(
        OUTPUT_FOLDER / "final_report.txt",
        "\n".join(report),
    )

    # Show completion message.
    print("\nAll questions completed.")
    print("Check the output folder for tables, graphs and final_report.txt.")


# Run main when this file is executed.
if __name__ == "__main__":
    main()

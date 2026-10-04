# This file contains simple input, output and graph functions.

import csv


def read_input_file(file_name: str) -> dict:
    # Create an empty dictionary for storing input values.
    data = {}

    # Store the current section name.
    section = None

    # Open the input file.
    with open(file_name, "r", encoding="utf-8") as file:
        # Read the file one line at a time.
        for line in file:
            # Remove extra spaces and the newline character.
            line = line.strip()

            # Ignore empty lines and comments.
            if not line or line.startswith("#"):
                continue

            # Check whether the line is a section name.
            if line.startswith("[") and line.endswith("]"):
                section = line[1:-1]

                # Create a dictionary for this section.
                data[section] = {}
                continue

            # Split normal input lines into key and value.
            key, value = line.split("=", 1)

            # Remove unnecessary spaces.
            key = key.strip()
            value = value.strip()

            # Store the value in the current section.
            data[section][key] = value

    # Return all input data.
    return data


def get_number_list(value: str) -> list:
    # Convert comma-separated values into a list of numbers.
    return [float(item.strip()) for item in value.split(",")]


def get_integer_list(value: str) -> list:
    # Convert comma-separated values into a list of integers.
    return [int(item.strip()) for item in value.split(",")]


def save_csv(file_name: str, headers: list, rows: list) -> None:
    # Open the CSV file for writing.
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        # Create a CSV writer.
        writer = csv.writer(file)

        # Write the column headings.
        writer.writerow(headers)

        # Write all result rows.
        writer.writerows(rows)


def save_text(file_name: str, text: str) -> None:
    # Open the text output file.
    with open(file_name, "w", encoding="utf-8") as file:
        # Write the given text.
        file.write(text)


def make_q1_graph(h_values: list, error_values: list, file_name: str) -> None:
    # Import matplotlib here so the main program stays simple.
    import matplotlib.pyplot as plt

    # Create a new graph.
    plt.figure()

    # Plot error against step size.
    plt.loglog(h_values, error_values, "o-", label="Absolute Error")

    # Add graph title.
    plt.title("Question 1: Error vs Step Size")

    # Add x-axis label.
    plt.xlabel("Step size h")

    # Add y-axis label.
    plt.ylabel("Absolute Error")

    # Show grid.
    plt.grid(True)

    # Show legend.
    plt.legend()

    # Save the graph.
    plt.savefig(file_name, dpi=200, bbox_inches="tight")

    # Close the graph.
    plt.close()


def make_q2_graph(n_values: list, approximation_values: list, reference_value: float, file_name: str) -> None:
    # Import matplotlib here.
    import matplotlib.pyplot as plt

    # Create a new graph.
    plt.figure()

    # Plot numerical values.
    plt.plot(n_values, approximation_values, "o-", label="Trapezoidal Approximation")

    # Plot reference value as a horizontal line.
    plt.axhline(reference_value, linestyle="--", label="Reference Value")

    # Add graph title.
    plt.title("Question 2: Approximation vs n")

    # Add x-axis label.
    plt.xlabel("Number of intervals n")

    # Add y-axis label.
    plt.ylabel("Integral value")

    # Show grid.
    plt.grid(True)

    # Show legend.
    plt.legend()

    # Save the graph.
    plt.savefig(file_name, dpi=200, bbox_inches="tight")

    # Close the graph.
    plt.close()


def make_q3_graph(x_values: list, f_values: list, file_name: str) -> None:
    # Import matplotlib here.
    import matplotlib.pyplot as plt

    # Create a new graph.
    plt.figure()

    # Plot the given experimental data.
    plt.plot(x_values, f_values, "o-", label="Given Data")

    # Add graph title.
    plt.title("Question 3: Experimental Data")

    # Add x-axis label.
    plt.xlabel("x")

    # Add y-axis label.
    plt.ylabel("f(x)")

    # Show grid.
    plt.grid(True)

    # Show legend.
    plt.legend()

    # Save the graph.
    plt.savefig(file_name, dpi=200, bbox_inches="tight")

    # Close the graph.
    plt.close()

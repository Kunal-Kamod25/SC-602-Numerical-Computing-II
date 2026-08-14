# main.py
#
# Why this file exists:
# This is the starting point of the whole project. It just shows
# a menu, asks the user what they want to do, and then calls the
# right functions from the "modules" folder to actually do the work.
#
# We are keeping this file simple on purpose. All the "real" logic
# (math, file reading, graph drawing, etc.) is written inside the
# modules folder. main.py should mostly just be doing:
#   1) show menu
#   2) get input file
#   3) call the classes
#   4) show/save result

from pathlib import Path

from modules.file_handler import FileHandler
from modules.interpolation import LagrangeInterpolation
from modules.validator import Validator
from modules.graph_plotter import GraphPlotter
from modules import utilities


# Folder locations, kept as constants at the top so they are easy
# to find and change later if needed.
INPUT_FOLDER = Path("data/input")
OUTPUT_FOLDER = Path("data/output")
GRAPH_FOLDER = Path("graphs")


def show_menu():
    # Just prints the menu options for the user.
    utilities.print_separator()
    print("LAGRANGE INTERPOLATION PROJECT")
    utilities.print_separator()
    print("1. Solve Question 1")
    print("2. Solve Question 2")
    print("3. Solve Question 3")
    print("4. Solve Question 4")
    print("5. Solve Question 5")
    print("6. Solve Custom Input")
    print("7. Exit")
    utilities.print_separator()


def get_question_files(choice):
    # Depending on the menu choice, decides which input file and
    # output file names to use, and what to call this question in
    # the graph title.
    question_map = {
        "1": ("question1.txt", "output_question1.txt", "question1.png", "Question 1"),
        "2": ("question2.txt", "output_question2.txt", "question2.png", "Question 2"),
        "3": ("question3.txt", "output_question3.txt", "question3.png", "Question 3"),
        "4": ("question4.txt", "output_question4.txt", "question4.png", "Question 4"),
        "5": ("question5.txt", "output_question5.txt", "question5.png", "Question 5"),
        "6": ("custom.txt", "output_custom.txt", "custom.png", "Custom Input"),
    }
    return question_map[choice]


def build_output_report(x_values, y_values, points, results, basis_check,
                         polynomial_object, time_taken, question_name):
    # Builds the list of lines that will be written into the
    # output text file. Keeping this as its own function so
    # run_question() does not become too long and messy.

    lines = []
    lines.append("LAGRANGE INTERPOLATION - RESULT REPORT")
    lines.append(f"Question: {question_name}")
    lines.append(f"Date/Time: {utilities.get_current_datetime_string()}")
    lines.append("")

    lines.append("INPUT DATA")
    lines.append("-" * 30)
    lines.append(f"Number of points: {len(x_values)}")
    for i in range(len(x_values)):
        lines.append(f"  x[{i}] = {x_values[i]}, y[{i}] = {y_values[i]}")
    lines.append("")

    lines.append("BASIS POLYNOMIAL VERIFICATION")
    lines.append("-" * 30)
    lines.append("(Checking that L_i(x_i) = 1, as per theory)")
    for i, j, value in basis_check:
        lines.append(f"  L_{i}(x_{i}) = {value}")
    lines.append("")

    if polynomial_object is not None:
        lines.append("INTERPOLATION POLYNOMIAL")
        lines.append("-" * 30)
        lines.append(str(polynomial_object))
        lines.append("")
    else:
        lines.append("INTERPOLATION POLYNOMIAL")
        lines.append("-" * 30)
        lines.append("Too many points to display full polynomial expression.")
        lines.append("(Numeric estimation was still done using the full dataset.)")
        lines.append("")

    lines.append("ESTIMATED VALUES")
    lines.append("-" * 30)
    for point, value in zip(points, results):
        lines.append(f"  f({point}) = {value}")
    lines.append("")

    lines.append("PERFORMANCE")
    lines.append("-" * 30)
    lines.append(f"Time taken: {time_taken} seconds")
    lines.append("")

    lines.append("Program finished successfully.")

    return lines


def run_question(choice):
    # This function does the full pipeline for one question:
    # read input -> validate -> calculate -> save output -> draw graph

    input_file_name, output_file_name, graph_file_name, question_name = get_question_files(choice)

    input_path = INPUT_FOLDER / input_file_name
    output_path = OUTPUT_FOLDER / output_file_name
    graph_path = GRAPH_FOLDER / graph_file_name
    csv_path = OUTPUT_FOLDER / "graph_data.csv"

    file_handler = FileHandler()
    validator = Validator()
    plotter = GraphPlotter()

    start_time = utilities.start_timer()

    # Step 1: Read the input file
    x_values, y_values, points = file_handler.read_input_file(input_path)

    # Step 2: Validate the data before doing any math on it
    validator.validate_all(x_values, y_values, points)

    # Step 3: Do the actual interpolation
    interpolator = LagrangeInterpolation(x_values, y_values)

    results = []
    for point in points:
        estimated_value = interpolator.estimate(point)
        results.append(utilities.format_number(estimated_value))

    basis_check = interpolator.verify_basis_property()
    polynomial_object = interpolator.build_polynomial()

    time_taken = utilities.stop_timer(start_time)

    # Step 4: Save results to output text file
    report_lines = build_output_report(
        x_values, y_values, points, results, basis_check,
        polynomial_object, time_taken, question_name
    )
    file_handler.write_output_file(output_path, report_lines)

    # Step 5: Draw and save the graph (using the first point as the
    # highlighted "estimated point" star on the graph)
    curve_x, curve_y = plotter.plot_and_save(
        interpolator, points[0], results[0], question_name, graph_path
    )
    file_handler.save_graph_data_csv(csv_path, x_values, y_values, curve_x, curve_y)

    # Step 6: Print a short summary to the screen too
    utilities.print_separator()
    print(f"{question_name} solved successfully!")
    for point, value in zip(points, results):
        print(f"  f({point}) = {value}")
    print(f"Time taken: {time_taken} seconds")
    utilities.print_separator()


def create_custom_input_file():
    # Lets the user type their own dataset, and saves it into
    # data/input/custom.txt in the same format the program expects.
    # Then run_question("6") can read it just like any other file.

    print("Enter your custom dataset.")

    try:
        n = int(input("How many data points do you have? "))
    except ValueError:
        print("Please enter a valid whole number.")
        return

    if n < 2:
        print("You need at least 2 points for interpolation.")
        return

    lines_to_save = [str(n)]

    for i in range(n):
        pair = input(f"Enter x{i} and y{i} (space separated, e.g. 1 2.5): ")
        lines_to_save.append(pair.strip())

    points_input = input("Enter the point(s) you want to estimate (space separated if more than one): ")
    points_list = points_input.strip().split()
    lines_to_save.extend(points_list)

    custom_path = INPUT_FOLDER / "custom.txt"
    with open(custom_path, "w") as file:
        for line in lines_to_save:
            file.write(line + "\n")

    print(f"Custom input saved to {custom_path}")


def main():
    # This is where the program actually starts running.
    # Keeps asking for menu choice until user picks "Exit".

    while True:
        show_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "7":
            print("Thank you for using the program. Goodbye!")
            break

        elif choice in ("1", "2", "3", "4", "5"):
            try:
                run_question(choice)
            except Exception as error:
                # Catching any error here so one bad input does not
                # crash the whole program, user can just try again.
                print(f"Error: {error}")

        elif choice == "6":
            try:
                create_custom_input_file()
                run_question("6")
            except Exception as error:
                print(f"Error: {error}")

        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


# This makes sure main() only runs when we execute this file
# directly, and not when it gets imported somewhere else.
if __name__ == "__main__":
    main()

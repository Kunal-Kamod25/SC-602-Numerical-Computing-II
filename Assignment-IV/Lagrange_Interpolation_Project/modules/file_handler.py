# file_handler.py
#
# Why this file exists:
# The program has to read data from input .txt files and also
# write the results into output .txt files. All of that file
# reading/writing code is kept in one place here, so main.py
# stays clean and easy to read.

import csv
from pathlib import Path


class FileHandler:
    """
    Handles everything related to files:
    - reading the input data files
    - writing the output result files
    - saving graph data as a csv file
    """

    def read_input_file(self, file_path):
        # Reads the input file and returns x values, y values
        # and a LIST of points we want to estimate. We allow more
        # than one point per file because some questions in the
        # assignment ask us to estimate more than one value
        # (like f(2.5) AND f(3.5) in Question 2).
        #
        # Expected file format:
        #   line 1              -> number of data points (n)
        #   next n lines        -> "x y" pairs, space separated
        #   remaining lines     -> one or more points to interpolate

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")

        with open(path, "r") as file:
            # Reading all lines and removing empty lines / spaces
            lines = [line.strip() for line in file.readlines() if line.strip() != ""]

        if len(lines) == 0:
            raise ValueError("Input file is empty.")

        try:
            number_of_points = int(lines[0])
        except ValueError:
            raise ValueError("First line of input file must be a number (count of points).")

        # We need: 1 line for count + n lines for data + at least 1 line for a point
        expected_lines = 1 + number_of_points + 1
        if len(lines) < expected_lines:
            raise ValueError("Input file format is wrong. Not enough data lines given.")

        x_values = []
        y_values = []

        # Reading the x y pairs, line by line
        for i in range(1, number_of_points + 1):
            parts = lines[i].split()
            if len(parts) != 2:
                raise ValueError(f"Line {i+1} in input file should have exactly 2 numbers (x and y).")
            try:
                x_val = float(parts[0])
                y_val = float(parts[1])
            except ValueError:
                raise ValueError(f"Line {i+1} in input file has non-numeric data.")

            x_values.append(x_val)
            y_values.append(y_val)

        # All the remaining lines (could be 1 or more) are points
        # that we need to estimate f(x) for.
        points_to_estimate = []
        remaining_lines = lines[number_of_points + 1:]

        for line in remaining_lines:
            try:
                points_to_estimate.append(float(line))
            except ValueError:
                raise ValueError(f"'{line}' is not a valid number for the point to estimate.")

        if len(points_to_estimate) == 0:
            raise ValueError("No point to estimate was given at the end of the file.")

        return x_values, y_values, points_to_estimate

    def write_output_file(self, file_path, content_lines):
        # content_lines is just a list of strings, each string is
        # one line of the report. We join them and write to file.
        # Using "w" mode means it automatically overwrites the
        # old output file every time, as required.
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as file:
            for line in content_lines:
                file.write(line + "\n")

        print(f"Output saved to: {file_path}")

    def save_graph_data_csv(self, file_path, x_values, y_values, curve_x, curve_y):
        # Saves the original points and the interpolation curve
        # points into a csv file, so it can be opened in Excel or
        # used again later without recalculating everything.
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["type", "x", "y"])

            for x_val, y_val in zip(x_values, y_values):
                writer.writerow(["original_point", x_val, y_val])

            for x_val, y_val in zip(curve_x, curve_y):
                writer.writerow(["curve_point", x_val, y_val])

        print(f"Graph data saved to: {file_path}")

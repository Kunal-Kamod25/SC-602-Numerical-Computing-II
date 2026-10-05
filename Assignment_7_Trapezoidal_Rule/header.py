# This file contains the function declarations used in the program.

from typing import List, Tuple


# Read all values from the input text file.
def read_input_file(file_name: str) -> dict:
    pass


# Run the trapezoidal rule for one value of n.
def trapezoidal_rule(func, a: float, b: float, n: int) -> float:
    pass


# Calculate the absolute error.
def absolute_error(approximation: float, exact_value: float) -> float:
    pass


# Estimate the order of accuracy.
def estimate_order(error_old: float, error_new: float) -> float:
    pass





# Save a list of rows as a CSV table.
def save_csv(file_name: str, headers: List[str], rows: List[list]) -> None:
    pass


# Save normal text output.
def save_text(file_name: str, text: str) -> None:
    pass

# This file contains the main numerical algorithm class.

import math


class TrapezoidalRule:
    # This class performs numerical integration using the trapezoidal rule.

    def __init__(self, function_name: str):
        # Store the name of the function.
        self.function_name = function_name

    def function_value(self, x: float) -> float:
        # Calculate f(x) according to the selected function.
        if self.function_name == "x^2":
            # Return x squared for Question 1.
            return x ** 2

        if self.function_name == "exp(-x^2)":
            # Return e^(-x^2) for Question 2.
            return math.exp(-(x ** 2))

        # Stop if an unknown function is given.
        raise ValueError("Function is not available.")

    def integrate(self, a: float, b: float, n: int) -> float:
        # Calculate the step size.
        h = (b - a) / n

        # Start the sum with half of the first value.
        total = 0.5 * self.function_value(a)

        # Add all the middle points.
        for i in range(1, n):
            # Calculate the current x value.
            x = a + i * h

            # Add the function value at this point.
            total = total + self.function_value(x)

        # Add half of the last function value.
        total = total + 0.5 * self.function_value(b)

        # Multiply the sum by h and return the answer.
        return h * total

    def step_size(self, a: float, b: float, n: int) -> float:
        # Calculate and return h.
        return (b - a) / n


def absolute_error(approximation: float, exact_value: float) -> float:
    # Calculate the absolute difference.
    return abs(exact_value - approximation)


def estimate_order(error_old: float, error_new: float) -> float:
    # Avoid division by zero.
    if error_new == 0:
        return float("inf")

    # Estimate p using E(h) / E(h/2) = 2^p.
    return math.log(error_old / error_new, 2)




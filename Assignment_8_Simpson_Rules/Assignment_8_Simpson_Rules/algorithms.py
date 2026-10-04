# This file contains the numerical algorithms using simple OOP classes.

import math


class Simpson:
    # Base class for Simpson numerical integration rules.

    def __init__(self, function_name: str):
        # Store the function name.
        self.function_name = function_name

    def function_value(self, x: float) -> float:
        # Calculate the selected function value.

        if self.function_name == "x^2":
            # Return x squared.
            return x ** 2

        if self.function_name == "exp(-x^2)":
            # Return e^(-x^2).
            return math.exp(-(x ** 2))

        # Show an error for an unknown function.
        raise ValueError("Function is not available.")

    def step_size(self, a: float, b: float, n: int) -> float:
        # Calculate h.
        return (b - a) / n


class SimpsonOneThird(Simpson):
    # This class performs numerical integration using Simpson 1/3 rule.

    def integrate(self, a: float, b: float, n: int) -> float:
        # Simpson 1/3 requires an even number of intervals.
        if n % 2 != 0:
            raise ValueError("Simpson 1/3 requires even n.")

        # Calculate step size.
        h = self.step_size(a, b, n)

        # Start with the first and last values.
        total = self.function_value(a) + self.function_value(b)

        # Add all middle points.
        for i in range(1, n):
            # Calculate current x.
            x = a + i * h

            # Odd points have weight 4.
            if i % 2 == 1:
                total = total + 4 * self.function_value(x)

            # Even points have weight 2.
            else:
                total = total + 2 * self.function_value(x)

        # Apply the Simpson 1/3 formula.
        return (h / 3) * total


class SimpsonThreeEighth(Simpson):
    # This class performs numerical integration using Simpson 3/8 rule.

    def integrate(self, a: float, b: float, n: int) -> float:
        # Simpson 3/8 requires n to be a multiple of 3.
        if n % 3 != 0:
            raise ValueError("Simpson 3/8 requires n to be a multiple of 3.")

        # Calculate step size.
        h = self.step_size(a, b, n)

        # Start with the first and last values.
        total = self.function_value(a) + self.function_value(b)

        # Add all middle points.
        for i in range(1, n):
            # Calculate current x.
            x = a + i * h

            # Points divisible by 3 have weight 2.
            if i % 3 == 0:
                total = total + 2 * self.function_value(x)

            # All other middle points have weight 3.
            else:
                total = total + 3 * self.function_value(x)

        # Apply the Simpson 3/8 formula.
        return (3 * h / 8) * total


def absolute_error(approximation: float, exact_value: float) -> float:
    # Return the absolute difference.
    return abs(exact_value - approximation)


def estimate_order(error_old: float, error_new: float, ratio: float = 2) -> float:
    # Avoid division by zero.
    if error_new == 0:
        return float("inf")

    # Calculate the experimental order.
    return math.log(error_old / error_new, ratio)


def simpson_mixed_for_four_intervals(
    values: list,
    h: float,
) -> float:
    # For 4 intervals, pure Simpson 3/8 cannot cover the full interval.
    # We use 3/8 on the first 3 intervals and 1/3 on the last 1 interval.
    first_part = (3 * h / 8) * (
        values[0] + 3 * values[1] + 3 * values[2] + values[3]
    )

    # Simpson 1/3 needs two intervals, so a single final interval cannot
    # be handled by Simpson 1/3 alone. Therefore this function is not used.
    return first_part

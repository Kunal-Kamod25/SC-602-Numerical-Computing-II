# Assignment 9: Numerical Algorithms with Class & Subclass Inheritance
# Base Class: NumericalIntegrator
# Subclasses: TrapezoidalRule, SimpsonOneThird, SimpsonThreeEighth

from typing import List


class NumericalIntegrator:
    # Base class representing a general numerical integration method.
    def __init__(self, name: str, order: str):
        self.name = name
        self.order = order

    def step_size(self, x_values: List[float]) -> float:
        # Calculate step size h assuming uniform spacing.
        if len(x_values) < 2:
            raise ValueError("Need at least 2 points to calculate step size.")
        return x_values[1] - x_values[0]

    def validate_inputs(self, x_values: List[float], y_values: List[float]) -> None:
        # Check that array lengths match and there are enough points.
        if len(x_values) != len(y_values):
            raise ValueError("x and y arrays must have the same length.")
        if len(x_values) < 2:
            raise ValueError("Integration requires at least 2 points.")

    def integrate(self, x_values: List[float], y_values: List[float]) -> float:
        # Base integrate method to be overridden by subclasses.
        raise NotImplementedError("Subclasses must implement integrate().")


class TrapezoidalRule(NumericalIntegrator):
    # Subclass implementing Composite Trapezoidal Rule.
    # Polynomial: Linear (degree 1)
    # Order: O(h^2)
    def __init__(self):
        super().__init__(name="Trapezoidal Rule", order="O(h^2)")

    def integrate(self, x_values: List[float], y_values: List[float]) -> float:
        self.validate_inputs(x_values, y_values)
        h = self.step_size(x_values)
        n = len(x_values) - 1

        # Endpoints have weight 0.5
        total = 0.5 * (y_values[0] + y_values[-1])

        # All interior points have weight 1.0
        for i in range(1, n):
            total += y_values[i]

        return h * total


class SimpsonOneThird(NumericalIntegrator):
    # Subclass implementing Simpson's 1/3 Rule.
    # Polynomial: Quadratic (degree 2 parabolas)
    # Order: O(h^4)
    # Requirement: Number of intervals n must be even.
    def __init__(self):
        super().__init__(name="Simpson 1/3 Rule", order="O(h^4)")

    def integrate(self, x_values: List[float], y_values: List[float]) -> float:
        self.validate_inputs(x_values, y_values)
        n = len(x_values) - 1

        # Check even intervals requirement
        if n % 2 != 0:
            raise ValueError(
                f"Simpson's 1/3 rule requires an even number of intervals. Given n = {n}."
            )

        h = self.step_size(x_values)

        # Endpoints have weight 1
        total = y_values[0] + y_values[-1]

        # Odd indices have weight 4, even interior indices have weight 2
        for i in range(1, n):
            if i % 2 == 1:
                total += 4 * y_values[i]
            else:
                total += 2 * y_values[i]

        return (h / 3.0) * total


class SimpsonThreeEighth(NumericalIntegrator):
    # Subclass implementing Simpson's 3/8 Rule.
    # Polynomial: Cubic (degree 3)
    # Order: O(h^4)
    # Requirement: Number of intervals n must be a multiple of 3.
    def __init__(self):
        super().__init__(name="Simpson 3/8 Rule", order="O(h^4)")

    def integrate(self, x_values: List[float], y_values: List[float]) -> float:
        self.validate_inputs(x_values, y_values)
        n = len(x_values) - 1

        # Check multiple of 3 requirement
        if n % 3 != 0:
            raise ValueError(
                f"Simpson's 3/8 rule requires n to be a multiple of 3. Given n = {n}."
            )

        h = self.step_size(x_values)

        # Endpoints have weight 1
        total = y_values[0] + y_values[-1]

        # Indices divisible by 3 have weight 2, others have weight 3
        for i in range(1, n):
            if i % 3 == 0:
                total += 2 * y_values[i]
            else:
                total += 3 * y_values[i]

        return (3.0 * h / 8.0) * total

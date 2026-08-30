"""
functions.py
------------
Defines the test functions used in the assignment, each bundled with its
exact analytical derivative so numerical results can be validated against
ground truth.

OOP Design:
    TestFunction (abstract base class)
        -> ExponentialFunction   : f(x) = e^x
        -> SineFunction          : f(x) = sin(x)
        -> CosineFunction        : f(x) = cos(x)
        -> PolynomialFunction    : f(x) = x^3 - 2x + 1
"""

from abc import ABC, abstractmethod
import math


class TestFunction(ABC):
    """Abstract base class for a scalar test function f(x)."""

    #: Human readable name, overridden by subclasses
    name: str = "TestFunction"

    @abstractmethod
    def evaluate(self, x: float) -> float:
        """Return f(x)."""
        raise NotImplementedError

    @abstractmethod
    def exact_derivative(self, x: float) -> float:
        """Return the exact analytical derivative f'(x)."""
        raise NotImplementedError

    def __call__(self, x: float) -> float:
        return self.evaluate(x)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r}>"


class ExponentialFunction(TestFunction):
    """f(x) = e^x ,  f'(x) = e^x"""

    name = "f(x) = e^x"

    def evaluate(self, x: float) -> float:
        return math.exp(x)

    def exact_derivative(self, x: float) -> float:
        return math.exp(x)


class SineFunction(TestFunction):
    """f(x) = sin(x) ,  f'(x) = cos(x)"""

    name = "f(x) = sin(x)"

    def evaluate(self, x: float) -> float:
        return math.sin(x)

    def exact_derivative(self, x: float) -> float:
        return math.cos(x)


class CosineFunction(TestFunction):
    """f(x) = cos(x) ,  f'(x) = -sin(x)"""

    name = "f(x) = cos(x)"

    def evaluate(self, x: float) -> float:
        return math.cos(x)

    def exact_derivative(self, x: float) -> float:
        return -math.sin(x)


class PolynomialFunction(TestFunction):
    """f(x) = x^3 - 2x + 1 ,  f'(x) = 3x^2 - 2"""

    name = "f(x) = x^3 - 2x + 1"

    def evaluate(self, x: float) -> float:
        return x ** 3 - 2 * x + 1

    def exact_derivative(self, x: float) -> float:
        return 3 * x ** 2 - 2


def get_all_test_functions():
    """Factory helper: returns a list of instances of every test function."""
    return [
        ExponentialFunction(),
        SineFunction(),
        CosineFunction(),
        PolynomialFunction(),
    ]

from __future__ import annotations

from abc import ABC, abstractmethod
import math
from typing import List


class TestFunction(ABC):
    name: str = "TestFunction"

    @abstractmethod
    def evaluate(self, x: float) -> float:
        raise NotImplementedError

    @abstractmethod
    def exact_derivative(self, x: float) -> float:
        raise NotImplementedError


class ExponentialFunction(TestFunction):
    name = "f(x)=e^x"

    def evaluate(self, x: float) -> float:
        return math.exp(x)

    def exact_derivative(self, x: float) -> float:
        return math.exp(x)


class SineFunction(TestFunction):
    name = "f(x)=sin(x)"

    def evaluate(self, x: float) -> float:
        return math.sin(x)

    def exact_derivative(self, x: float) -> float:
        return math.cos(x)


class CosineFunction(TestFunction):
    name = "f(x)=cos(x)"

    def evaluate(self, x: float) -> float:
        return math.cos(x)

    def exact_derivative(self, x: float) -> float:
        return -math.sin(x)


class PolynomialFunction(TestFunction):
    name = "f(x)=x^3-2x+1"

    def evaluate(self, x: float) -> float:
        return x**3 - 2.0 * x + 1.0

    def exact_derivative(self, x: float) -> float:
        return 3.0 * x**2 - 2.0


def get_default_test_functions() -> List[TestFunction]:
    return [ExponentialFunction(), SineFunction(), CosineFunction(), PolynomialFunction()]

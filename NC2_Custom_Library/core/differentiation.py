from __future__ import annotations

from abc import ABC, abstractmethod

from .base_method import NumericalMethod
from .exceptions import InvalidStepSizeError


class DifferentiationMethod(NumericalMethod, ABC):
    name = "DifferentiationMethod"
    order = "O(h^?)"

    @abstractmethod
    def derivative(self, func, x: float, h: float) -> float:
        raise NotImplementedError

    @staticmethod
    def validate_h(h: float) -> None:
        if h <= 0:
            raise InvalidStepSizeError(f"Step size must be positive, got h={h}.")


class FiniteDifference(DifferentiationMethod, ABC):
    pass


class ForwardDifference(FiniteDifference):
    name = "Forward Difference"
    order = "O(h)"

    def derivative(self, func, x: float, h: float) -> float:
        self.validate_h(h)
        return (func(x + h) - func(x)) / h


class BackwardDifference(FiniteDifference):
    name = "Backward Difference"
    order = "O(h)"

    def derivative(self, func, x: float, h: float) -> float:
        self.validate_h(h)
        return (func(x) - func(x - h)) / h


class CentralDifference(FiniteDifference):
    name = "Central Difference"
    order = "O(h^2)"

    def derivative(self, func, x: float, h: float) -> float:
        self.validate_h(h)
        return (func(x + h) - func(x - h)) / (2.0 * h)

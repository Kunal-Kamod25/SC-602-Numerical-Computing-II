"""
differentiation.py
-------------------
Numerical differentiation algorithms implemented as classes.

OOP Design:
    DifferentiationMethod (abstract base class)
        -> CentralDifference          : D(h)  = [f(x+h) - f(x-h)] / (2h)      -> O(h^2)
        -> RichardsonExtrapolation    : R(h)  = [4*D(h/2) - D(h)] / 3         -> O(h^4)

Richardson Extrapolation re-uses a CentralDifference instance internally,
which demonstrates composition (an OOP principle) rather than re-writing
the central-difference formula from scratch.
"""

from abc import ABC, abstractmethod
from .functions import TestFunction


class DifferentiationMethod(ABC):
    """Abstract base class for any numerical differentiation technique."""

    #: Theoretical order of accuracy, e.g. "O(h^2)"
    order: str = "O(h^?)"
    name: str = "DifferentiationMethod"

    @abstractmethod
    def compute(self, func: TestFunction, x: float, h: float) -> float:
        """Return the numerical derivative approximation at point x."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} order={self.order}>"


class CentralDifference(DifferentiationMethod):
    """
    Central Difference formula:
        D(h) = [f(x+h) - f(x-h)] / (2h)
    Leading error term ~ O(h^2).
    """

    order = "O(h^2)"
    name = "Central Difference"

    def compute(self, func: TestFunction, x: float, h: float) -> float:
        if h == 0:
            raise ValueError("Step size h must not be zero.")
        return (func.evaluate(x + h) - func.evaluate(x - h)) / (2.0 * h)


class RichardsonExtrapolation(DifferentiationMethod):
    """
    Richardson Extrapolation applied to the Central Difference formula.

    Central Difference error expansion:
        D(h) = f'(x) + c1*h^2 + c2*h^4 + ...

    Combining D(h) and D(h/2) eliminates the leading h^2 error term:
        R(h) = [4*D(h/2) - D(h)] / 3
    which is accurate to O(h^4).
    """

    order = "O(h^4)"
    name = "Richardson Extrapolation"

    def __init__(self, base_method: DifferentiationMethod = None):
        # Composition: Richardson extrapolation builds on a base method
        # (defaults to Central Difference, as required by the assignment).
        self.base_method = base_method if base_method is not None else CentralDifference()

    def compute(self, func: TestFunction, x: float, h: float) -> float:
        if h == 0:
            raise ValueError("Step size h must not be zero.")
        d_h = self.base_method.compute(func, x, h)
        d_h_half = self.base_method.compute(func, x, h / 2.0)
        return (4.0 * d_h_half - d_h) / 3.0

from __future__ import annotations

from .differentiation import CentralDifference, DifferentiationMethod


class RichardsonExtrapolation(DifferentiationMethod):
    name = "Richardson Extrapolation"
    order = "O(h^4)"

    def __init__(self, base_method: DifferentiationMethod | None = None):
        # Student note: composition + inheritance both are used here.
        self._base_method = base_method if base_method is not None else CentralDifference()

    def derivative(self, func, x: float, h: float) -> float:
        self.validate_h(h)
        d_h = self._base_method.derivative(func, x, h)
        d_h_half = self._base_method.derivative(func, x, h / 2.0)
        return (4.0 * d_h_half - d_h) / 3.0

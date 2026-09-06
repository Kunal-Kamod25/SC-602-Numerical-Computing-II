from __future__ import annotations

from abc import ABC
from typing import Iterable, Sequence

import numpy as np

from .exceptions import MismatchedLengthError


class NumericalMethod(ABC):
    """Common parent for all method classes."""

    def absolute_error(self, exact_values: Sequence[float], approx_values: Sequence[float]) -> np.ndarray:
        exact_arr = np.asarray(exact_values, dtype=float)
        approx_arr = np.asarray(approx_values, dtype=float)
        if exact_arr.shape != approx_arr.shape:
            raise MismatchedLengthError(
                f"Error arrays must match in shape, got {exact_arr.shape} and {approx_arr.shape}."
            )
        return np.abs(exact_arr - approx_arr)

    def max_error(self, exact_values: Sequence[float], approx_values: Sequence[float]) -> float:
        return float(np.max(self.absolute_error(exact_values, approx_values)))

    def relative_error(self, exact_values: Sequence[float], approx_values: Sequence[float]) -> np.ndarray:
        exact_arr = np.asarray(exact_values, dtype=float)
        abs_error = self.absolute_error(exact_values, approx_values)
        # Small epsilon avoids divide-by-zero crash for exact=0.
        safe_denom = np.where(exact_arr == 0.0, 1e-12, np.abs(exact_arr))
        return abs_error / safe_denom

    @staticmethod
    def as_float_array(values: Iterable[float]) -> np.ndarray:
        return np.asarray(list(values), dtype=float)

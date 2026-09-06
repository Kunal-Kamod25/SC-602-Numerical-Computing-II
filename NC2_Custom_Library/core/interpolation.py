from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

import numpy as np
from scipy.interpolate import BarycentricInterpolator

from .base_method import NumericalMethod
from .exceptions import DuplicateXError, InsufficientDataError, MismatchedLengthError


class Interpolator(NumericalMethod, ABC):
    @abstractmethod
    def evaluate(self, x_eval):
        raise NotImplementedError

    @abstractmethod
    def derivative(self, x_eval):
        raise NotImplementedError


class LagrangeInterpolator(Interpolator):
    """Barycentric Lagrange interpolation (stable for larger datasets)."""

    def __init__(self, x_values: Sequence[float], y_values: Sequence[float]):
        self._x = np.asarray(x_values, dtype=float)
        self._y = np.asarray(y_values, dtype=float)
        self._validate_points()
        self._model = BarycentricInterpolator(self._x, self._y)

    def _validate_points(self) -> None:
        if self._x.shape != self._y.shape:
            raise MismatchedLengthError("x and y must be same length.")
        if len(self._x) < 2:
            raise InsufficientDataError("Need at least 2 points.")
        if len(np.unique(self._x)) != len(self._x):
            raise DuplicateXError("Duplicate x values are not allowed.")

    def evaluate(self, x_eval):
        values = self._model(x_eval)
        if np.isscalar(x_eval):
            return float(values)
        return np.asarray(values, dtype=float)

    def derivative(self, x_eval):
        values = self._model.derivative(x_eval, der=1)
        if np.isscalar(x_eval):
            return float(values)
        return np.asarray(values, dtype=float)


class NewtonInterpolator(Interpolator):
    def __init__(self, x_values: Sequence[float], y_values: Sequence[float]):
        self._x = np.asarray(x_values, dtype=float)
        self._y = np.asarray(y_values, dtype=float)
        self._validate_points()
        self._n = len(self._x)
        self._table = np.zeros((self._n, self._n), dtype=float)
        self._coefficients = np.zeros(self._n, dtype=float)
        self._poly_std = None
        self._build_divided_difference_table()

    def _validate_points(self) -> None:
        if self._x.shape != self._y.shape:
            raise MismatchedLengthError("x and y must be same length.")
        if len(self._x) < 2:
            raise InsufficientDataError("Need at least 2 points.")
        if len(np.unique(self._x)) != len(self._x):
            raise DuplicateXError("Duplicate x values are not allowed.")

    def _build_divided_difference_table(self) -> None:
        self._table[:, 0] = self._y
        for col in range(1, self._n):
            for row in range(self._n - col):
                num = self._table[row + 1, col - 1] - self._table[row, col - 1]
                den = self._x[row + col] - self._x[row]
                self._table[row, col] = num / den
        self._coefficients = self._table[0, :].copy()

        poly = np.poly1d([self._coefficients[0]])
        running_prod = np.poly1d([1.0])
        for k in range(1, self._n):
            running_prod *= np.poly1d([1.0, -self._x[k - 1]])
            poly += self._coefficients[k] * running_prod
        self._poly_std = poly

    def get_table(self) -> np.ndarray:
        return self._table.copy()

    def get_coefficients(self) -> np.ndarray:
        return self._coefficients.copy()

    def evaluate(self, x_eval):
        x_eval_arr = np.atleast_1d(np.asarray(x_eval, dtype=float))
        result = np.full_like(x_eval_arr, self._coefficients[0], dtype=float)
        for k in range(1, self._n):
            term = np.full_like(x_eval_arr, self._coefficients[k], dtype=float)
            for j in range(k):
                term *= (x_eval_arr - self._x[j])
            result += term
        if np.isscalar(x_eval):
            return float(result[0])
        return result

    def derivative(self, x_eval):
        dpoly = np.polyder(self._poly_std)
        values = dpoly(x_eval)
        if np.isscalar(x_eval):
            return float(values)
        return np.asarray(values, dtype=float)

"""
interpolator.py

Migrated NewtonInterpolator from core/ into the toolkit.
Added OOP checks to throw specific NewtonToolkitErrors on bad data.
"""

import numpy as np
from .exceptions import InsufficientDataError, MismatchedLengthError, DuplicateXError

class NewtonInterpolator:
    def __init__(self, x, y):
        # OOP exception handling built-in!
        if len(x) != len(y):
            raise MismatchedLengthError(f"Length mismatch: {len(x)} x-values vs {len(y)} y-values.")
        if len(x) < 2:
            raise InsufficientDataError("Need at least 2 points to interpolate.")
        if len(set(x)) != len(x):
            raise DuplicateXError("Duplicate x-values detected in the dataset.")
            
        self.x = np.array(x, dtype=float)
        self.y = np.array(y, dtype=float)
        self.n = len(self.x)
        self.table = None
        self.coeffs = None
        self._build_table()

    def _build_table(self):
        n = self.n
        table = np.zeros((n, n))
        table[:, 0] = self.y

        for j in range(1, n):
            for i in range(n - j):
                table[i, j] = (table[i + 1, j - 1] - table[i, j - 1]) / (self.x[i + j] - self.x[i])

        self.table = table
        self.coeffs = table[0, :].copy()

    def get_table(self):
        return self.table

    def get_coefficients(self):
        return self.coeffs

    def evaluate(self, x_eval):
        x_eval = np.atleast_1d(np.asarray(x_eval, dtype=float))
        result = np.full_like(x_eval, self.coeffs[0])

        for k in range(1, self.n):
            term = np.full_like(x_eval, self.coeffs[k])
            for j in range(k):
                term *= (x_eval - self.x[j])
            result += term

        return result if result.size > 1 else result[0]

    def derivative(self, x_eval):
        x_eval = np.atleast_1d(np.asarray(x_eval, dtype=float))
        result = np.zeros_like(x_eval)

        for k in range(1, self.n):
            term_deriv = np.zeros_like(x_eval)
            for m in range(k):
                partial = np.ones_like(x_eval)
                for j in range(k):
                    if j == m:
                        continue
                    partial *= (x_eval - self.x[j])
                term_deriv += partial
            result += self.coeffs[k] * term_deriv

        return result if result.size > 1 else result[0]

    def print_table(self):
        n = self.n
        print("Divided Difference Table:")
        for i in range(n):
            row = [f"{self.table[i, j]:.6f}" for j in range(n - i)]
            print(f"x={self.x[i]:>6.3f} | " + "  ".join(row))
            
    def absolute_error(self, exact_vals, approx_vals):
        """Helper added directly to the interpolator to avoid relying on base_method"""
        return np.abs(np.array(exact_vals) - np.array(approx_vals))


class LagrangeInterpolator:
    """Migrated from core for Q4 comparison."""
    def __init__(self, x, y):
        if len(x) != len(y):
            raise MismatchedLengthError("Length mismatch in Lagrange initialization.")
        self.x = np.array(x, dtype=float)
        self.y = np.array(y, dtype=float)
        self.n = len(x)

    def evaluate(self, x_eval):
        x_eval = np.atleast_1d(np.asarray(x_eval, dtype=float))
        result = np.zeros_like(x_eval)
        for i in range(self.n):
            Li = np.ones_like(x_eval)
            for j in range(self.n):
                if j == i: continue
                Li *= (x_eval - self.x[j]) / (self.x[i] - self.x[j])
            result += self.y[i] * Li
        return result if result.size > 1 else result[0]

    def derivative(self, x_eval):
        x_eval = np.atleast_1d(np.asarray(x_eval, dtype=float))
        result = np.zeros_like(x_eval)

        for i in range(self.n):
            denom = 1.0
            for j in range(self.n):
                if j != i:
                    denom *= (self.x[i] - self.x[j])

            Li_deriv_num = np.zeros_like(x_eval)
            others = [j for j in range(self.n) if j != i]
            for m in others:
                partial = np.ones_like(x_eval)
                for j in others:
                    if j != m:
                        partial *= (x_eval - self.x[j])
                Li_deriv_num += partial

            result += self.y[i] * Li_deriv_num / denom

        return result if result.size > 1 else result[0]

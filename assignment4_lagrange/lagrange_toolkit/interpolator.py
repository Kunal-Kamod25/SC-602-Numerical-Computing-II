"""
interpolator.py
----------------
Core classes for numerical interpolation, focusing on Object-Oriented Design.
Includes an abstract base class `Interpolation` and a derived class 
`LagrangeInterpolation` that utilizes the numerically stable Barycentric 
method for evaluating high-degree polynomials on large datasets.
"""

from abc import ABC, abstractmethod
from typing import Sequence, List, Union
import numpy as np
from scipy.interpolate import BarycentricInterpolator

from .exceptions import (
    DuplicateXError,
    InsufficientDataError,
    MismatchedLengthError,
)

class Interpolation(ABC):
    """Abstract base class for interpolation methods."""
    
    @abstractmethod
    def fit(self, x: Sequence[float], y: Sequence[float]) -> None:
        """Fit the interpolation model to the given data points."""
        pass

    @abstractmethod
    def evaluate(self, x_vals: Union[float, Sequence[float]]) -> Union[float, List[float]]:
        """Evaluate the interpolated polynomial at a specific point or array of points."""
        pass


class LagrangeInterpolation(Interpolation):
    """
    Builds and evaluates a Lagrange interpolating polynomial using the 
    numerically stable Barycentric method.
    """

    def __init__(self, x_values: Sequence[float] = None, y_values: Sequence[float] = None):
        self.x = []
        self.y = []
        self.model = None

        if x_values is not None and y_values is not None:
            self.fit(x_values, y_values)

    def fit(self, x: Sequence[float], y: Sequence[float]) -> None:
        """Fit the Lagrange interpolator to the given data points."""
        self.x = [float(v) for v in x]
        self.y = [float(v) for v in y]

        self._validate_input()
        
        # Use scipy's BarycentricInterpolator for numerical stability
        # It natively handles ZeroDivisionError scenarios by failing appropriately
        # when duplicate X values exist, but we already catch that in _validate_input.
        self.model = BarycentricInterpolator(self.x, self.y)

    def evaluate(self, x_vals: Union[float, Sequence[float]]) -> Union[float, List[float]]:
        """Estimate f(x_val) using the interpolating polynomial."""
        if self.model is None:
            raise ValueError("Model is not fitted. Call fit() first.")
        
        is_scalar = np.isscalar(x_vals)
        if is_scalar:
            return float(self.model(x_vals))
            
        estimates = self.model(x_vals)
        return [float(e) for e in estimates]

    def _validate_input(self) -> None:
        """Check the data makes sense before we try to interpolate it."""
        if len(self.x) != len(self.y):
            raise MismatchedLengthError(
                f"x has {len(self.x)} values but y has {len(self.y)} values. "
                "They must be the same length."
            )

        if len(self.x) < 2:
            raise InsufficientDataError(
                "Need at least 2 data points to interpolate, got "
                f"{len(self.x)}."
            )

        if len(set(self.x)) != len(self.x):
            raise DuplicateXError(
                "x values must all be unique for Lagrange interpolation "
                "(found at least one repeated x value)."
            )

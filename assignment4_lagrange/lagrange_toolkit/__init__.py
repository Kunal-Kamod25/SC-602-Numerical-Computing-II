"""
lagrange_toolkit
-----------------
Small reusable package for Lagrange interpolation problems.

I built this as one package so I can reuse the same interpolation
logic for both Assignment 4 (small hand-given datasets) and
Assignment 5 (large 1000-point dataset), instead of writing the
interpolation code twice.
"""

from .interpolator import Interpolation, LagrangeInterpolation
from .data_loader import load_points_from_csv, load_points_from_file, load_points_from_lists
from .exceptions import (
    DuplicateXError,
    InsufficientDataError,
    MismatchedLengthError,
    DataFileError,
)

__all__ = [
    "Interpolation",
    "LagrangeInterpolation",
    "load_points_from_csv",
    "load_points_from_file",
    "load_points_from_lists",
    "DuplicateXError",
    "InsufficientDataError",
    "MismatchedLengthError",
    "DataFileError",
]

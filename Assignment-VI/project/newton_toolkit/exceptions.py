"""
exceptions.py

Custom exceptions for the newton_toolkit package.
I'm adding these to match the structure we used in Assignment 4.
This ensures that when our interpolation breaks, it throws a highly
specific error rather than a generic ValueError.
"""

class NewtonToolkitError(ValueError):
    """Base class for all errors raised by this package."""
    pass


class DuplicateXError(NewtonToolkitError):
    """Raised when two or more x-values in the dataset are identical."""
    pass


class InsufficientDataError(NewtonToolkitError):
    """Raised when there are fewer than 2 data points."""
    pass


class MismatchedLengthError(NewtonToolkitError):
    """Raised when the list of x-values and y-values are not the same length."""
    pass


class DataFileError(NewtonToolkitError):
    """Raised when a data file can't be found or parsed correctly."""
    pass

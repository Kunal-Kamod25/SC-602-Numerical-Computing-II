"""
exceptions.py
-------------
Custom exceptions for the lagrange_toolkit package.

I made these instead of just raising plain Exception/ValueError
everywhere, so that when something goes wrong it's obvious WHAT
went wrong just from the exception name (this also makes it easy
to catch specific problems separately in the calling script).
"""


class LagrangeToolkitError(ValueError):
    """Base class for all errors raised by this package.

    Having one base class means a caller can do:
        except LagrangeToolkitError:
    and catch anything from this package in one go, if they want to.
    """
    pass


class DuplicateXError(LagrangeToolkitError):
    """Raised when two or more x-values in the dataset are the same.

    Lagrange interpolation needs every x-value to be unique, otherwise
    the basis polynomials involve dividing by zero (xi - xj = 0).
    """
    pass


class InsufficientDataError(LagrangeToolkitError):
    """Raised when there are fewer than 2 data points.

    You need at least 2 points to draw any kind of interpolating line/curve.
    """
    pass


class MismatchedLengthError(LagrangeToolkitError):
    """Raised when the list of x-values and y-values are not the same length."""
    pass


class DataFileError(LagrangeToolkitError):
    """Raised when a data file can't be found, opened, or parsed correctly."""
    pass

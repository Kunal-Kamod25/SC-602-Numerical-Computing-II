class NC2LibraryError(Exception):
    """Base error for the custom NC2 library."""


class DataFileError(NC2LibraryError):
    """Raised when an input file cannot be read or parsed."""


class DuplicateXError(NC2LibraryError):
    """Raised when duplicate x-values are found."""


class InsufficientDataError(NC2LibraryError):
    """Raised when points are not enough for interpolation."""


class MismatchedLengthError(NC2LibraryError):
    """Raised when x/y lengths are different."""


class InvalidStepSizeError(NC2LibraryError):
    """Raised when h <= 0 for numerical differentiation."""

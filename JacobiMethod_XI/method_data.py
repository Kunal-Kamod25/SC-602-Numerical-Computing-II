# method_data.py

# Store the results obtained from Jacobi's method
class RotationResult:

    def __init__(self, values, vectors, steps, errors):
        # Eigenvalues are the final diagonal elements
        self.values = values

        # Eigenvectors are stored as columns of this matrix
        self.vectors = vectors

        # Number of rotations performed
        self.steps = steps

        # Largest off-diagonal element after each rotation
        self.errors = errors
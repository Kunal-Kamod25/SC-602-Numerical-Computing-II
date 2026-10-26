# jacobi_method.py

import numpy as np
from method_data import RotationResult


# Class for finding eigenvalues and eigenvectors
class RotationSolver:

    def __init__(self, matrix, tolerance=1e-8, max_steps=1000):
        # Convert the input matrix into a NumPy array
        self.matrix = np.array(matrix, dtype=float)

        # Accuracy required for convergence
        self.tolerance = tolerance

        # Maximum number of rotations allowed
        self.max_steps = max_steps

    # Perform Jacobi's rotation method
    def calculate(self):

        A = self.matrix.copy()

        # Check whether the matrix is square
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("The matrix must be square.")

        # Jacobi rotation requires a symmetric matrix
        if not np.allclose(A, A.T):
            raise ValueError("The matrix must be symmetric.")

        n = A.shape[0]

        # Start with an identity matrix for eigenvectors
        V = np.eye(n) #creates an identity matrix.

        errors = []
        rotations = 0

        # Repeat until the off-diagonal elements are sufficiently small
        for step in range(self.max_steps):

            # Find the largest off-diagonal element
            off_diagonal = np.abs(A - np.diag(np.diag(A)))
            p, q = np.unravel_index(
                np.argmax(off_diagonal), off_diagonal.shape
            )

            largest = abs(A[p, q])
            errors.append(largest)

            # Stop when the required accuracy is reached
            if largest < self.tolerance:
                break

            # Calculate the rotation angle
            angle = 0.5 * np.arctan2(
                2 * A[p, q],
                A[q, q] - A[p, p]
            )

            # Calculate sine and cosine of the angle
            c = np.cos(angle)
            s = np.sin(angle)

            # Build the rotation matrix
            R = np.eye(n)
            R[p, p] = c
            R[q, q] = c
            R[p, q] = s
            R[q, p] = -s

            # Apply the similarity transformation: A_new = R.T @ A @ R
            A = R.T @ A @ R

            # Remove tiny numerical asymmetry
            A = (A + A.T) / 2

            # Accumulate the corresponding eigenvector rotations
            V = V @ R

            rotations += 1

        # The diagonal entries approximate the eigenvalues
        values = np.diag(A).copy()

        # Sort eigenvalues from largest to smallest
        order = np.argsort(values)[::-1] #sort the values in ascending order
        values = values[order] # This rearranges the eigenvalues
        V = V[:, order] # This rearranges the columns of the eigenvector matrix in the same order

        # Return the final results
        return RotationResult(
            values.tolist(),
            V.tolist(),
            rotations,
            errors
        )
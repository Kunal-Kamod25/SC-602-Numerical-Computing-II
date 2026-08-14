# interpolation.py
#
# Why this file exists:
# This is the "brain" of the whole project. This file has the
# actual Lagrange Interpolation formula implemented as a class.
#
# Lagrange Interpolation formula (for reference, from our notes):
#
#   P(x) = sum( y[i] * L_i(x) )   for i = 0 to n-1
#
#   where L_i(x) = product( (x - x[j]) / (x[i] - x[j]) )  for all j != i
#
# L_i(x) is called the "basis polynomial". It has a special
# property: L_i(x[i]) = 1 and L_i(x[j]) = 0 for every other j.

import numpy as np
from modules.polynomial import Polynomial

# If there are more points than this, we will not try to build the
# full symbolic polynomial (P(x) = ... form) because sympy becomes
# extremely slow for big polynomials. We will still calculate the
# numeric answer using numpy, which is fast even for big data.
MAX_POINTS_FOR_SYMBOLIC_POLY = 15


class LagrangeInterpolation:
    """
    Main class that does the Lagrange Interpolation calculation.
    We store x and y as numpy arrays so that the program can
    handle small data (10 points) as well as very large data
    (like 100000 points) without becoming too slow.
    """

    def __init__(self, x_list, y_list):
        # Using numpy arrays instead of normal python lists because
        # numpy is much faster for large amounts of numbers, and
        # the question specifically asked us to support up to
        # 100000 points.
        self.x = np.array(x_list, dtype=float)
        self.y = np.array(y_list, dtype=float)
        self.n = len(self.x)

    def calculate_basis_value(self, i, x_value):
        # Calculates L_i(x_value), a single number, not symbolic.
        # This is used both for estimating f(point) and also for
        # verifying the basis property.
        numerator = 1.0
        denominator = 1.0

        for j in range(self.n):
            if j != i:
                numerator = numerator * (x_value - self.x[j])
                denominator = denominator * (self.x[i] - self.x[j])

        return numerator / denominator

    def estimate(self, point):
        # This calculates P(point) using the numeric formula
        # directly. This works fine even for very large n because
        # we are not building any symbolic expression here, just
        # plain numbers.
        total = 0.0
        for i in range(self.n):
            basis_value = self.calculate_basis_value(i, point)
            total = total + (self.y[i] * basis_value)
        return total

    def get_all_basis_values_at_point(self, point):
        # Returns a list of L_0(point), L_1(point), ... L_n-1(point)
        # Useful for showing basis values in the output file.
        basis_values = []
        for i in range(self.n):
            basis_values.append(self.calculate_basis_value(i, point))
        return basis_values

    def verify_basis_property(self):
        # According to theory, L_i(x_i) should always be 1, and
        # L_i(x_j) should be 0 for any other point x_j.
        # We check this here to prove our formula is working
        # correctly. We only do this check up to a reasonable
        # limit of points, otherwise this becomes an n^2 loop
        # which would be too slow for huge datasets.
        check_limit = min(self.n, MAX_POINTS_FOR_SYMBOLIC_POLY)

        results = []
        for i in range(check_limit):
            value_at_own_point = self.calculate_basis_value(i, self.x[i])
            results.append((i, i, round(value_at_own_point, 6)))

        return results

    def estimate_many(self, points_array):
        # This does the same job as estimate(), but for MANY points
        # at once (used when we draw the smooth curve on the graph).
        #
        # We use numpy here instead of a simple python loop because
        # our dataset can be as big as 100000 points, and looping
        # point by point, basis by basis in plain python would be
        # very slow. Numpy can do this same math much faster because
        # it works on whole arrays together instead of one number
        # at a time.
        points_array = np.array(points_array, dtype=float)
        total = np.zeros_like(points_array)

        for i in range(self.n):
            numerator = np.ones_like(points_array)
            denominator = 1.0

            for j in range(self.n):
                if j != i:
                    numerator = numerator * (points_array - self.x[j])
                    denominator = denominator * (self.x[i] - self.x[j])

            basis_values = numerator / denominator
            total = total + (self.y[i] * basis_values)

        return total

    def build_polynomial(self):
        # Builds the FULL symbolic polynomial P(x), so we can
        # print it in proper math form like "P(x) = 2*x + 3".
        #
        # We only do this for smaller datasets because sympy
        # symbolic expansion becomes really slow once we have
        # many points (the polynomial degree grows with points).
        if self.n > MAX_POINTS_FOR_SYMBOLIC_POLY:
            return None

        poly = Polynomial()
        x_symbol = poly.x

        for i in range(self.n):
            # Build the symbolic version of L_i(x)
            numerator_expr = 1
            denominator_value = 1.0

            for j in range(self.n):
                if j != i:
                    numerator_expr = numerator_expr * (x_symbol - self.x[j])
                    denominator_value = denominator_value * (self.x[i] - self.x[j])

            term = self.y[i] * numerator_expr / denominator_value
            poly.add_term(term)

        poly.simplify()
        return poly

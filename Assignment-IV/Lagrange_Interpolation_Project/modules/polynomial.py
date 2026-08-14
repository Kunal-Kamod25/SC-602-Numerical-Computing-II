# polynomial.py
#
# Why this file exists:
# The Lagrange method gives us a polynomial, but just having a
# Python function that computes values is not very "readable".
# For the assignment, we also want to actually SHOW the polynomial
# in normal math form, like: P(x) = 2.0 + 1.5*x - 0.5*x^2
#
# We use the sympy library here because it can handle symbolic
# math (that means it understands "x" as a variable, not just a
# number) and it can also simplify and expand expressions for us.

import sympy


class Polynomial:
    """
    This class stores a polynomial in symbolic form using sympy,
    and gives us methods to print it nicely or evaluate it at
    some x value.
    """

    def __init__(self):
        # sympy.symbols creates a symbolic variable named 'x'
        # which we will use to build the polynomial expression.
        self.x = sympy.symbols('x')

        # This will hold the actual polynomial expression.
        # We start with 0 because we build it up term by term.
        self.expression = 0

    def add_term(self, term):
        # Adds one more piece to the polynomial.
        # This is called once per basis polynomial in Lagrange method.
        self.expression = self.expression + term

    def simplify(self):
        # sympy.expand turns something like (x-1)*(x-2) into
        # x^2 - 3x + 2, which is much easier to read.
        self.expression = sympy.expand(self.expression)
        self._clean_tiny_coefficients()

    def _clean_tiny_coefficients(self):
        # Because we are using normal decimal numbers (floats) and
        # not exact fractions, sometimes sympy leaves behind tiny
        # "leftover" values like 0.0000000000000003 where the real
        # answer should just be 0. This happens due to how
        # computers store decimal numbers internally (floating
        # point rounding). This function cleans those up so the
        # final polynomial looks neat, e.g. it turns a term like
        # -3e-16*x**3 into simply 0 (which then disappears).
        try:
            poly_form = sympy.Poly(self.expression, self.x)
        except sympy.PolynomialError:
            # If for some reason it cannot be converted to a
            # polynomial (e.g. expression is just a plain number),
            # we just skip the cleanup step.
            return

        coefficients = poly_form.all_coeffs()
        degree = len(coefficients) - 1

        cleaned_expression = 0
        for power, coeff in enumerate(reversed(coefficients)):
            coeff_value = float(coeff)
            if abs(coeff_value) < 1e-9:
                continue  # treat as zero, so we just skip this term
            cleaned_expression += round(coeff_value, 10) * (self.x ** power)

        self.expression = cleaned_expression

    def get_expression(self):
        return self.expression

    def evaluate_at(self, value):
        # Substitutes the given value in place of x and
        # calculates the final number.
        result = self.expression.subs(self.x, value)
        # Convert to a normal Python float for easier use later.
        return float(result)

    def to_readable_string(self):
        # Converts the sympy expression into a normal string
        # that looks like proper math notation.
        # Example output: "1.0*x**2 + 2.0*x + 3.0"
        return str(self.expression)

    def __str__(self):
        # This lets us just do print(polynomial_object) and get
        # a nice readable form automatically.
        return "P(x) = " + self.to_readable_string()

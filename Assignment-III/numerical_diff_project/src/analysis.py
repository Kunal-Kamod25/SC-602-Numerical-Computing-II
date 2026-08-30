"""
analysis.py
-----------
Orchestrates the numerical experiment:
    - For every test function and every step size h, compute:
        1. Central Difference D(h)
        2. Richardson Extrapolation R(h)
        3. Exact derivative
        4. Absolute error of D(h)
        5. Absolute error of R(h)
    - Compute observed convergence order (log-log slope) for both methods.

OOP Design:
    ResultRecord        : simple data container (dataclass) for one (function, h) row
    ExperimentRunner     : runs the full sweep and stores/returns results
"""

from dataclasses import dataclass, asdict
from typing import List
import math

from .functions import TestFunction
from .differentiation import DifferentiationMethod, CentralDifference, RichardsonExtrapolation


@dataclass
class ResultRecord:
    """One row of the results table for a given function and step size h."""
    function_name: str
    x: float
    h: float
    D_h: float          # Central Difference approximation
    R_h: float           # Richardson Extrapolation approximation
    exact: float
    error_D: float
    error_R: float

    def as_dict(self) -> dict:
        return asdict(self)


class ExperimentRunner:
    """
    Runs Central Difference and Richardson Extrapolation for a set of
    test functions across a set of step sizes h, at a fixed evaluation
    point x.
    """

    def __init__(
        self,
        functions: List[TestFunction],
        h_values: List[float],
        x_eval: float = 1.0,
        central: DifferentiationMethod = None,
        richardson: DifferentiationMethod = None,
    ):
        self.functions = functions
        self.h_values = sorted(h_values, reverse=True)  # largest h first
        self.x_eval = x_eval
        self.central = central if central is not None else CentralDifference()
        self.richardson = richardson if richardson is not None else RichardsonExtrapolation(self.central)
        self.results: List[ResultRecord] = []

    def run(self) -> List[ResultRecord]:
        """Execute the full sweep and populate self.results."""
        self.results = []
        for func in self.functions:
            exact = func.exact_derivative(self.x_eval)
            for h in self.h_values:
                d_h = self.central.compute(func, self.x_eval, h)
                r_h = self.richardson.compute(func, self.x_eval, h)
                err_d = abs(exact - d_h)
                err_r = abs(exact - r_h)
                self.results.append(
                    ResultRecord(
                        function_name=func.name,
                        x=self.x_eval,
                        h=h,
                        D_h=d_h,
                        R_h=r_h,
                        exact=exact,
                        error_D=err_d,
                        error_R=err_r,
                    )
                )
        return self.results

    def results_for(self, function_name: str) -> List[ResultRecord]:
        """Filter stored results for a single function name."""
        return [r for r in self.results if r.function_name == function_name]

    @staticmethod
    def observed_slope(h_values: List[float], error_values: List[float]) -> float:
        """
        Estimate the log-log convergence slope via a simple linear
        least-squares fit of log(error) vs log(h), ignoring any points
        where error is zero or non-finite (can occur once round-off
        error dominates).

        The slope approximates the order p in: error ~ C * h^p
        """
        xs, ys = [], []
        for h, e in zip(h_values, error_values):
            if e is not None and e > 0 and math.isfinite(e):
                xs.append(math.log10(h))
                ys.append(math.log10(e))

        n = len(xs)
        if n < 2:
            return float("nan")

        mean_x = sum(xs) / n
        mean_y = sum(ys) / n
        num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
        den = sum((x - mean_x) ** 2 for x in xs)
        if den == 0:
            return float("nan")
        return num / den

    @staticmethod
    def truncation_dominated_prefix(h_values: List[float], error_values: List[float]):
        """
        Walk h from largest to smallest and keep only the leading run of
        points where the error is still (roughly) monotonically
        decreasing. Once round-off error starts pushing the error back
        up, that point and everything after it is dropped. This isolates
        the region where the theoretical truncation-error order (O(h^2)
        or O(h^4)) is actually expected to hold, which is exactly the
        regime the assignment asks you to compare against theory.

        h_values is assumed sorted largest -> smallest (as produced by
        ExperimentRunner). A small relative tolerance allows for tiny
        floating-point wiggles that aren't a genuine round-off up-turn.
        """
        tol = 1e-6  # relative tolerance for "still decreasing"
        h_keep, e_keep = [], []
        prev_e = None
        for h, e in zip(h_values, error_values):
            if e is None or not math.isfinite(e) or e <= 0:
                break
            if prev_e is not None and e > prev_e * (1 + tol):
                break
            h_keep.append(h)
            e_keep.append(e)
            prev_e = e
        # need at least 2 points to fit a slope
        if len(h_keep) < 2:
            return h_values[: min(2, len(h_values))], error_values[: min(2, len(error_values))]
        return h_keep, e_keep

    def slopes_for(self, function_name: str) -> dict:
        """
        Return the observed convergence slopes for D(h) and R(h) for a
        given function.

        Two slopes are reported for each method:
          - slope_D / slope_R:            fit over ONLY the truncation-
            dominated region (h large enough that round-off hasn't taken
            over yet). This is the number that should match the
            theoretical O(h^2) / O(h^4) orders.
          - slope_D_full / slope_R_full:  fit over ALL collected h
            values, included for reference/discussion of round-off
            behaviour (Q3, Q6).
        """
        rows = self.results_for(function_name)
        h_vals = [r.h for r in rows]
        err_d = [r.error_D for r in rows]
        err_r = [r.error_R for r in rows]

        h_trunc_d, e_trunc_d = self.truncation_dominated_prefix(h_vals, err_d)
        h_trunc_r, e_trunc_r = self.truncation_dominated_prefix(h_vals, err_r)

        return {
            "slope_D": self.observed_slope(h_trunc_d, e_trunc_d),
            "slope_R": self.observed_slope(h_trunc_r, e_trunc_r),
            "slope_D_full": self.observed_slope(h_vals, err_d),
            "slope_R_full": self.observed_slope(h_vals, err_r),
            "n_points_D": len(h_trunc_d),
            "n_points_R": len(h_trunc_r),
        }

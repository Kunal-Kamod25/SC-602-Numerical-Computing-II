"""
differentiation.py
"""
import numpy as np
from .base_method import NumericalMethod

class FiniteDifference(NumericalMethod):
    def __init__(self, func, h=1e-3):
        super().__init__()
        self.func = func
        self.h = h
    def evaluate(self, x_eval):
        raise NotImplementedError

class ForwardDifference(FiniteDifference):
    def evaluate(self, x_eval):
        f, h = self.func, self.h
        return (f(x_eval + h) - f(x_eval)) / h

class BackwardDifference(FiniteDifference):
    def evaluate(self, x_eval):
        f, h = self.func, self.h
        return (f(x_eval) - f(x_eval - h)) / h

class CentralDifference(FiniteDifference):
    def evaluate(self, x_eval):
        f, h = self.func, self.h
        return (f(x_eval + h) - f(x_eval - h)) / (2 * h)

class RichardsonExtrapolation(NumericalMethod):
    def __init__(self, diff_method_cls, func, h=1e-2):
        super().__init__()
        self.diff_method_cls = diff_method_cls
        self.func = func
        self.h = h
    def evaluate(self, x_eval):
        D_h = self.diff_method_cls(self.func, self.h).evaluate(x_eval)
        D_h2 = self.diff_method_cls(self.func, self.h / 2).evaluate(x_eval)
        return D_h2 + (D_h2 - D_h) / 3

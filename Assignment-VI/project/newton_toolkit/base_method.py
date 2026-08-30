"""
base_method.py
"""
import numpy as np

class NumericalMethod:
    def __init__(self, x=None, y=None):
        pass
        
    def absolute_error(self, exact_vals, approx_vals):
        return np.abs(np.array(exact_vals) - np.array(approx_vals))
        
    def relative_error(self, exact_vals, approx_vals):
        e = np.array(exact_vals)
        a = np.array(approx_vals)
        return np.abs((e - a) / np.where(e == 0, 1e-12, e))
        
    def max_error(self, exact_vals, approx_vals):
        return np.max(self.absolute_error(exact_vals, approx_vals))

from __future__ import annotations

from typing import Sequence

import numpy as np


def loglog_slope(h_values: Sequence[float], errors: Sequence[float]) -> float:
    h = np.asarray(h_values, dtype=float)
    err = np.asarray(errors, dtype=float)
    mask = (h > 0) & (err > 0)
    if np.count_nonzero(mask) < 2:
        return float("nan")
    x = np.log10(h[mask])
    y = np.log10(err[mask])
    slope, _ = np.polyfit(x, y, deg=1)
    return float(slope)

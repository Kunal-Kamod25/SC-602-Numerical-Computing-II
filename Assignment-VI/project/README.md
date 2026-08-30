# Numerical Computing II — Assignment VI (Newton Interpolation)

Restructured so this isn't its own isolated folder anymore — `core/` is meant
to hold the shared classes from previous assignments too (finite difference,
Richardson, Lagrange), and each new assignment just adds a new file that
imports from `core/` instead of re-writing the same formulas again.

## Structure

```
project/
├── core/
│   ├── base_method.py        # NumericalMethod - abstract base, error metrics
│   ├── interpolation.py      # Interpolator -> LagrangeInterpolator, NewtonInterpolator
│   └── differentiation.py    # FiniteDifference -> Forward/Backward/Central, Richardson
├── io_utils/
│   └── file_io.py            # csv read/write helpers
├── inputs/                   # data files each script reads from
│   ├── q1_data.csv ... q6_data.csv
│   └── q5_config.csv         # list of n values for the Runge experiment
├── outputs/                  # generated at runtime: tables (csv) + plots (png)
│   └── q1/ q2/ q3/ q4/ q5/ q6/
├── q1_newton_basic.py
├── q2_unequal_spacing.py
├── q3_more_data.py
├── q4_newton_vs_lagrange.py
├── q5_runge_phenomenon.py
├── q6_numerical_differentiation.py
└── main.py                   # runs all 6 in order
```

## Class hierarchy

```
NumericalMethod (abstract)
├── Interpolator
│   ├── LagrangeInterpolator      (has .evaluate(), .derivative())
│   └── NewtonInterpolator        (has .evaluate(), .derivative(), .get_table())
├── FiniteDifference
│   ├── ForwardDifference
│   ├── BackwardDifference
│   └── CentralDifference
└── RichardsonExtrapolation       (wraps any FiniteDifference subclass)
```

`core/differentiation.py` is where last assignment's forward/backward/
central difference + Richardson code lives now — I rewrote it to inherit
from the same `NumericalMethod` base as the interpolation stuff, so Q6 can
just import `CentralDifference` directly instead of copy-pasting the formula
into a new file. If your actual old code had extra features (convergence
plots vs step size, etc.) port those into this file rather than making a
separate one.

## Running it

```bash
python3 main.py          # runs Q1 through Q6, writes everything to outputs/
python3 q3_more_data.py  # or run just one question directly
```

Every script:
1. reads its input data from `inputs/*.csv`
2. builds the relevant interpolator/differentiator object(s)
3. prints results to the console
4. writes result tables to `outputs/qN/*.csv`
5. saves plots to `outputs/qN/*.png`

## Notes on Q3 and Q6 (the parts that got missed before)

- **Q3** now includes the actual required comparison table (first 4 / 8 / 12
  / all 16 points -> degree -> max error), not just the full 16-point plot.
- **Q6** now compares three derivative methods side by side (Newton
  polynomial derivative, Lagrange polynomial derivative, plain central
  finite difference on the real function) instead of just Newton vs exact.

# Assignment IV — Lagrange Interpolation

Numerical Computing II | Aug 14, 2026

## What's in here

```
assignment4_lagrange/
├── pyproject.toml          # poetry project + dependencies
├── poetry.lock              # locked dependency versions
├── lagrange_toolkit/         # the reusable package
│   ├── __init__.py
│   ├── exceptions.py         # custom exceptions
│   ├── data_loader.py        # file handling (CSV + list input)
│   ├── interpolator.py       # LagrangeInterpolator class (main logic)
│   └── utils.py               # plotting + printing helpers
├── solve_assignment4.py      # runs all 5 assignment questions
└── outputs/                   # generated graphs (created when you run the script)
```

I split the interpolation logic into its own package (`lagrange_toolkit`)
instead of writing everything in one script, so I can reuse the exact same
code for Assignment 5, which uses a much bigger dataset.

## Setup

This project uses [Poetry](https://python-poetry.org/) for dependency
management (keeps the exact numpy/matplotlib versions locked so it runs
the same on any machine).

```bash
# 1. install poetry if you don't already have it
curl -sSL https://install.python-poetry.org | python3 -

# 2. from inside this folder, install the dependencies
poetry install

# 3. run the assignment
poetry run python solve_assignment4.py
```

Graphs get saved into the `outputs/` folder.

## Package overview

- **`interpolator.py`** — the `LagrangeInterpolator` class. Give it x and y
  values, it builds the basis polynomials `L_i(x)`, combines them into the
  final `P(x)`, and lets you evaluate it at any point or check its degree.
- **`exceptions.py`** — custom exceptions (`DuplicateXError`,
  `InsufficientDataError`, `MismatchedLengthError`, `DataFileError`) so
  errors are specific instead of generic.
- **`data_loader.py`** — handles reading points either from plain lists
  (used in this assignment) or from a CSV file (used in Assignment 5),
  with proper `try/except` around file I/O.
- **`utils.py`** — plotting and table-printing helpers, kept separate so
  `solve_assignment4.py` stays focused on the actual assignment answers.

## Dependencies

- Python `>=3.10,<4.0`
- `numpy` — polynomial representation and arithmetic
- `matplotlib` — plotting the interpolation curves

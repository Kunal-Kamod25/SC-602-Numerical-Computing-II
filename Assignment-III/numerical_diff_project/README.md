# Numerical Computing II — Assignment III
## Can We Make Numerical Differentiation More Accurate? Investigation of Richardson Extrapolation

A modular, object-oriented Python implementation of Central Difference and
Richardson Extrapolation, with a full convergence study, plots, results
tables, and written answers to Q1–Q6.

---

## 1. Project Structure

```
numerical_diff_project/
├── main.py                     # single entry point — run this
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── functions.py            # TestFunction hierarchy (e^x, sin x, cos x, x^3-2x+1)
│   ├── differentiation.py      # DifferentiationMethod hierarchy (Central Diff, Richardson)
│   ├── analysis.py             # ExperimentRunner: runs the sweep, computes errors & slopes
│   ├── file_handler.py         # All file I/O (CSV, text report) in one place
│   └── visualizer.py           # All matplotlib plotting in one place
└── output/                     # generated when you run main.py
    ├── results/
    │   ├── results.csv             # full results table (D(h), R(h), exact, errors)
    │   └── convergence_slopes.csv  # observed vs theoretical log-log slopes
    ├── plots/
    │   ├── test_functions.png
    │   ├── convergence_overview.png
    │   └── convergence_<function>.png   (one per function)
    ├── report.txt               # full written report incl. Q1-Q6 answers
    └── algorithm_pseudocode.txt
```

## 2. How to Run

```bash
pip install -r requirements.txt
python main.py
```

Everything (CSV tables, plots, and the text report) is (re)generated inside
the `output/` folder.

## 3. Design Overview (OOP)

- **`TestFunction`** (abstract base class) — each of the four functions
  (`ExponentialFunction`, `SineFunction`, `CosineFunction`,
  `PolynomialFunction`) implements `evaluate(x)` and `exact_derivative(x)`,
  so numerical results can always be checked against ground truth.

- **`DifferentiationMethod`** (abstract base class)
  - `CentralDifference` — `D(h) = [f(x+h) - f(x-h)] / (2h)`, theoretical
    order `O(h²)`.
  - `RichardsonExtrapolation` — composes a `CentralDifference` instance and
    combines `D(h)` and `D(h/2)` as `R(h) = [4·D(h/2) - D(h)] / 3`,
    theoretical order `O(h⁴)`.

- **`ExperimentRunner`** (`analysis.py`) — sweeps every function over every
  `h`, stores a `ResultRecord` per (function, h) pair, and estimates the
  observed log-log convergence slope via least-squares. It automatically
  isolates the *truncation-error-dominated* region (before round-off takes
  over) so the observed slope can be fairly compared to the theoretical
  order — it also reports the full-range slope separately for discussion.

- **`FileHandler`** (`file_handler.py`) — the only module that touches the
  filesystem: writes/reads CSVs and text reports, and manages the
  `output/results` and `output/plots` directories.

- **`Visualizer`** (`visualizer.py`) — the only module that touches
  matplotlib: function plots, per-function log-log convergence plots, and
  a combined overview figure.

- **`main.py`** — orchestrates the above: builds the objects, runs the
  sweep, saves everything, and writes the final report (including the
  answers to Q1–Q6, grounded in the actual computed numbers).

## 4. Step Sizes Used

`h = 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10, 1e-11, 1e-12`

The first six satisfy the assignment's minimum requirement; the remaining
six extend the sweep to clearly show where floating-point round-off error
begins to dominate and overwhelm the truncation-error benefit of smaller `h`
(visible as the "V-shaped" curves in the convergence plots).

## 5. Evaluation Point

All derivatives are approximated at `x = 1`, as required by the assignment
(`f'(1)` for all four functions).

# Lagrange Interpolation Project

Numerical Computing II Assignment — implementation of Lagrange
Interpolation in Python, done using OOP and modular programming.

---

## 1. Project Overview

This project takes a set of `(x, y)` data points and finds the
value of `f(x)` at some new point using **Lagrange's Interpolation
Formula**:

```
P(x) = sum( y[i] * L_i(x) )   for i = 0 to n-1

where L_i(x) = product( (x - x[j]) / (x[i] - x[j]) )   for all j != i
```

The program:
- reads data points from a `.txt` input file
- builds the interpolation polynomial
- calculates the estimated value at the required point
- verifies the basis polynomial property (`L_i(x_i) = 1`)
- saves a full report to an output `.txt` file
- draws and saves a graph of the curve
- also saves the plotted points as a `.csv` file

There is a menu with 5 pre-made assignment questions, plus an
option to enter your own custom dataset.

---

## 2. Folder Structure

```
Lagrange_Interpolation_Project/
│
├── data/
│   ├── input/                 -> input .txt files (one per question)
│   │   ├── question1.txt
│   │   ├── question2.txt
│   │   ├── question3.txt
│   │   ├── question4.txt
│   │   ├── question5.txt
│   │   └── custom.txt
│   │
│   └── output/                -> generated result files
│       ├── output_question1.txt
│       ├── output_question2.txt
│       ├── output_question3.txt
│       ├── output_question4.txt
│       ├── output_question5.txt
│       ├── output_custom.txt
│       └── graph_data.csv
│
├── graphs/                    -> generated graph images (.png)
│   ├── question1.png
│   ├── question2.png
│   ├── question3.png
│   ├── question4.png
│   ├── question5.png
│   └── custom.png
│
├── modules/                   -> all the OOP / logic code
│   ├── __init__.py
│   ├── file_handler.py
│   ├── interpolation.py
│   ├── graph_plotter.py
│   ├── polynomial.py
│   ├── validator.py
│   └── utilities.py
│
├── main.py                    -> program entry point (menu)
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 3. Requirements

- Python 3.12 or higher
- Libraries: `numpy`, `matplotlib`, `sympy`
  (see `requirements.txt`)

---

## 4. Installation

```bash
# 1. Go into the project folder
cd Lagrange_Interpolation_Project

# 2. (Optional but recommended) create a virtual environment
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate

# 3. Install the required libraries
pip install -r requirements.txt
```

---

## 5. How to Run

```bash
python main.py
```

You will see a menu like this:

```
========================================
LAGRANGE INTERPOLATION PROJECT
========================================
1. Solve Question 1
2. Solve Question 2
3. Solve Question 3
4. Solve Question 4
5. Solve Question 5
6. Solve Custom Input
7. Exit
========================================
Enter your choice (1-7):
```

Just type the number of the question you want to solve. The
program will automatically read the correct input file, do the
calculation, and save the output file + graph.

Choosing option `6` will ask you to type your own data points
directly in the terminal, and it saves them into
`data/input/custom.txt` before solving it.

---

## 6. Input File Format

Every input file follows this simple format:

```
<number of points>
<x0> <y0>
<x1> <y1>
...
<point to estimate>
```

You can also give more than one point to estimate — just put
each one on its own line at the end. Example (from `question2.txt`):

```
4
1 2.0
2 4.5
3 8.0
4 13.5
2.5
3.5
```

This means: 4 data points are given, and we want to know
`f(2.5)` **and** `f(3.5)`.

---

## 7. Output Format

Each output file (saved in `data/output/`) contains:

- Program title and which question it is
- Date and time it was generated
- All the input data points
- Basis polynomial verification (`L_i(x_i) = 1` check)
- The full interpolation polynomial, e.g. `P(x) = 1.0*x**2 + 1.0`
- The estimated value(s)
- Time taken to run
- A "Program finished successfully" line at the end

Old output files are automatically overwritten every time you
run that question again, so you always see the latest result.

---

## 8. Graph Example

Every question also produces a graph like this (this is the
actual graph generated for Question 2, showing `f(2.5)` and
`f(3.5)` estimated from 4 given points):

`graphs/question2.png`

The graph always shows:
- the original data points (red dots)
- the smooth interpolation curve (blue line)
- the estimated point (green star)
- title, axis labels, legend, and grid

---

## 9. Assignment Questions (Quick Summary)

| Question | What it asks |
|---|---|
| Q1 | Build polynomial from 3 points, verify basis property, find f(1.5) |
| Q2 | Find f(2.5) and f(3.5) from 4 points |
| Q3 | Find f(1) and f(2) from 4 unevenly spaced points |
| Q4 | Find f(4), f(6), f(8) — note f(8) is extrapolation (outside given range) |
| Q5 | Find degree of polynomial from perfect-square data and explain why it comes out quadratic even with 4 points given |

**About Question 5:** Even though 4 points are given, the actual
underlying data follows `y = x^2` exactly. Lagrange interpolation
through 4 points normally gives a degree-3 (cubic) polynomial, but
since the 4th point does not add any "new curve information"
(it fits perfectly on the same parabola as the other 3), the
`x^3` and `x` terms in the final polynomial come out as zero. So
the polynomial simplifies down to just `P(x) = x^2`, a quadratic.

---

## 10. Large Dataset Support

The program is written using `numpy` arrays (not fixed-size lists)
so it does not break when the number of data points changes — it
has been tested with datasets ranging from 10 points up to a few
hundred points without issues.

**Important note on very large datasets (thousands of points):**
The "naive" Lagrange formula used in this project calculates the
numerator and denominator of each basis polynomial by directly
multiplying many `(x - x[j])` terms together. When there are a
very large number of points (roughly above 100-200, depending on
the data), these products become too large for a normal computer
float to store accurately. This is called **floating-point
overflow**, and it makes the result come out as `nan` (not a
number). The program detects this and prints a warning when a
large dataset is loaded, so this is not a silent bug, it is a
known limitation of the direct Lagrange formula. See "Future
Improvements" below for how this could be fixed properly.

To keep the graph readable and fast for large datasets, the graph
image only plots a sample of the original points (see
`MAX_POINTS_FOR_GRAPH` in `graph_plotter.py`), but the numeric
answer written to the output file always uses the **full**
dataset.

Similarly, showing the full symbolic polynomial (`P(x) = ...`) is
only done for datasets up to 15 points (see
`MAX_POINTS_FOR_SYMBOLIC_POLY` in `interpolation.py`) because
building and simplifying a huge symbolic expression with `sympy`
becomes very slow for bigger polynomials. The numeric estimate
(the actual number) is still calculated correctly using the full
dataset even when the polynomial itself is not printed.

---

## 11. File-by-File Explanation

### `main.py`
**Why it exists:** This is the starting point of the program. It
shows the menu, takes the user's choice, and calls the right
classes from `modules/` to do the actual work.
**Main functions:** `show_menu()`, `run_question()`,
`create_custom_input_file()`, `main()`
**Time Complexity:** Depends on which question is run (see
`interpolation.py` below); `main.py` itself just does simple
menu logic which is O(1).
**Space Complexity:** O(n) to hold the x and y values for the
question being solved.

### `modules/file_handler.py` — class `FileHandler`
**Why it exists:** Keeps all file reading/writing code in one
place, separate from the math logic.
**Methods:**
- `read_input_file()` — reads and parses the input `.txt` file
- `write_output_file()` — writes the result report to a `.txt` file
- `save_graph_data_csv()` — saves plotted points into a `.csv` file
**Time Complexity:** O(n) to read/write n lines of data.
**Space Complexity:** O(n) to store the lines in memory.

### `modules/validator.py` — class `Validator`
**Why it exists:** Checks that the data is valid *before* we try
to do any math on it (e.g. no duplicate x values).
**Methods:** `check_minimum_points()`, `check_duplicate_x()`,
`check_equal_length()`, `check_not_empty()`,
`check_point_in_reasonable_range()`,
`check_large_dataset_warning()`, `validate_all()`
**Time Complexity:** O(n) for the duplicate check (uses a set),
O(1) for the rest.
**Space Complexity:** O(n) for the temporary set used in the
duplicate check.

### `modules/interpolation.py` — class `LagrangeInterpolation`
**Why it exists:** This is the actual math engine of the project.
**Methods:**
- `calculate_basis_value()` — calculates one `L_i(x)` value
- `estimate()` — calculates `P(point)` for a single point
- `estimate_many()` — same as above but for many points at once
  (used for drawing the smooth curve), sped up using `numpy`
- `verify_basis_property()` — checks `L_i(x_i) = 1`
- `build_polynomial()` — builds the full symbolic polynomial
  using the `Polynomial` class (only for smaller datasets)
**Time Complexity:** Calculating one basis value is O(n).
Estimating one point needs all n basis values, so it is O(n^2).
Building the full polynomial is also roughly O(n^2) basis terms,
each with a symbolic expansion cost on top of that.
**Space Complexity:** O(n) for storing the x and y arrays.

### `modules/polynomial.py` — class `Polynomial`
**Why it exists:** Wraps `sympy`'s symbolic math so we can build
up and neatly print the final polynomial expression.
**Methods:** `add_term()`, `simplify()`, `evaluate_at()`,
`to_readable_string()`, `_clean_tiny_coefficients()`
**Time Complexity:** Depends on `sympy`'s internal expansion
algorithm, generally grows with the number of terms/degree.
**Space Complexity:** O(degree) to store the polynomial expression.

### `modules/graph_plotter.py` — class `GraphPlotter`
**Why it exists:** Keeps all the `matplotlib` drawing code
separate from the math code.
**Methods:** `plot_and_save()`, `_get_sample_for_plotting()`
**Time Complexity:** O(k) where k is `CURVE_RESOLUTION` (number
of points used to draw the smooth curve line), each needing an
O(n) basis calculation, so roughly O(k * n).
**Space Complexity:** O(k) to store the curve points for drawing.

### `modules/utilities.py`
**Why it exists:** Small reusable helper functions used across
the whole project (timer, date string, formatting numbers).
**Functions:** `get_current_datetime_string()`,
`print_separator()`, `start_timer()`, `stop_timer()`,
`format_number()`
**Time / Space Complexity:** All O(1), these are simple one-line
helper functions.

---

## 12. Future Improvements

- Use the **barycentric form** of Lagrange interpolation instead
  of the naive/direct form. The barycentric formula is
  mathematically equivalent but is much more numerically stable,
  so it would let the program handle thousands of points without
  running into floating-point overflow.
- Add a proper GUI (using `tkinter`) instead of a text menu.
- Let the user directly type data in the terminal without needing
  to go through a file first, for quick one-off checks.
- Add automatic detection of the "true" polynomial degree (like
  in Question 5) by checking which coefficients are close to
  zero, and print that as a separate line in the report.
- Add unit tests using `unittest` or `pytest` for each module.

---

## 13. Notes

This project was written for a Numerical Computing II assignment,
so the code is kept intentionally simple and beginner-friendly —
no advanced Python tricks, no decorators, no complex inheritance.
Every function has comments explaining what it is doing, written
the way a student would explain it in a viva.

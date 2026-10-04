ASSIGNMENT 7 - COMPOSITE TRAPEZOIDAL RULE

This is a beginner-friendly Python implementation of the Numerical Computing
Assignment 7.

FILES:
1. main.py
   Main program. It reads input and calls each question.

2. header.py
   Simple function declarations/type information, kept separately like a
   header file as requested.

3. algorithms.py
   Contains the TrapezoidalRule class and numerical formulas.

4. functions.py
   Contains input reading, output saving and graph functions.

5. input.txt
   All problem inputs are kept here. Change values here instead of changing
   the main program.

6. output/
   Contains generated CSV tables, graphs and final_report.txt.

HOW TO RUN:
1. Install Python.
2. Open terminal in this folder.
3. Install matplotlib:
       pip install -r requirements.txt
4. Run:
       python main.py

IMPORTANT FORMULAS:

Composite Trapezoidal Rule:
I = h [ f(a)/2 + f(x1) + ... + f(x(n-1)) + f(b)/2 ]

where:
h = (b-a)/n

Absolute Error:
Error = |Exact Value - Approximation|

Order:
p = log2(E(h) / E(h/2))

Richardson Extrapolation for trapezoidal rule:
R = (4*T(2h) - T(h))/3

EXPECTED MAIN RESULTS:

Question 1 exact value:
8/3 = 2.6666666667

Question 3 estimated integral:
6.5125

The code is intentionally kept simple and modular for a beginner student.

# NC2 Custom Numerical Library

This is a unified Python project for Numerical Computing II assignments.
Instead of keeping every assignment as a separate style/project, this folder puts everything in one modular OOP library.

## What this includes

- Assignment II: Forward/Backward/Central numerical differentiation
- Assignment III: Richardson extrapolation (built using inheritance + composition)
- Assignment IV: Lagrange interpolation on assignment input files
- Assignment V: Big-dataset interpolation (150-point student dataset)
- Assignment VI: Newton interpolation + method comparisons + Runge table

## OOP features used

- **Abstraction**: abstract base classes for differentiation/interpolation styles.
- **Inheritance**: concrete classes (Forward, Backward, Central, Newton, Lagrange) inherit from base classes.
- **Polymorphism**: common interfaces used in assignment runners.
- **Encapsulation**: internal tables/coefficients are stored in class internals and exposed through methods.
- **Exception Handling**: custom exceptions for invalid files, bad step size, invalid points, etc.

## Folder structure

```text
NC2_Custom_Library/
├── core/           # main numerical classes and exceptions
├── io_utils/       # input/output helpers
├── assignments/    # separate assignment runner files
├── inputs/         # separate input folders per assignment
├── outputs/        # separate output folders per assignment
└── main.py         # run everything in one shot
```

## How to run

```bash
pip install -r requirements.txt
python main.py
```

You can also run each assignment file directly, for example:

```bash
python assignments/ass5_main.py
```

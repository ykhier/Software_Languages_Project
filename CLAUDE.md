# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a **software languages comparison project** that implements the same polynomial root-finding algorithm in two languages: Python and Racket. The goal is to compare behavior and (in Python) runtime against NumPy's built-in solver.

## Running the Code

**Python:**
```bash
python python_code.py
```
Runs the custom algorithm and compares results against `np.roots`, printing both root lists and runtimes.

**Racket:**
```bash
racket code_racket.rkt
```
Must be run from the project root directory — the Racket code uses `(current-directory)` to build the data file path.

**Dependencies:** Python requires `numpy`. Racket uses only standard libraries (`racket/list`, `racket/file`).

## Algorithm Architecture

Both implementations follow the same structure:

1. **`load-coeffs` / `load_coeffs`** — reads `data/poly_coeff_newton.csv` (997 coefficients → degree-996 polynomial) and normalizes by the max absolute value.

2. **`horner-eval`** — evaluates the polynomial using Horner's method. `horner-eval-with-deriv` simultaneously computes value and derivative in one pass.

3. **`scan-range`** — scans an interval `[lo, hi]` at step 0.001, uses `derivative-coeffs` to find monotone sub-intervals (where sign changes in the derivative mark boundaries), then applies bisection + Newton-Raphson on each sub-interval where a sign change in the function value exists.

4. **`find-all-roots`** — dual scan strategy:
   - **Inner roots**: `scan-range` on `[-1.05, 1.05]`
   - **Outer roots**: reverses the coefficient list, scans `[-1.05, 1.05]` for roots `y` of the reversed polynomial, then maps back via `x = 1/y`. This catches large-magnitude roots because if `p(x) = 0` then the reversed polynomial has root `1/x`.
   - Deduplicates by rounding to 6 decimal places.

## Key Structural Difference Between Implementations

The Python version uses NumPy arrays throughout (`horner_eval` accepts and returns arrays), enabling vectorized evaluation. The Racket version is purely functional using lists and manual recursion — `scan-range` in Racket converts bounds to a vector for O(1) indexed access.

## Data

`data/poly_coeff_newton.csv` — one coefficient per line, highest-degree first (index 0 = leading coefficient). The polynomial is degree 996 with real coefficients spanning large magnitudes (up to ~1953), normalized before use.

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project does

Implements a polynomial root-finding algorithm in two languages — Python and Racket — for a software-languages comparison. The algorithm combines bisection, Newton-Raphson refinement, and a dual-scan strategy (inner roots + reciprocal-polynomial outer roots) to find all real roots of a high-degree polynomial loaded from a CSV file.

## Running the code

```bash
# Python (requires numpy)
python python_code.py

# Racket
racket code_racket.rkt
```

Both programs load `data/poly_coeff_newton.csv`, normalize the coefficients, find roots, and print results with timing. The Python version additionally compares against `np.roots` as a reference.

## Architecture

Both implementations share the same algorithm structure:

1. **`load-coeffs` / `load_coeffs`** — reads the CSV (one coefficient per line) and normalizes by the maximum absolute value.
2. **`horner-eval`** — evaluates the polynomial at a point using Horner's method.
3. **`horner-eval-with-deriv`** — returns `(p(x), p'(x))` in one pass for Newton-Raphson.
4. **`derivative-coeffs`** — computes the coefficient array of the formal derivative.
5. **`scan-range`** — scans `[lo, hi]` in steps of 0.001; splits into monotone segments by tracking derivative sign changes; applies bisection then Newton-Raphson in each sign-change interval.
6. **`find-all-roots`** — calls `scan-range` on `[-1.05, 1.05]` for roots near zero (inner), then repeats on the reversed coefficients (reciprocal polynomial) and inverts the results for large roots (outer).

The data file `data/poly_coeff_newton.csv` contains ~997 coefficients (one per line), representing a degree-996 polynomial used as the test case.

## Language notes

- Python uses NumPy vectorized operations for `scan_range` (the `bounds` and `vals` arrays are computed all at once; sign changes are detected with `np.where`).
- Racket uses pure recursive list processing; `build-list` + `list->vector` is used to avoid repeated list traversal during the boundary-index scan.
- Both cap bisection and Newton-Raphson at 100 iterations with the same convergence threshold (`eps = 1e-6`).

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Each project implements algorithms in **two languages**: Python and Racket (Scheme dialect).
Every project is submitted as a pair (code + submission zip).

---

## Running the Code

### Python

```powershell
python python_code.py
```

Requires `data/poly_coeff_newton.csv` (git-ignored). The script loads coefficients, runs the custom algorithm, then compares against `numpy.roots`.

### Racket

```powershell
racket code_racket.rkt
```

**Note:** `code_racket.rkt` contains a hardcoded absolute file path in `(main)` — update it to point to the local `data/poly_coeff_newton.csv` before running.

---

## Current Implementation: Polynomial Root Finding

Both files implement the same algorithm: finding all real roots of a high-degree polynomial (~996th degree) using **Bisection + Newton-Raphson + Dual Scan**.

Key architectural decisions (documented in `python_explanation.md`):

1. **Horner's method** — evaluates `p(x)` and `p'(x)` in a single O(n) pass.
2. **Sign-scan bracketing** — dense grid scan over `[-1.05, 1.05]` detecting sign changes; avoids recursive derivative approach which produces false roots at this degree.
3. **Dual scan via inverse transform** — roots with `|x| > 1` are found by reversing coefficient order (`q(y) = yⁿ·p(1/y)`), scanning for y-roots, then inverting back. This avoids float64 overflow for large x.
4. **Coefficient normalization** — divides all coefficients by their max absolute value to keep values in a numerically stable range.

The Python version vectorizes the grid evaluation and sign-change detection with numpy. The Racket version uses tail-recursive loops throughout (no `set!` or mutation).

---

## Language Rules

### Python

- Allowed external libraries: **numpy only** — for vectorization of code
- Forbidden: `numpy.linalg`, `numpy.polynomial`, and similar sub-modules

### Racket

- Allowed external libraries: **flomat only** — for vectorization of code
- Forbidden: `set!` and any mutation functions — no mutable state

---

## Code Requirements (both languages)

- Code must be **general and reusable** — a valid template, no hardcoded values
- All documentation must follow a **single uniform style**
- **Delete unused code** — no dead code left in files
- Use the **methodologies taught in the course**
- **No copying code** from external sources

---

## Submission Requirements

The submission zip must include:

1. Explanation of the algorithms implemented
2. Advantages and disadvantages of **your specific use** of each language (not general language comparison)
3. Optimization techniques demonstrated in each language
4. Speed comparison between your implementation and the given input — if there's a difference, explain why

---

## File Structure Convention

- Python files: `*_code.py`
- Racket files: `*_code.rkt`
- Explanation docs: `*_explanation.md`
- Data files: `data/` (git-ignored)
- Skills/prompts: `Skills/` (git-ignored)

# Software Languages Project — CLAUDE.md

## Project Overview
Each project implements algorithms in **two languages**: Python and Racket (Scheme dialect).
Every project is submitted as a pair (code + submission zip).

---

## Language Rules

### Python
- Allowed external libraries: **numpy only** — for vectorization of code
- Forbidden: `numpy.linalg`, `numpy.polynomial`, and similar sub-modules
- No other external libraries

### Racket
- Allowed external libraries: **flomat only** — for vectorization of code
- Forbidden: functions with side effects — no `set!` and similar mutation functions
- No use of built-in mutable state

---

## Code Requirements (apply to both languages)

- Code must be **general and reusable** — useful for the full scope of the course
- Code must be a **valid template** — only receives input from the project, no hardcoded values
- All documentation must follow a **single uniform style**
- **Delete unused code** — no dead code left in files
- Use the **methodologies taught in the course**
- **No copying code** from external sources or existing implementations
- **No using AI to write the code** — Claude can help understand and explain, but not generate the implementation

---

## Submission Requirements

The submission (zip with code + document) must include:
1. Explanation of the algorithms implemented
2. Advantages and disadvantages of **your specific use** of each language (not general language comparison)
3. Optimization techniques demonstrated in each language
4. Speed comparison between your implementation and the given input — if there's a difference, explain why

---

## File Structure Convention
- Python files: `*_code.py`
- Racket files: `*_code.rkt`
- Data files: `data/` (git-ignored, not committed)
- Skills/prompts: `Skills/` (git-ignored, not committed)

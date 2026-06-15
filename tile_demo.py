import os
import time
import numpy as np
from python_code import load_coeffs, find_all_roots


def tiled_real_roots(block_coeffs, t, eps=1e-7):
    """
    Real roots of np.tile(block_coeffs, t) WITHOUT brute force.

    tile(C, t) as a polynomial equals  P(x) * (x^(L*t) - 1) / (x^L - 1),
    where P is the block polynomial and L = len(C).  So its real roots are
    the real roots of P plus the real roots of that geometric factor:

        extra real root x = -1   iff   L is odd and t is even
        (otherwise the factor contributes no real root)

    We therefore solve only the small block P (fast) and add -1 when needed.
    """
    L = len(block_coeffs)
    roots = find_all_roots(block_coeffs, eps)
    if L % 2 == 1 and t % 2 == 0:
        roots = sorted(set(roots + [-1.0]))
    return roots


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    block = load_coeffs(os.path.join(script_dir, 'data', 'poly_coeff_newton.csv'))

    # --- verification on small tiles: shortcut must equal numpy brute force ---
    print("--- verification (small tiles, vs np.roots) ---")
    small = np.array([1.0, -2.5, 1.0])              # P(x) = (x-0.5)(x-2), L=3
    for t in (2, 3, 4, 5):
        full = np.tile(small, t)
        brute = sorted(round(r.real, 6) for r in np.roots(full) if abs(r.imag) < 1e-9)
        fast = tiled_real_roots(small, t)
        print(f"  tile={t} deg={len(full)-1:>3}  shortcut={fast}  numpy={brute}  match={fast == brute}")

    # --- the real request: tile(coeffs, 1000) -> degree ~997000, instantly ---
    print("\n--- np.tile(coeffs, 1000): degree", len(block) * 1000 - 1, "---")
    t0 = time.perf_counter()
    roots_1000 = tiled_real_roots(block, 1000)
    elapsed = time.perf_counter() - t0
    print(f"Real roots: {roots_1000}")
    print(f"Time: {elapsed:.4f} seconds   (brute force would need ~4 TB RAM)")

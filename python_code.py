import os
import math
import numpy as np
import time


def load_coeffs(filename):
    coeffs = np.loadtxt(filename)
    return coeffs / np.max(np.abs(coeffs))


def derivative_coeffs(coeffs):
    n = len(coeffs) - 1
    if n == 0:
        return np.array([0.0])
    return coeffs[:-1] * np.arange(n, 0, -1, dtype=np.float64)


def coeff_bound(coeffs):
    a_n = float(coeffs[0])
    n = len(coeffs) - 1
    vals = [
        (abs(float(coeffs[k]) / a_n)) ** (1.0 / k)
        for k in range(1, n + 1) if coeffs[k] != 0.0
    ]
    return 2.0 * max(vals) if vals else 1.0


def make_evaluator(poly):
    n = len(poly) - 1
    P = [float(v) for v in poly]
    P0, P1 = P[0], tuple(P[1:])
    R = P[::-1]
    R0, R1 = R[0], tuple(R[1:])
    isfinite = math.isfinite

    def f(x):
        if -1.0 <= x <= 1.0:
            p = P0
            dp = 0.0
            for c in P1:
                dp = dp * x + p
                p = p * x + c
            if dp == 0.0:
                return p, None, False
            return p, p / dp, True

        u = 1.0 / x
        Q = R0
        dQ = 0.0
        for c in R1:
            dQ = dQ * u + Q
            Q = Q * u + c
        if not (isfinite(Q) and isfinite(dQ)):
            return None, None, False
        sx = 1.0 if (x > 0 or n % 2 == 0) else -1.0
        sval = sx * Q
        denom = n * Q - u * dQ
        if denom == 0.0 or not isfinite(denom):
            return sval, None, False
        return sval, x * Q / denom, True

    return f


def _bisection(f, a, b, eps, sa):
    for _ in range(50):
        mid = (a + b) / 2.0
        if (b - a) / 2.0 < eps:
            return mid
        sm, _, _ = f(mid)
        if sm is None or sm == 0.0:
            return mid
        if sm * sa > 0:
            a, sa = mid, sm
        else:
            b = mid
    return (a + b) / 2.0


def solve_in_bracket(f, a, b, eps, sa):
    x = (a + b) / 2.0
    for _ in range(40):
        _, ratio, ok = f(x)
        if not ok or ratio is None:
            return _bisection(f, a, b, eps, sa)
        x_new = x - ratio
        if not math.isfinite(x_new) or x_new <= a or x_new >= b:
            return _bisection(f, a, b, eps, sa)
        if abs(x_new - x) < eps:
            return x_new
        x = x_new
    return _bisection(f, a, b, eps, sa)


def _roots_from_critical(poly, A, B, eps, critical_pts):
    f = make_evaluator(poly)
    pts = [A] + sorted(x for x in critical_pts if A < x < B) + [B]
    svals = [f(x)[0] for x in pts]

    roots = []
    for i in range(len(pts) - 1):
        sl, sr = svals[i], svals[i + 1]
        if sl is None or sr is None:
            continue
        if sl * sr < 0:
            r = solve_in_bracket(f, pts[i], pts[i + 1], eps, sl)
            if r is not None and (not roots or abs(roots[-1] - r) > eps):
                roots.append(r)
    return sorted(roots)


def find_roots_in_interval(coeffs, A, B, eps):
    n = len(coeffs) - 1

    if n <= 0:
        return []
    if n == 1:
        x = float(-coeffs[1] / coeffs[0])
        return [x] if A <= x <= B else []
    if n == 2:
        a_c, b_c, c_c = float(coeffs[0]), float(coeffs[1]), float(coeffs[2])
        disc = b_c * b_c - 4.0 * a_c * c_c
        if disc < 0:
            return []
        sq = np.sqrt(max(disc, 0.0))
        xs = {(-b_c - sq) / (2.0 * a_c), (-b_c + sq) / (2.0 * a_c)}
        return sorted(x for x in xs if A <= x <= B)

    chain = []
    d = coeffs
    while len(d) > 2:
        d = derivative_coeffs(d)
        m = np.max(np.abs(d))
        if m > 0:
            d = d / m
        chain.append(d)

    lin = chain[-1]
    if abs(lin[0]) < 1e-15:
        current = []
    else:
        x0 = float(-lin[1] / lin[0])
        current = [x0] if A < x0 < B else []

    for poly in reversed(chain[:-1]):
        current = _roots_from_critical(poly, A, B, eps, current)

    return _roots_from_critical(coeffs, A, B, eps, current)


def find_all_roots(coeffs, eps):
    R = coeff_bound(coeffs)
    A, B = -R - 0.1, R + 0.1
    roots = find_roots_in_interval(coeffs, A, B, eps)
    return sorted(set(float(np.round(r, 6)) for r in roots))


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'data', 'poly_coeff_newton.csv')
    eps = 1e-7

    try:
        poly_coeffs = load_coeffs(file_path)

        print("--- Custom Algorithm (Derivative Isolation + Newton/Bisection) ---")
        print(f"Search interval from coefficient bound: "
              f"[-{coeff_bound(poly_coeffs):.4f}, {coeff_bound(poly_coeffs):.4f}]")
        t0 = time.perf_counter()
        my_roots = find_all_roots(poly_coeffs, eps)
        elapsed = time.perf_counter() - t0
        print(f"Number of real roots found: {len(my_roots)}")
        print(f"Roots: {my_roots}")
        print(f"Runtime: {elapsed:.4f} seconds\n")

        print("--- NumPy np.roots ---")
        t1 = time.perf_counter()
        np_all = np.roots(poly_coeffs)
        real_np = sorted(set(
            float(np.round(r.real, 6))
            for r in np_all if abs(r.imag) < 1e-8
        ))
        elapsed_np = time.perf_counter() - t1
        print(f"Number of real roots found: {len(real_np)}")
        print(f"Roots: {real_np}")
        print(f"NumPy Runtime: {elapsed_np:.4f} seconds\n")

        if my_roots == real_np:
            print("SUCCESS - Roots match exactly.")
        elif len(my_roots) == len(real_np):
            print("WARNING - Root count matches but values differ.")
        else:
            print(
                f"WARNING - Root count differs: custom={len(my_roots)}, numpy={len(real_np)}")

    except Exception:
        import traceback
        traceback.print_exc()

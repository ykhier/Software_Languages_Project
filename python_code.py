import os
import numpy as np
import time


def load_coeffs(filename):
    coeffs = np.loadtxt(filename)

    return coeffs / np.max(np.abs(coeffs))


def horner_eval(coeffs, x):
    res = coeffs[0]
    for c in coeffs[1:]:
        res = res * x + c
    return res


def horner_eval_with_deriv(coeffs, x):
    res = coeffs[0]
    der = 0.0
    for c in coeffs[1:]:
        der = der * x + res
        res = res * x + c
    return res, der


def bisection(coeffs, a, b, eps):
    fa = horner_eval(coeffs, a)
    for _ in range(100):
        mid = (a + b) / 2
        fmid = horner_eval(coeffs, mid)

        if np.isnan(fmid):
            return mid

        if abs(fmid) < eps or (b - a) / 2 < eps:
            return mid

        if np.sign(fmid) == np.sign(fa):
            a = mid
            fa = fmid
        else:
            b = mid
    return (a + b) / 2


def newton_raphson(coeffs, x0, eps):
    x = x0
    for _ in range(50):
        fx, dfx = horner_eval_with_deriv(coeffs, x)

        if np.isinf(fx) or np.isinf(dfx) or np.isnan(fx) or np.isnan(dfx) or abs(dfx) < 1e-15:
            return x

        x_new = x - fx / dfx

        if abs(x_new - x) < eps:
            return x_new
        x = x_new
    return x


def derivative_coeffs(coeffs):
    n = len(coeffs) - 1
    if n == 0:
        return np.array([0.0])
    # כל מקדם מוכפל בחזקה המתאימה: [n*a0, (n-1)*a1, ..., 1*a_{n-1}]
    powers = np.arange(n, 0, -1)
    return coeffs[:-1] * powers


def scan_range(coeffs, lo, hi, eps):
    step = 0.001
    # שימוש ב-linspace בטוח יותר מ-arange למניעת פספוס קצוות בגלל עיגול עשרוני
    num_points = int(round((hi - lo) / step)) + 1
    bounds = np.linspace(lo, hi, num_points)
    vals = horner_eval(coeffs, bounds)

    # --- שלב 1: מציאת גבולות קטעי מונוטוניות לפי שורשי f' ---
    # לפי ההערה: כל שורש x של f מקיים f'(x)=0 או נמצא בין שני שורשים עוקבים של f'.
    # f מונוטונית בין נקודות קריטיות עוקבות, ולכן בכל קטע כזה יש לכל היותר שורש אחד.
    # הגבולות הם אינדקסי הרשת משני צדי כל שינוי סימן של f' — שימוש ב-vals (f ברשת)
    # מבטיח יציבות נומרית מלאה, ללא חישוב f בנקודות קריטיות מדויקות שבהן עלול להיות ביטול.
    dcoeffs = derivative_coeffs(coeffs)
    dvals = horner_eval(dcoeffs, bounds)
    dsigns = np.sign(dvals)

    boundary_set = {0, num_points - 1}
    dchanges = np.where(dsigns[:-1] * dsigns[1:] < 0)[0]
    for i in dchanges:
        boundary_set.add(int(i))
        boundary_set.add(int(i) + 1)
    boundary_set.update(np.where(dvals == 0.0)[0].tolist())
    boundary_indices = sorted(boundary_set)

    # --- שלב 2: בדיקת שינוי סימן של f בין גבולות עוקבים ---
    # כל קטע חד-מונוטוני → bisection+Newton מוצא את השורש היחיד
    roots = []

    for j in range(len(boundary_indices) - 1):
        a_idx = boundary_indices[j]
        b_idx = boundary_indices[j + 1]
        fa = vals[a_idx]
        fb = vals[b_idx]

        if np.isnan(fa) or np.isnan(fb) or np.isinf(fa) or np.isinf(fb):
            continue

        # אפס מדויק בנקודת הגבול (שורש כפול: f=0 ו-f'=0 באותה נקודה)
        if fa == 0.0:
            roots.append(float(bounds[a_idx]))

        # שינוי סימן → שורש יחיד בקטע המונוטוני, חידוד ב-bisection+Newton
        if np.sign(fa) * np.sign(fb) < 0:
            root_bi = bisection(coeffs, bounds[a_idx], bounds[b_idx], eps)
            root_final = newton_raphson(coeffs, root_bi, eps)
            roots.append(root_final)

    # בדיקת נקודת הקצה האחרונה
    if vals[boundary_indices[-1]] == 0.0:
        roots.append(float(bounds[boundary_indices[-1]]))

    return roots


def find_all_roots(coeffs, eps):
    # 1. מציאת שורשים פנימיים (הגדלנו מעט את הטווח כדי לכלול את 1 ו- -1 בבטחה)
    inner_roots = scan_range(coeffs, -1.05, 1.05, eps)

    # 2. הפיכת הפולינום למציאת שורשים חיצוניים (עבור y=1/x)
    reversed_coeffs = coeffs[::-1]
    y_roots = scan_range(reversed_coeffs, -1.05, 1.05, eps)

    outer_roots = []
    for y in y_roots:
        if abs(y) > eps:
            x = 1.0 / y
            outer_roots.append(x)

    # 3. איחוד ועיבוד סופי - ה-set יעלים את כל הכפילויות שנוצרו בגלל החפיפה בטווחי החיפוש
    all_roots = inner_roots + outer_roots
    valid_roots = [r for r in all_roots if not np.isnan(r) and not np.isinf(r)]
    return sorted(list(set(float(np.round(r, 6)) for r in valid_roots)))


# --- הרצה והשוואה ---
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'data', 'poly_coeff_newton.csv')
    eps = 1e-6

    try:
        poly_coeffs = load_coeffs(file_path)

        print("--- Custom Algorithm (Bisection + Newton-Raphson + Dual Scan) ---")
        t0 = time.perf_counter()
        my_roots = find_all_roots(poly_coeffs, eps)
        elapsed_my = time.perf_counter() - t0

        print(f"Number of real roots found: {len(my_roots)}")
        print(f"Roots: {my_roots}")
        print(f"Custom Algorithm Runtime: {elapsed_my:.4f} seconds\n")

        print("--- Numpy np.roots Algorithm ---")
        t1 = time.perf_counter()
        numpy_roots = np.roots(poly_coeffs)

        real_numpy_roots = np.real(
            numpy_roots[np.abs(numpy_roots.imag) < 1e-8])
        real_numpy_roots = sorted(
            list(set(float(np.round(r, 6)) for r in real_numpy_roots)))
        elapsed_np = time.perf_counter() - t1

        print(f"Number of real roots found: {len(real_numpy_roots)}")
        print(f"Roots: {real_numpy_roots}")
        print(f"Numpy np.roots Runtime: {elapsed_np:.4f} seconds\n")

        # בדיקת תאימות סופית
        if len(my_roots) == len(real_numpy_roots):
            is_match = np.allclose(my_roots, real_numpy_roots, atol=1e-5)
            print(
                f"MATCH RESULT: {'SUCCESS - Roots are identical!' if is_match else 'WARNING - Roots differ.'}")
        else:
            print("WARNING - Algorithms found a different number of real roots.")

    except Exception as e:
        print(f"An error occurred: {e}")

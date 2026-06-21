import numpy as np
import time
import os


def hornerEval(coeffs, x):
    res = coeffs[0]
    for c in coeffs[1:]:
        res = res * x + c
    return res


def hornerEvalWithDeriv(coeffs, x):
    res = coeffs[0]
    der = 0.0
    for c in coeffs[1:]:
        der = der * x + res
        res = res * x + c
    return res, der


def derivativeCoefficients(coeffs):
    n = len(coeffs) - 1
    return [coeffs[i] * (n - i) for i in range(n)]


def findFiniteEdge(coeffs, a, b):
    fVal = hornerEval(coeffs, a)
    if np.isfinite(fVal):
        return a, fVal

    for _ in range(100):
        a = (a + b) / 2.0
        fVal = hornerEval(coeffs, a)
        if np.isfinite(fVal):
            return a, fVal

    return None, None


def safeBracket(coeffs, a, b):
    left, fLeft = findFiniteEdge(coeffs, a, b)
    if left is None:
        return None, None, None, None

    right, fRight = findFiniteEdge(coeffs, b, left)
    if right is None:
        return None, None, None, None

    return left, right, fLeft, fRight


def newtonRaphson(coeffs, x0, eps):
    x = x0
    for _ in range(100):
        fx, dfx = hornerEvalWithDeriv(coeffs, x)

        if not np.isfinite(fx) or not np.isfinite(dfx) or dfx == 0:
            return None

        if abs(fx) < eps:
            return x

        xnew = x - fx / dfx

        if not np.isfinite(xnew):
            return None

        if abs(xnew - x) < eps:
            return xnew
        x = xnew

    return None


def bisection(coeffs, a, b, eps):
    fa = hornerEval(coeffs, a)

    while (b - a) / 2.0 > eps:
        mid = (a + b) / 2.0
        fmid = hornerEval(coeffs, mid)

        if fmid == 0:
            return mid
        if fa * fmid < 0:
            b = mid
        else:
            a = mid
            fa = fmid
    return (a + b) / 2.0


def firstDegree(coeff0, coeff1):
    root = -coeff1 / coeff0
    return [root]


def secondDegree(coeff0, coeff1, coeff2):
    a, b, c = coeff0, coeff1, coeff2
    discriminant = b**2 - 4 * a * c
    roots = []
    sqrtDisc = np.sqrt(discriminant)
    r1 = (-b - sqrtDisc) / (2.0 * a)
    r2 = (-b + sqrtDisc) / (2.0 * a)
    roots = [r1, r2]
    return roots


def findRoots(coeffs, a, b, eps):
    polyDegree = len(coeffs) - 1

    if polyDegree <= 0:
        return []

    if polyDegree == 1:
        return firstDegree(coeffs[0], coeffs[1])

    if polyDegree == 2:
        return secondDegree(coeffs[0], coeffs[1], coeffs[2])

    chain = [coeffs]
    current = coeffs
    while len(current) > 3:
        current = derivativeCoefficients(current)
        chain.append(current)

    lowest = chain[-1]
    roots = secondDegree(lowest[0], lowest[1], lowest[2])

    for poly in reversed(chain[:-1]):
        dcoeffsRoots = [r for r in roots if a <= r <= b]
        splitPoints = [a] + sorted(dcoeffsRoots) + [b]

        roots = []
        for i in range(len(splitPoints) - 1):
            lo = splitPoints[i]
            hi = splitPoints[i + 1]

            finiteBracket = safeBracket(poly, lo, hi)
            if finiteBracket[0] is None:
                continue

            lo, hi, fa, fb = finiteBracket

            if fa * fb <= 0:
                x0 = (lo + hi) / 2.0
                root = newtonRaphson(poly, x0, eps)

                if root is None:
                    root = bisection(poly, lo, hi, eps)

                if np.isfinite(root) and a <= root <= b:
                    roots.append(root)

    return roots


def scanPage(coeffs, eps):
    innerRoots = findRoots(coeffs, -1.0, 1.0, eps)
    reversedCoeffs = list(reversed(coeffs))
    outerRootsBounds = findRoots(reversedCoeffs, -1.0, 1.0, eps)

    outerRoots = []
    for y in outerRootsBounds:
        if abs(y) > 1e-12:
            x = 1.0 / y
            outerRoots.append(x)

    allRoots = innerRoots + outerRoots
    roundedRoots = []
    for r in allRoots:
        roundedRoots.append(float(np.round(r, 6)))

    return sorted(set(roundedRoots))


def loadCoeffs(path):
    with open(path) as f:
        return [float(line.strip()) for line in f if line.strip()]


def main():
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    csvPath = os.path.join(scriptDir, 'data', 'poly_coeff_newton.csv')

    print("--- Custom Algorithm (CSV file): ---")
    csvCoeffs = loadCoeffs(csvPath)
    t0 = time.perf_counter()
    csvRoots = scanPage(csvCoeffs, 1e-12)
    csvTime = time.perf_counter() - t0
    print(f"Number of real roots found: {len(csvRoots)}")
    print(f"Roots: {csvRoots}")
    print(f"Custom Algorithm Runtime: {csvTime:.4f} seconds\n")

    print("--- Numpy np.roots Algorithm ---")
    t2 = time.perf_counter()
    numpyRoots = np.roots(csvCoeffs)
    realNumpyRoots = np.real(numpyRoots[np.abs(numpyRoots.imag) < 1e-8])
    realNumpyRoots = sorted(list(set(float(np.round(r, 6))
                            for r in realNumpyRoots)))
    npTime = time.perf_counter() - t2
    print(f"Number of real roots found: {len(realNumpyRoots)}")
    print(f"Roots: {realNumpyRoots}")
    print(f"Numpy np.roots Runtime: {npTime:.4f} seconds\n")

    print("--- Comparison (Custom vs Numpy) ---")
    if csvRoots == realNumpyRoots:
        print("MATCH - both algorithms found the same roots.")
    else:
        print("MISMATCH - the outputs differ.")


if __name__ == "__main__":
    main()

"""
Lab 1 starter code.
"""


def bisection(f, a, b, tol=1e-6, max_iters=50):
    """
    Implementation of the Bisection root finding algorithm.

    Parameters
    ----------
    f
        A callable object representing a univariate function.
    a
        The lower guess (should be set such that f(a) < 0).
    b
        The upper guess (should be set such that f(b) > 0).
    tol, optional
        Tolerance for the solver, by default 1e-6.
    max_iters, optional
        Maximum number of iterations before raising RuntimeError, by default 50.

    Raises
    ------
    RuntimeError
        If number of iterations exceeds max_iters.
    """
    fa = f(a)
    fb = f(b)
    if abs(fa) <= tol:
        return a
    if abs(fb) <= tol:
        return b
    if a >= b or fa * fb > 0:
        raise ValueError("a and b must bracket a root")

    iterations = 0
    while iterations < max_iters:
        midpoint = (a + b) / 2
        fm = f(midpoint)
        if abs(fm) <= tol or (b - a) / 2 <= tol:
            return midpoint
        if fa * fm < 0:
            b = midpoint
        else:
            a = midpoint
            fa = fm
        iterations += 1

    raise RuntimeError("Bisection did not converge within max_iters")


def newton(f, fp, x0, tol=1e-6, max_iters=50):
    """
    Implementation of Newton's root finding algorithm.

    Parameters
    ----------
    f
        A callable object representing a univariate function.
    fp
        A callable object representing the first derivative (f prime) of the
        univariate function.
    x0
        Initial guess.
    tol, optional
        Tolerance for the solver, by default 1e-6.
    max_iters, optional
        Maximum number of iterations before raising RuntimeError, by default 50.

    Raises
    ------
    RuntimeError
        If number of iterations exceeds max_iters.
    """
    x = x0
    for _ in range(max_iters):
        fx = f(x)
        if abs(fx) <= tol:
            return x
        slope = fp(x)
        if slope == 0:
            raise ZeroDivisionError("Newton's method encountered a zero derivative")
        x = x - fx / slope

    if abs(f(x)) <= tol:
        return x
    raise RuntimeError("Newton's method did not converge within max_iters")

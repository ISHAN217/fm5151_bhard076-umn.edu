import root

y = 27
f = lambda x: x**3 - y
fp = lambda x: 3 * x**2
ans = 3


def test_bisection_converge_increasing_func():
    tol = 1e-10
    result = root.bisection(f, a=0, b=50, tol=tol, max_iters=100)
    assert abs(result - ans) < tol


def test_bisection_converge_decreasing_func():
    tol = 1e-10
    result = root.bisection(lambda x: -f(x), a=0, b=50, tol=tol, max_iters=100)
    assert abs(result - ans) < tol


def test_bisection_max_iters_hit():
    runtime_error = False
    try:
        _ = root.bisection(f, a=-10000, b=10000, tol=1e-10, max_iters=2)
    except RuntimeError:
        runtime_error = True
    assert runtime_error


def test_newton_converge_increasing_func():
    tol = 1e-10
    result = root.newton(f, fp, x0=50, tol=tol, max_iters=100)
    assert abs(result - ans) < tol


def test_newton_converge_decreasing_func():
    tol = 1e-10
    result = root.newton(
        lambda x: -f(x), lambda x: -fp(x), x0=50, tol=tol, max_iters=100
    )
    assert abs(result - ans) < tol


def test_newton_max_iters():
    runtime_error = False
    try:
        _ = root.newton(f, fp, x0=50, tol=1e-10, max_iters=2)
    except RuntimeError:
        runtime_error = True
    assert runtime_error


if __name__ == "__main__":
    tests = [
        (key, obj)
        for (key, obj) in locals().items()
        if key.startswith("test") and callable(obj)
    ]
    ok = "\033[92m"
    fail = "\033[91m"
    end = "\033[0m"
    for name, fn in tests:
        try:
            fn()
            print(f"({name}) [{ok}PASS{end}]{end}")
        except Exception as e:
            print(f"({name}) [{fail}FAIL{end}]: ({type(e).__name__}) {str(e)}")

#Bisection method
def bisection_method(f, a, b, tolerance):
    if f(a) == 0 or f(b) == 0:
        if f(a) == 0:
            print(f"Root is: {a}")
        if f(b) == 0:
            print(f"Root is: {b}")
        return 

    if f(a) * f(b) >= 0:
        print("The function must have opposite signs at a and b to bracket a root.")
        return None

    iteration = 0
    print("Starting Bisection Method...")
    while (b - a) / 2 > tolerance:
        c = (a + b) / 2
        print(f"Iteration {iteration}: a = {a:.6f}, b = {b:.6f}, c = {c:.6f}, f(c) = {f(c):.6e}")

        # Check if the midpoint is a root
        if abs(f(c)) < tolerance:
            print(f"Root found at c = {c} (tolerance reached).")
            return c

        if f(a) * f(c) < 0:
            b = c
        else:
            a = c

        iteration += 1

    c = (a + b) / 2
    print(f"Approximate root after {iteration} iterations: c = {c}")
    return c

# Test Function
def f(x):
    return x**3 - 6*x**2 + 11*x - 6

# Test Inputs
a = 1
b = 2
tolerance = 1e-6

root = bisection_method(f, a, b, tolerance)
if root is not None:
    print(f"Approximate root: {root}")

# How does the choice of [a,b] affect convergence?

# To "bracket" root first condition is to have opposite signs for f(a) and f(b)
# to ensure that interval values crosses x axis
# The larger interval -> the more iterations spent to zoom in on the root.
# The number of iterations can be computed by formula log2((b-a)/tolerance)
# If f(a) * f(b) >= 0 it means that y values has same sign,
# therefore there might be no root in the interval or here’s an even number of roots in the interval,
# and the method might fail to detect one.






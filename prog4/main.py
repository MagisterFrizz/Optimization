from math import sqrt


class Solver:
    def __init__(self, func):
        self.func = func

    def bisection_method(self, a: float, b: float, tolerance: float) -> float:
        """
        How does the choice of [a,b] affect convergence?
        To "bracket" root first condition is to have opposite signs for func(a) and func(b)
        to ensure that interval values crosses x axis
        The larger interval -> the more iterations spent to zoom in on the root.
        The number of iterations can be computed by formula log2((b-a)/tolerance)
        If func(a) * func(b) >= 0 it means that y values has same sign,
        therefore there might be no root in the interval or here's an even number of roots in the interval,
        and the method might fail to detect one.
        """

        func = self.func

        if func(a) == 0:
            print(f"Root is: {a}")
            return a
        elif func(b) == 0:
            print(f"Root is: {b}")
            return b

        if func(a) * func(b) >= 0:
            print("The function must have opposite signs at a and b to bracket a root.")
            return None

        iteration = 0
        print("Starting Bisection Method...")
        while (b - a) / 2 > tolerance:
            c = (a + b) / 2
            print(f"Iteration {iteration}: a = {a:.6f}, b = {b:.6f}, c = {c:.6f}, func(c) = {func(c):.6e}")

            # Check if the midpoint is a root
            if abs(func(c)) < tolerance:
                print(f"Root found at c = {c} (tolerance reached).")
                return c

            if func(a) * func(c) < 0:
                b = c
            else:
                a = c

            iteration += 1

        c = (a + b) / 2
        print(f"Approximate root after {iteration} iterations: c = {c}")
        return c

    def golden_section_method(self, a: float, b: float, type: int = 1, e: float = 1e-6) -> tuple[float, float]:
        """
        ### Input and output
        Takes the interval [a, b] for some function and returns maxima and maximum (if type is 1)\n
        or minima and minimum (if type is -1)
        ### Idea of the method
        The golden section method proposes is to save computations by reusing 
        the discarded value in the immediately succeeding iteration.
        """

        # Define function and borders of given interval [a, b]
        func = self.func
        x_l, x_r = a, b

        # Iteration 0
        x1 = x_r - (sqrt(5) - 1) / 2 * (x_r - x_l)
        x2 = x_l + (sqrt(5) - 1) / 2 * (x_r - x_l)

        # Change of interval's borders
        if type * func(x1) > type * func(x2):
            x_r = x2
        elif type * func(x1) < type * func(x2):
            x_l = x1
        else: 
            x_l, x_r = x1, x2

        i = 0

        # Next Iterations
        while x_r - x_l > e:

            # Use of unused value
            if type * func(x1) > type * func(x2):
                x2 = x1
                x1 = x_r - (sqrt(5) - 1) / 2 * (x_r - x_l)
            elif type * func(x1) < type * func(x2):
                x1 = x2
                x2 = x_l + (sqrt(5) - 1) / 2 * (x_r - x_l)
            else:
                x1 = x_r - (sqrt(5) - 1) / 2 * (x_r - x_l)
                x2 = x_l + (sqrt(5) - 1) / 2 * (x_r - x_l)

            # Change of interval's borders
            if type * func(x1) > type * func(x2):
                x_r = x2
            elif type * func(x1) < type * func(x2):
                x_l = x1
            else: 
                x_l, x_r = x1, x2

            i += 1

        # Console output
        if type > 0:
            print(f"Maximum: {(x_l + x_r) / 2:.5f},\nMaxima: {func((x_l + x_r) / 2):.5f}")
        else:
            print(f"Minimum: {(x_l + x_r) / 2:.5f},\nMinima: {func((x_l + x_r) / 2):.5f}")

        # Return of x and f(x)
        return x_l, func(x_l)
            

def f2(x):
    return (x - 2)**2 + 3

def f3(x):
    return -x**2 + 4*x + 1

solver = Solver(f2)
x, y = solver.golden_section_method(0, 5, -1, 1e-5)

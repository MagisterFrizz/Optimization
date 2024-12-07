from math import sqrt


class Solver:
    def bisection_method(self, f, a: float, b: float, tolerance: float) -> float:
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

        print("Bisection Method:")

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
            print(f"Iteration {iteration}: a = {a:.6f}, b = {b:.6f}, c = {c:.6f}, func(c) = {f(c):.6e}")

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

    def golden_section_method(self, f, a: float, b: float, type: int = 1, e: float = 1e-6, 
                              log: bool = True) -> tuple[float, float]:
        """
        ### Input and output
        Takes the interval [a, b] for some function and returns maxima and maximum (if type is 1)\n
        or minima and minimum (if type is -1)
        ### Idea of the method
        The golden section method proposes is to save computations by reusing 
        the discarded value in the immediately succeeding iteration.
        """
        if log:
            print("Golden Section Method:")

        # Define borders of given interval [a, b]
        x_l, x_r = a, b

        # Iteration 0
        x1 = x_r - (sqrt(5) - 1) / 2 * (x_r - x_l)
        x2 = x_l + (sqrt(5) - 1) / 2 * (x_r - x_l)

        # Change of interval's borders
        if type * f(x1) > type * f(x2):
            x_r = x2
        elif type * f(x1) < type * f(x2):
            x_l = x1
        else: 
            x_l, x_r = x1, x2

        i = 0

        # Next Iterations
        while x_r - x_l > e:

            # Use of unused value
            if type * f(x1) > type * f(x2):
                x2 = x1
                x1 = x_r - (sqrt(5) - 1) / 2 * (x_r - x_l)
            elif type * f(x1) < type * f(x2):
                x1 = x2
                x2 = x_l + (sqrt(5) - 1) / 2 * (x_r - x_l)
            else:
                x1 = x_r - (sqrt(5) - 1) / 2 * (x_r - x_l)
                x2 = x_l + (sqrt(5) - 1) / 2 * (x_r - x_l)

            # Change of interval's borders
            if type * f(x1) > type * f(x2):
                x_r = x2
            elif type * f(x1) < type * f(x2):
                x_l = x1
            else: 
                x_l, x_r = x1, x2

            i += 1

        # Console output
        if log:
            if type > 0:
                print(f"Maximum: {(x_l + x_r) / 2:.5f},\nMaxima: {f((x_l + x_r) / 2):.5f}\n")
            else:
                print(f"Minimum: {(x_l + x_r) / 2:.5f},\nMinima: {f((x_l + x_r) / 2):.5f}\n")

        # Return of x and f(x)
        return x_l, f(x_l)
            
    def gradient_ascent_method(self, f, df, x0: float, e: float = 1e-4,
                                log: bool = True) -> tuple[float, float]:
        """
        ### Input and output
        Takes the function, it's derivative and initial point x0 and returns optima and optimum of the function.\n
        ### Idea of the method
        Gradient ascent generates successive points in the direction of the gradient of the function.
        """
        if log:
            print("Gradient Ascent Method:")

        x = x0

        # Iteration 1
        def h(r):
            return f(x + r * df(x))

        # Find optimal coeficient r for gradient ascent
        r_opt, _ = self.golden_section_method(h, -100, 100, log=False)
        x_new = x + r_opt * df(x)

        # Next iterations
        while abs(x - x_new) > e:

            def h(r):
                return f(x_new + r * df(x_new))
            
            x = x_new

            # Find optimal coeficient r for gradient ascent
            r_opt, _ = self.golden_section_method(h, -100, 100, log=False)
            x_new = x + r_opt * df(x)
        
        if log:
            print(f"Optimum: {x:.5f},\nOptima: {f(x):.5f}\n")

        return x, f(x)

def f1(x):
    return x**3 - 6*x**2 + 11*x - 6

def f2(x):
    return (x - 2)**2 + 3

def f3(x):
    return -x**2 + 4*x + 1

def df3(x):
    return -2*x + 4

solver = Solver()

root = solver.bisection_method(f1, 1, 2, 1e-6)

x, y = solver.golden_section_method(f2, 0, 5, -1, 1e-5)

x, y = solver.gradient_ascent_method(f3, df3, 0)

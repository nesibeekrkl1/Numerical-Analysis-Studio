import numpy as np

class NumericalAnalysisEngine:
    @staticmethod
    def f(x, func_text):
        """Safely converts the user's string input into a Numpy-supported executable function."""
        # Mapping Numpy functions to work directly inside eval
        math_dict = {
            "x": x,
            "np": np,
            "sin": np.sin,
            "cos": np.cos,
            "tan": np.tan,
            "log": np.log,
            "exp": np.exp,
            "sqrt": np.sqrt,
            "pi": np.pi
        }
        # Securing the evaluation by shutting down __builtins__
        return eval(func_text, {"__builtins__": None}, math_dict)

    @classmethod
    def numerical_derivative(cls, x, func_text, h=0.0001):
        """Calculates f'(x) using the central difference method."""
        try:
            return (cls.f(x + h, func_text) - cls.f(x - h, func_text)) / (2 * h)
        except:
            return float('nan')

    @classmethod
    def trapezoidal_integral(cls, a, b, func_text, n=100):
        """Calculates the definite integral using the trapezoidal rule."""
        try:
            h = (b - a) / n
            total = (cls.f(a, func_text) + cls.f(b, func_text)) / 2.0
            for i in range(1, n):
                total += cls.f(a + i * h, func_text)
            return total * h
        except:
            return float('nan')

    @classmethod
    def auto_find_interval(cls, func_text, start=0.0, step=0.5, max_search=200):
        """Scans for an interval with opposite signs to bracket a root for the Bisection method."""
        for i in range(max_search):
            x1 = start + (i * step)
            x2 = x1 + step
            try:
                if cls.f(x1, func_text) * cls.f(x2, func_text) <= 0:
                    return x1, x2
            except: 
                pass

            x1_left = start - (i * step)
            x2_left = x1_left - step
            try:
                if cls.f(x1_left, func_text) * cls.f(x2_left, func_text) <= 0:
                    return x2_left, x1_left
            except: 
                pass
        return None, None

    @classmethod
    def find_root_bisection(cls, func_text, tolerance=0.000001):
        """Finds a root using the Bisection method."""
        a, b = cls.auto_find_interval(func_text)
        if a is None or b is None:
            return "Root interval could not be auto-detected."
            
        while (b - a) > tolerance:
            mid = (a + b) / 2.0
            try:
                f_mid = cls.f(mid, func_text)
                if abs(f_mid) < 1e-12:
                    return f"{mid:.5f}"
                if cls.f(a, func_text) * f_mid < 0:
                    b = mid
                else:
                    a = mid
            except:
                return "Calculation Error (Undefined Region)."
        return f"{(a + b) / 2.0:.5f}"



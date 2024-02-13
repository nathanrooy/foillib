from math import pow, sqrt
from typing import List


# naca constants
A0 = 0.2969
A1 = -0.1260
A2 = -0.3516
A3 = 0.2843


a0123 = lambda x: A0 * sqrt(x) + A1 * x + A2 * pow(x, 2) + A3 * pow(x, 3)


def a4(finite_te: bool) -> float:
    if finite_te:
        return -0.1015
    else:
        return -0.1036


def thickness_distribution(t: float, finite_te: bool, xc: list) -> List[float]:
    """
    NACA-4 and 5 series airfoils share the same thickness distribution (y_t)
    """
    _a4 = a4(finite_te)
    y_t = [5 * t * (a0123(x) + _a4 * pow(x, 4)) for x in xc]

    # force the trailing edge to zero
    if not finite_te:
        y_t[-1] = 0
    return y_t

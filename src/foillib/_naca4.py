from math import atan, cos, pow, sin, sqrt
from typing import List, Tuple

from ._common import spacing
from ._naca_common import thickness_distribution
from ._types import SpacingMethod


def naca4(
    M: int, P: int, XX: int, npts: int, finite_te: bool, spacing_method: SpacingMethod
) -> List[Tuple]:
    """
    NACA-4 SERIES AIRFOIL -> "MPXX"

    M  : maximum value of the mean line in hundredths of chord.
    P  : chordwise position of max camber in tenths of chord.
    XX : max thickness (t/c) in percent chord.
    """

    # munge thickness input
    t = float(XX) / 100.0

    # generate chord positions
    xc = spacing(npts, spacing_method)

    # compute airfoil half-thickness
    yt = thickness_distribution(t, finite_te, xc)

    # symmetrical airfoils
    if P == 0:
        x = xc[::-1] + [0] + xc
        y = yt[::-1] + [0] + [-v for v in yt]
        return x, y

    # cambered airfoils
    m = float(M) / 100.0
    p = float(P) / 10.0

    # determine mean camber line (yc), camber gradient (dyc_dx), and theta
    xu, yu, xl, yl = [0] * len(xc), [0] * len(xc), [0] * len(xc), [0] * len(xc)
    for i, x in enumerate(xc):
        if x <= p:
            yc = m / pow(p, 2) * (2 * p * x - pow(x, 2))
            dyc_dx = 2 * m / pow(p, 2) * (p - x)
        else:
            yc = m / pow(1 - p, 2) * ((1 - 2 * p) + (2 * p * x) - pow(x, 2))
            dyc_dx = 2 * m / pow(1 - p, 2) * (p - x)

        # compute surface coordinates
        theta = atan(dyc_dx)
        xu[i] = x - yt[i] * sin(theta)
        yu[i] = yc + yt[i] * cos(theta)
        xl[i] = x + yt[i] * sin(theta)
        yl[i] = yc - yt[i] * cos(theta)

    # assemble final airfoil coordinates
    x = xu[::-1] + [0] + xl
    y = yu[::-1] + [0] + yl
    return x, y

from math import atan, cos, pow, sin
from typing import List, Tuple

from ._common import spacing
from ._naca_common import thickness_distribution
from ._types import SpacingMethod


# tabulated camber line parameters
prk1 = {
    # non-reflexed (simple)
    0: {
        "210": {"p": 0.05, "r": 0.0580, "k1": 361.40},
        "220": {"p": 0.10, "r": 0.1260, "k1": 51.640},
        "230": {"p": 0.15, "r": 0.2025, "k1": 15.957},
        "240": {"p": 0.20, "r": 0.2900, "k1":  6.643},
        "250": {"p": 0.25, "r": 0.3910, "k1":  3.230},
    },
    # reflexed
    1: {
        "221": {"p": 0.05, "r": 0.0580, "k1": 361.40, "k2/k1": 0.000764},
        "231": {"p": 0.15, "r": 0.2170, "k1": 15.793, "k2/k1": 0.00677},
        "241": {"p": 0.20, "r": 0.3180, "k1":  6.520, "k2/k1": 0.0303},
        "251": {"p": 0.25, "r": 0.4410, "k1":  3.191, "k2/k1": 0.1355},
    },
}


def naca5(
    L: int,
    P: int,
    S: int,
    TT: int,
    npts: int,
    finite_te: bool,
    spacing_method=SpacingMethod,
) -> List[Tuple]:
    """
    NACA-5 SERIES AIRFOIL -> "LPSXX"

    L  : Designed coefficient of lift multiplied by 3/20.
    P  : The position of maximum camber divided by 20.
    S  : 0 = normal camber line, 1 = reflexed camber line.
    XX : max thickness (t/c) in percent chord.
    """

    # munge inputs
    t = float(TT) / 100.0
    profile = f"{L:d}{P:d}{S:d}"

    # generate chord positions
    xc = spacing(npts, spacing_method)

    # compute airfoil half-thickness
    yt = thickness_distribution(t, finite_te, xc)

    # determine interpolated camberline parameters
    if S == 0:
        p, r, k1 = (
            prk1[S][profile]["p"],
            prk1[S][profile]["r"],
            prk1[S][profile]["k1"],
        )
    else:
        p, r, k1, k2_k1 = (
            prk1[S][profile]["p"],
            prk1[S][profile]["r"],
            prk1[S][profile]["k1"],
            prk1[S][profile]["k2/k1"],
        )

    # determine mean camber line (yc), camber gradient (dyc_dx), and theta
    xu, yu, xl, yl = [0] * len(xc), [0] * len(xc), [0] * len(xc), [0] * len(xc)
    for i, x in enumerate(xc):

        # non-reflex (standard)
        if S == 0:
            if x <= r:
                yc = (k1 / 6) * (
                    pow(x, 3) - 3 * r * pow(x, 2) + pow(r, 2) * (3 - r) * x
                )
                dyc_dx = (k1 / 6) * (3 * pow(x, 2) - 6 * r * x + pow(r, 2) * (3 - r))
            else:
                yc = (k1 * pow(r, 3) / 6) * (1 - x)
                dyc_dx = -(k1 * pow(r, 3) / 6)

        # reflex
        if S == 1:
            if x <= r:
                yc = (k1 / 6) * (
                    pow(x - r, 3)
                    - k2_k1 * pow(1 - r, 3) * x
                    - pow(r, 3) * x
                    + pow(r, 3)
                )
                dyc_dx = (k1 / 6) * (
                    3 * pow(x - r, 2) - k2_k1 * pow(1 - r, 3) - pow(r, 3)
                )
            else:
                yc = (k1 / 6) * (
                    k2_k1 * pow(x - r, 3)
                    - k2_k1 * pow(1 - r, 3) * x
                    - pow(r, 3) * x
                    + pow(r, 3)
                )
                dyc_dx = (k1 / 6) * (
                    3 * k2_k1 * pow(x - r, 2) - k2_k1 * pow(1 - r, 3) - pow(r, 3)
                )

        # compute surface coordinates
        theta = atan(dyc_dx)
        xu[i] = x - yt[i] * sin(theta)
        yu[i] = yc + yt[i] * cos(theta)
        xl[i] = x + yt[i] * sin(theta)
        yl[i] = yc - yt[i] * cos(theta)

    x = xu[::-1] + [0] + xl
    y = yu[::-1] + [0] + yl
    return x, y

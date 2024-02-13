from math import cos, sin, sqrt
from typing import List, Tuple

from ._common import spacing
from ._types import SpacingMethod


def b2(t: float, p0: float, p1: float, p2: float) -> float:
    """
    Quadratic definition

    t  : float
    p0 : float
    p1 : float
    p2 : float
    """
    return p1 + (p0 - p1) * (1 - t) ** 2 + (p2 - p1) * t**2


def b2_find_t(x: list, a: float, b: float, c: float) -> float:
    """
    Find the roots: given x, solve for t
    """
    d = abs(c * x + x * a - 2 * x * b + b**2 - c * a)
    if a + c != 2 * b:
        t = (a - b + sqrt(d)) / (c + a - 2 * b)
    elif a == 2 * b - c and b != c:
        t = -(-2 * b + c + x) / (2 * (b - c))
    return max(min(1, t), 0)


def b2_segment(x: list, p0: list, p1: list, p2: list) -> List[Tuple]:
    """
    Single quadratic segment

    """

    # determine which chord points fall within the current bezier segment
    x_seg = [_x for _x in x if p0[0] < _x <= p2[0]]

    # given the chord positions, determine the local segment positions (t)
    t = [b2_find_t(_x, p0[0], p1[0], p2[0]) for _x in x_seg]

    # compute the bezier y-values
    y = [b2(_t, p0[1], p1[1], p2[1]) for _t in t]

    # munge and return
    return list(zip(*[x_seg, y]))


def quadratic_bezier(x: List[float], cps: List[Tuple]) -> List[Tuple]:
    """
    Piecewise Quadratic Bezier Curve

    x   : x-coordinate positions along chord (le -> te).
    cps : list of tuples representing the bezier control points [(x1,y1), (x2,y2),...,(xn,yn)s]
    """

    # compute the first segment
    curve = []
    x_mid = (cps[1][0] + cps[2][0]) / 2.0
    y_mid = (cps[1][1] + cps[2][1]) / 2.0
    curve += b2_segment(x, cps[0], cps[1], (x_mid, y_mid))

    # cycle through the intermediate segments
    for i in range(1, len(cps) - 3):
        x_mid1 = (cps[i][0] + cps[i + 1][0]) / 2.0
        y_mid1 = (cps[i][1] + cps[i + 1][1]) / 2.0
        x_mid2 = (cps[i + 1][0] + cps[i + 2][0]) / 2.0
        y_mid2 = (cps[i + 1][1] + cps[i + 2][1]) / 2.0
        curve += b2_segment(x, (x_mid1, y_mid1), cps[i + 1], (x_mid2, y_mid2))

    # compute final segment
    x_mid = (cps[-3][0] + cps[-2][0]) / 2.0
    y_mid = (cps[-3][1] + cps[-2][1]) / 2.0
    curve += b2_segment(x, (x_mid, y_mid), cps[-2], cps[-1])

    return curve


def bezier(
    cpts_le: List,
    cpts_top: List[Tuple],
    cpts_bot: List[Tuple] = None,
    te: float = 0.00252,
    npts: int = 100,
    spacing_method: SpacingMethod = "cosine",
) -> List[Tuple]:
    """
    The Bezier airfoil is comprised of two composite (piecewise) Bezier curves connected at the
    leading edge with G1 (tangent) continuity.

    cps_le  :
    cps_top :
    cps_bot :
    te      :
    npts    :
    spacing_method :
    """

    # general input checks
    assert len(cpts_top) >= 2, "not enough control points specified for top surface..."
    assert len(cpts_le) in [1, 2], "leading edge radius has not been specified..."
    for v in cpts_le:
        assert v > 0, "leading edge radius must be defined with positive values"
    for i in range(len(cpts_top) - 1):
        assert (
            cpts_top[i][0] < cpts_top[i + 1][0]
        ), "top surface control point x-coordinates must be monotonically increasing"
    if cpts_bot != None:
        assert (
            len(cpts_bot) >= 2
        ), "not enough control points specified for bottom surface..."
        for i in range(len(cpts_bot) - 1):
            assert (
                cpts_bot[i][0] < cpts_bot[i + 1][0]
            ), "bottom surface control point x-coordinates must be monotonically increasing"

    # generate chord positions
    xc = spacing(npts, spacing_method)

    # munge leading edge control points
    if len(cpts_le) == 1:
        cpts_le = [abs(cpts_le[0])] * 2

    # top surface
    cpts_top = [(0, 0), (0, cpts_le[0])] + cpts_top + [(1, te / 2)]
    xy_top = quadratic_bezier(xc, cpts_top)

    # bottom surface
    if cpts_bot != None:
        cpts_bot = [(0, 0), (0, -cpts_le[1])] + cpts_bot + [(1, -te / 2)]
        xy_bot = quadratic_bezier(xc, cpts_bot)
    else:
        xy_bot = [(x, -y) for x, y in xy_top]

    # assemble the entire curve
    xy = xy_top[::-1] + [(0, 0)] + xy_bot

    return list(zip(*xy))

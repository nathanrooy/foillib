from math import cos, pi
from typing import List

from ._types import SpacingMethod


def spacing(npts: int, spacing_method: SpacingMethod = "cosine") -> List[float]:
    """
    - Starts at the LE -> TE
    - The leading edge point (0,0) is not included.
    """
    assert spacing_method in ["equal", "cosine"]
    if spacing_method == "equal":
        return [x / npts for x in range(1, npts + 1)]
    elif spacing_method == "cosine":
        return [(1 - cos(x / npts * pi)) / 2 for x in range(1, npts + 1)]

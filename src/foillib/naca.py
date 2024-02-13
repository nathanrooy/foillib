from typing import List

from ._naca4 import naca4
from ._naca5 import naca5, prk1
from ._types import SpacingMethod


def naca(
    digits: str, npts=100, finite_te=True, spacing_method: SpacingMethod = "cosine"
) -> List[tuple]:
    has_dash = "-" in digits
    assert len(digits) in [4, 5]

    # naca-4 series airfoils
    if len(digits) == 4 and has_dash == False:
        return naca4(
            int(digits[0]),
            int(digits[1]),
            int(digits[2:]),
            npts,
            finite_te,
            spacing_method,
        )

    # naca-5 series airfoils
    if len(digits) == 5 and has_dash == False:
        assert (
            digits[:3] in prk1[0].keys() or digits[:3] in prk1[1].keys()
        ), "Unsupported design"
        assert digits[2] in [
            "0",
            "1",
        ], 'Ensure that the camber line is defined as: regular="1" or reflexed="2"'
        return naca5(
            int(digits[0]),
            int(digits[1]),
            int(digits[2]),
            int(digits[3:]),
            npts,
            finite_te,
            spacing_method,
        )

    # naca-6 series airfoils
    # coming soon maybe...

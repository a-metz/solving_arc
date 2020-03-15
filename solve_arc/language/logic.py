from ..utilities.hashable_partial import partial

import numpy as np

from .grid import Grid
from .argument import expect_tuple


@expect_tuple(length=2, on_error_return=[])
def parameterize(a, b):
    if a.shape != b.shape:
        return []

    return [
        elementwise_equal_and,
        elementwise_equal_or,
        elementwise_xor,
    ]


@expect_tuple(length=2, on_error_return=None)
def elementwise_equal_and(a, b):
    if a.shape != b.shape:
        return None

    try:
        return Grid(_elementwise_eand(a.state, b.state))
    except ValueError:
        return None


@expect_tuple(length=2, on_error_return=None)
def elementwise_equal_or(a, b):
    if a.shape != b.shape:
        return None

    try:
        return Grid(_elementwise_eor(a.state, b.state))
    except ValueError:
        return None


@expect_tuple(length=2, on_error_return=None)
def elementwise_xor(a, b):
    if a.shape != b.shape:
        return None

    try:
        return Grid(_elementwise_xor(a.state, b.state))
    except ValueError:
        return None


@np.vectorize
def _elementwise_eand(a, b):
    if a == 0:
        return 0
    elif b == 0:
        return 0
    elif a == b:
        return a
    else:
        raise ValueError(
            "elements need to be equal or at least one of them needs to be 0, "
            "but instead are {} and {}".format(a, b)
        )


@np.vectorize
def _elementwise_eor(a, b):
    if a == 0:
        return b
    elif b == 0:
        return a
    elif a == b:
        return a
    else:
        raise ValueError(
            "elements need to be equal or at least one of them needs to be 0, "
            "but instead are {} and {}".format(a, b)
        )


@np.vectorize
def _elementwise_xor(a, b):
    if a == 0:
        return b
    elif b == 0:
        return a
    else:
        return 0

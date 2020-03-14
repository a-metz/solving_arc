from functools import partial

import numpy as np

from .grid import Grid


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
            "but instead are a[...]={} and b[...]={}".format(a, b)
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
            "but instead are a[...]={} and b[...]={}".format(a, b)
        )


@np.vectorize
def _elementwise_xor(a, b):
    if a == 0:
        return b
    elif b == 0:
        return a
    else:
        return 0


def _extract_operands(grids):
    # if not unpackable, will raise ValueError
    a, b = grids

    if a.shape != b.shape:
        raise ValueError(
            "arguments need to have the same shape, "
            "but instead are a.shape={} and b.shape={}".format(a.shape, b.shape)
        )

    return a, b


def elementwise_equal_and(grids):
    try:
        a, b = _extract_operands(grids)
        return Grid(_elementwise_eand(a.state, b.state))
    except ValueError:
        return None


def elementwise_equal_or(grids):
    try:
        a, b = _extract_operands(grids)
        return Grid(_elementwise_eor(a.state, b.state))
    except ValueError:
        return None


def elementwise_xor(grids):
    try:
        a, b = _extract_operands(grids)
        return Grid(_elementwise_xor(a.state, b.state))
    except ValueError:
        return None


def parameterize(grids):
    try:
        a, b = _extract_operands(grids)
    except ValueError:
        return []

    return [
        partial(elementwise_equal_and, [a, b]),
        partial(elementwise_equal_or, [a, b]),
        partial(elementwise_xor, [a, b]),
    ]

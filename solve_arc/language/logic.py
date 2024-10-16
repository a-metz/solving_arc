import numpy as np

from .arguments import *


def elementwise_equal_and(a, b):
    if a.shape != b.shape:
        return None

    try:
        return Grid(_elementwise_eand(a.state, b.state))
    except ValueError:
        return None


def elementwise_equal_or(a, b):
    if a.shape != b.shape:
        return None

    try:
        return Grid(_elementwise_eor(a.state, b.state))
    except ValueError:
        return None


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


def selection_elementwise_and(a, b):
    return Selection(np.logical_and(a.state, b.state))


def selection_elementwise_or(a, b):
    return Selection(np.logical_or(a.state, b.state))


def selection_elementwise_xor(a, b):
    return Selection(np.logical_xor(a.state, b.state))


def selection_elementwise_eq(a, b):
    return Selection(a.state == b.state)


def selection_elementwise_not(selection):
    return Selection(np.invert(selection.state))

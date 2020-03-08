import numpy as np

from .grid import Grid


def _check_shape_equals(a, b):
    if a.shape != b.shape:
        raise ValueError(
            "arguments need to have the same shape, "
            "but instead are a.shape={} and b.shape={}".format(a.shape, b.shape)
        )
    return a, b


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


def elementwise_eand(a, b):
    _check_shape_equals(a, b)
    return Grid(_elementwise_eand(a.state, b.state))


def _eor(a, b):
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


_elementwise_eor = np.vectorize(_eor)


def elementwise_eor(a, b):
    _check_shape_equals(a, b)
    return Grid(_elementwise_eor(a.state, b.state))


def _xor(a, b):
    if a == 0:
        return b
    elif b == 0:
        return a
    else:
        return 0


_elementwise_xor = np.vectorize(_xor)


def elementwise_xor(a, b):
    _check_shape_equals(a, b)
    return Grid(_elementwise_xor(a.state, b.state))

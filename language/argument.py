from .grid import Grid


class ArgumentError(Exception):
    pass


def extract_scalar(arg, type_=Grid):
    if isinstance(arg, type_):
        return arg

    # might be packed in single element list
    if hasattr(arg, "__len__") and len(arg) == 1:
        return extract_scalar(arg[0])

    raise ArgumentError("expected single element of correct type")


def extract_tuple(arg, length=2, type_=Grid):
    if hasattr(arg, "__len__") and len(arg) == length:
        return tuple(extract_scalar(arg, type_) for arg in arg)

    # might be packed in another single element list
    if hasattr(arg, "__len__") and len(arg) == 1:
        return extract_tuple(arg[0], length)

    raise ArgumentError("expected correct number of elements of correct type")

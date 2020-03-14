from .grid import Grid


class ArgumentError(Exception):
    pass


def extract_scalar(argument, type_=Grid):
    if isinstance(argument, type_):
        return argument

    # might be packed in single element list
    if hasattr(argument, "__len__") and len(argument) == 1:
        return extract_scalar(argument[0])

    raise ArgumentError("expected single element of correct type")


def extract_tuple(argument, length=2, type_=Grid):
    if hasattr(argument, "__len__") and len(argument) == length:
        return tuple(extract_scalar(arg, type_) for arg in argument)

    # might be packed in another single element list
    if hasattr(argument, "__len__") and len(argument) == 1:
        return extract_tuple(argument[0], length)

    raise ArgumentError("expected correct number of elements of correct type")

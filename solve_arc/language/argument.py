from functools import wraps
from .grid import Grid


class ArgumentError(Exception):
    pass


def expect_scalar(on_error_return, expected_type=Grid):
    """return decorator which safely extracts a scalar input of expected_type
    from first argument or returns on_error_return on error
    """

    def decorator(func):
        @wraps(func)
        def wrapper(argument, *args, **kwargs):
            try:
                scalar = extract_scalar(argument, expected_type)
            except ArgumentError:
                return on_error_return
            return func(scalar, *args, **kwargs)

        return wrapper

    return decorator


def extract_scalar(argument, expected_type=Grid):
    if isinstance(argument, expected_type):
        return argument

    # might be packed in single element list
    if hasattr(argument, "__len__") and len(argument) == 1:
        return extract_scalar(argument[0])

    raise ArgumentError("expected single element of correct type")


def expect_tuple(length, on_error_return, expected_type=Grid):
    """return decorator which safely extracts a tuple input of expected_type
    from first argument or returns on_error_return on error
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                tuple_ = extract_tuple(args[:length], length, expected_type)
            except ArgumentError:
                return on_error_return
            return func(*tuple_, *args[length:], **kwargs)

        return wrapper

    return decorator


def extract_tuple(argument, length, expected_type=Grid):
    if hasattr(argument, "__len__") and len(argument) == length:
        return tuple(extract_scalar(arg, expected_type) for arg in argument)

    # might be packed in another single element list
    if hasattr(argument, "__len__") and len(argument) == 1:
        return extract_tuple(argument[0], length)

    raise ArgumentError("expected correct number of elements of correct type")

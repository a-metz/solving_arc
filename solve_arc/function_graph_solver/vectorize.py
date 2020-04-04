import itertools

# break naming conventions for consistent decorator naming
class vectorize:
    """vectorize decorator with hash only dependent on wrapped function"""

    def __init__(self, func):
        self.func = func
        self.__name__ = self.func.__name__

    def __call__(self, *arg_tuples):
        return tuple(self.func(*args) for args in zip(*arg_tuples))

    def __str__(self):
        return self.func.__name__

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.func.__name__)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def __hash__(self):
        return hash(self.func)


class repeat:
    """repeat iterator with hash only dependent on wrapped value"""

    def __init__(self, value, times=None):
        if times:
            self.repeated_value = (value,) * times
        else:
            self.repeated_value = itertools.repeat(value)

        self.value = value

    def __iter__(self):
        return iter(self.repeated_value)

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def __hash__(self):
        return hash(self.value)


def repeat_once(value):
    return repeat(value, times=1)

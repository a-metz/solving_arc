import itertools


class _FunctionWrapper:
    """wrapped function with hash only dependent on function"""

    def __init__(self, func):
        self.func = func
        self.__name__ = self.func.__name__

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()

    def __str__(self):
        return self.func.__name__

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.func.__name__)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def __hash__(self):
        return hash(self.func)


# break naming conventions for consistent decorator naming
class vectorize(_FunctionWrapper):
    """vectorized application of function"""

    def __call__(self, *arg_tuples):
        return tuple(self.func(*args) for args in zip(*arg_tuples))


class _ValueWrapper:
    """wrapped value with hash only dependent on value"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def __hash__(self):
        return hash(self.value)


class repeat(_ValueWrapper):
    """repeat wrapped value

    unlike itertools.repeat this iterable is hashed / comparable based on value
    """

    def __init__(self, value):
        super().__init__(value)
        self.repeated_value = itertools.repeat(value)

    def __iter__(self):
        return iter(self.repeated_value)


class repeat_once(_ValueWrapper):
    """iterator which provides wrapped value once"""

    def __init__(self, value):
        super().__init__(value)
        self.repeated_value = (value,)

    def __iter__(self):
        return iter(self.repeated_value)

from ..language import Grid, Mask


class _Node:
    def __call__(self, use_cache=True):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        raise NotImplementedError()

    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def __hash__(self):
        raise NotImplementedError()


class Function(_Node):
    """cached partial application"""

    def __init__(self, callable_, *args):
        self.callable_ = callable_
        self.args = args

    def __call__(self, use_cache=True):
        """evaluate function with evaluated args, use cached values if possible and use_cache is True"""
        if not (use_cache and hasattr(self, "value")):
            args = [arg(use_cache) for arg in self.args]
            self.value = self.callable_(*args)

        return self.value

    def __str__(self):
        return "{}({})".format(self.callable_.__name__, ", ".join(str(arg) for arg in self.args))

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join([self.callable_.__name__] + [repr(arg) for arg in self.args]),
        )

    def __hash__(self):
        return hash(self.callable_) ^ hash(tuple(arg() for arg in self.args))


class Constant(_Node):
    def __init__(self, value):
        self.value = value

    def __call__(self, use_cache=True):
        return self.value

    def __str__(self):
        return "{}".format(str(self.value))

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, repr(self.value))

    def __hash__(self):
        return hash(self.value)

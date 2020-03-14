import functools


class partial(functools.partial):
    def __eq__(self, other):
        return (
            self.func == other.func and self.args == other.args and self.keywords == other.keywords
        )

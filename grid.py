import numpy as np


class Grid:
    def __init__(self, state):
        self.state = np.array(state, copy=True)

        if len(self.state.shape) != 2:
            raise ValueError(
                "state needs to be 2d array, "
                "but insead is {}d array".format(len(self.state.shape))
            )

    @classmethod
    def empty(cls, shape):
        return cls(np.zeros(shape=shape))

    @property
    def shape(self):
        return self.state.shape

    def __getitem__(self, *args, **kwargs):
        return self.__class__(self.state.__getitem__(*args, **kwargs))

    def __hash__(self):
        # only consider state for hash
        return hash(self.state.tobytes())

    def __eq__(self, other):
        return hash(self) == hash(other)

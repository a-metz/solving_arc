import numpy as np


class Grid:
    def __init__(self, state):
        self.state = np.array(state)

    @classmethod
    def empty(cls, shape):
        return cls(np.zeros(shape=shape))

    @property
    def shape(self):
        return self.state.shape

    def __getitem__(self, *args, **kwargs):
        return self.state.__getitem__(*args, **kwargs)

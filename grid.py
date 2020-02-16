import numpy as np


class Grid:
    def __init__(self, array):
        self.array = np.array(array)

    @classmethod
    def empty(cls, shape):
        return cls(np.zeros(shape=shape))

    @property
    def shape(self):
        return self.array.shape

    def __getitem__(self, *args, **kwargs):
        return self.array.__getitem__(*args, **kwargs)

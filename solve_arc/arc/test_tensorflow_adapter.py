from .tensorflow_adapter import *


def test_all_grids_dataset():
    for tensor in get_all_grids_dataset(limit=10):
        print(tensor)

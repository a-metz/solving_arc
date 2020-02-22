from .dataset import *


def test_load_data():
    task = load_dir("utilities/test_data/")["test_data"]

    assert task.train[0].input.shape == (3, 3)
    assert task.train[0].output.shape == (9, 9)
    assert task.test[0].input.shape == (3, 3)
    assert task.test[0].output.shape == (9, 9)

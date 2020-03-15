from .dataset import *


def test_load_tasks():
    # run pytest from repo root
    task = load_tasks("solve_arc/arc/test_data")["0520fde7"]

    assert task.train[0].input.shape == (3, 7)
    assert task.train[0].output.shape == (3, 3)
    assert task.test[0].input.shape == (3, 7)
    assert task.test[0].output.shape == (3, 3)

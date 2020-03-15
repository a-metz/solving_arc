from .dataset import *


def test_load_tasks():
    # run pytest from repo root
    task = load_tasks("solve_arc/arc/test_data")["arc_test_data"]

    assert task.train[0].input.shape == (3, 3)
    assert task.train[0].output.shape == (9, 9)
    assert task.test[0].input.shape == (3, 3)
    assert task.test[0].output.shape == (9, 9)

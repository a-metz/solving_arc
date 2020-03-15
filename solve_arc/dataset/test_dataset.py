from .dataset import *


def test_load_data():
    # run pytest from repo root
    task = load_dir("solve_arc/dataset/test_data")["arc_test_data"]

    assert task.train[0].input.shape == (3, 3)
    assert task.train[0].output.shape == (9, 9)
    assert task.test[0].input.shape == (3, 3)
    assert task.test[0].output.shape == (9, 9)

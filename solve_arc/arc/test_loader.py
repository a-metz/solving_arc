from .loader import *
from ..language import Grid


def test_dimensions():
    arc_tasks = training_tasks()

    # 400 tasks in training set
    assert len(arc_tasks) == 400

    for task_id in arc_tasks.keys():
        # 8-digit hex as string
        assert len(task_id) == 8

    for task in arc_tasks.values():
        num_train_subtasks = len(task.train)
        assert num_train_subtasks > 0

        num_test_subtasks = len(task.test)
        assert num_test_subtasks > 0


def test_train_and_test_subtasks_for_arbitrary_task():
    subtasks = training_tasks()["0520fde7"].train

    assert len(subtasks) == 3

    expected_input_grid = Grid.from_string(
        """
        1 0 0 5 0 1 0
        0 1 0 5 1 1 1
        1 0 0 5 0 0 0
        """
    )
    assert subtasks[0].input == expected_input_grid

    expected_output_grid = Grid.from_string(
        """
        0 0 0
        0 2 0
        0 0 0
        """
    )
    assert subtasks[0].output == expected_output_grid

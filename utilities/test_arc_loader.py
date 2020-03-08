from .arc_loader import *
from ..language.grid import Grid


def test_dimensions():
    tasks = arc_tasks()

    # 400 tasks in training set
    assert len(tasks) == 400

    for task_id in tasks.keys():
        # 8-digit hex as string
        assert len(task_id) == 8

    for task in tasks.values():
        num_train_subtasks = len(task.train)
        assert num_train_subtasks > 0

        num_test_subtasks = len(task.test)
        assert num_test_subtasks > 0


def test_train_and_test_subtasks_for_arbitrary_task():
    subtasks = list(train_and_test_subtasks("0520fde7"))

    assert len(subtasks) == 4

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

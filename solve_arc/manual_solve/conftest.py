import re
import warnings

import pytest

from ..arc.loader import training_tasks


def train_and_test_subtasks(task_id):
    yield from training_tasks()[task_id].train
    yield from training_tasks()[task_id].test


# parameterize subtasks using test name
def pytest_generate_tests(metafunc):
    test_name = metafunc.function.__name__

    match = re.search(r"([0-9a-f]{8})", test_name)
    if match is not None:
        task_id = match.group(0)
        metafunc.parametrize(
            ["input_", "expected"],
            [(subtask.input, subtask.output) for subtask in train_and_test_subtasks(task_id)],
        )
    else:
        warnings.warn("Could not parse task id for test '{}'.".format(test_name))

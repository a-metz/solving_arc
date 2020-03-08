import re
import warnings

import pytest

from ..utilities.arc_loader import train_and_test_subtasks

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

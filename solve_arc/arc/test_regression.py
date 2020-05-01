from warnings import warn

import pytest

from .evaluation import _evaluate, _get_tasks
from .loader import training_tasks, evaluation_tasks
from .task_ids import SOLVED_TASK_IDS, REGRESSION_TASK_IDS


@pytest.fixture
def default_kwargs():
    return {
        "max_search_depth": 5,
        "max_seconds_per_task": 20,
        "max_expansions_per_node": 20,
    }


@pytest.mark.slow
def test_regression(default_kwargs):
    expect_solve = set(REGRESSION_TASK_IDS)
    solved = set(_evaluate(_get_tasks(expect_solve), **default_kwargs))

    assert expect_solve == solved, "failed to solve: {}".format(
        ", ".join(sorted(expect_solve - solved))
    )

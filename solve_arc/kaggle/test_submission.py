import pytest

from ..language import Grid
from .submission import *


def test_format_grid():
    grid = Grid([[1, 2], [3, 4]])

    assert format_grid(grid) == "|12|34|"


def test_format_results():
    task_id = "0520fde7"
    # single attempt
    test_0_result = Grid([[1, 0, 1], [0, 1, 1]])
    # multiple attempts
    test_1_result = [Grid([[1, 2], [3, 4]]), Grid([[5, 6], [7, 8]])]
    results = [test_0_result, test_1_result]

    results_string = format_results(task_id, results)
    assert results_string[0] == "0520fde7_0,|101|011| |00|00| |00|00|"
    assert results_string[1] == "0520fde7_1,|12|34| |56|78| |00|00|"


@pytest.fixture
def default_kwargs():
    return {
        "max_search_depth": 5,
        "max_seconds_per_task": 20,
        "max_expansions_per_node": 20,
    }


@pytest.mark.slow
def test_generate_submission_smoketest(default_kwargs):
    generate_submission(
        "solve_arc/kaggle/test_data", **default_kwargs,
    )

    submission = open("submission.csv", "r").readlines()
    assert submission[0] == "output_id,output\n"
    assert submission[1] == "0520fde7_0,|202|000|000| |00|00| |00|00|\n"
    # default result because no solution found
    assert submission[2] == "7c008303_0,|00|00| |00|00| |00|00|\n"
    # two test subtasks
    assert submission[3] == "ed36ccf7_0,|005|005|050| |00|00| |00|00|\n"
    assert submission[4] == "ed36ccf7_1,|100|011|100| |00|00| |00|00|\n"


@pytest.mark.slow
def test_generate_submission__only_selected_range(default_kwargs):
    generate_submission(
        "solve_arc/kaggle/test_data", task_range=slice(2, None), **default_kwargs,
    )

    submission = open("submission.csv", "r").readlines()
    assert submission[0] == "output_id,output\n"
    # not solved because not in task range
    assert submission[1] == "0520fde7_0,|00|00| |00|00| |00|00|\n"
    assert submission[2] == "7c008303_0,|00|00| |00|00| |00|00|\n"
    # two test subtasks
    assert submission[3] == "ed36ccf7_0,|005|005|050| |00|00| |00|00|\n"
    assert submission[4] == "ed36ccf7_1,|100|011|100| |00|00| |00|00|\n"

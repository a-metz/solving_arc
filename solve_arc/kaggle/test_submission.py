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


@pytest.mark.slow
def test_generate_submission_smoketest():
    generate_submission(
        "solve_arc/kaggle/test_data",
        max_search_depth=4,
        max_seconds_per_task=10,
        max_expansions_per_node=10,
    )

    submission = open("submission.csv", "r").readlines()
    assert submission[0] == "output_id,output\n"
    assert submission[1] == "0520fde7_0,|202|000|000| |00|00| |00|00|\n"
    # two test subtasks
    assert submission[2] == "3428a4f5_0,|30303|00030|00003|30033|33030|03000| |00|00| |00|00|\n"
    assert submission[3] == "3428a4f5_1,|03303|33030|00300|00330|33033|03303| |00|00| |00|00|\n"
    # default result because no solution found
    assert submission[4] == "7c008303_0,|00|00| |00|00| |00|00|\n"


@pytest.mark.slow
def test_generate_submission__only_selected_range():
    generate_submission(
        "solve_arc/kaggle/test_data",
        max_search_depth=4,
        max_seconds_per_task=10,
        max_expansions_per_node=10,
        task_range=slice(1, 2),
    )

    submission = open("submission.csv", "r").readlines()
    assert submission[0] == "output_id,output\n"
    # not solved because not in task range
    assert submission[1] == "0520fde7_0,|00|00| |00|00| |00|00|\n"
    assert submission[2] == "3428a4f5_0,|30303|00030|00003|30033|33030|03000| |00|00| |00|00|\n"
    assert submission[3] == "3428a4f5_1,|03303|33030|00300|00330|33033|03303| |00|00| |00|00|\n"
    # default result because no solution found
    assert submission[4] == "7c008303_0,|00|00| |00|00| |00|00|\n"

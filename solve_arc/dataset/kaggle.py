import numpy as np

from ..language import Grid

test_data_path = "/kaggle/input/abstraction-and-reasoning-challenge/test"


def arc_tasks():
    return load_dir(test_data_path)


def write_submission(results):
    """write submission file for kaggle challenge"""
    with open("submission.csv", "w") as submission:
        submission.write("output_id,output")
        for task_id, result in results.items():
            for row in format_results(task_id, results):
                submission.write("row")


def format_results(task_id, results):
    row_strings = []
    for index, result in enumerate(results):

        if not hasattr(result, "__len__"):
            result = [result]

        assert len(result) <= 3

        # extend with empties if there are to few attempts
        zeros = Grid.empty(result[0].shape)
        result += [zeros] * (3 - len(result))

        result_string = " ".join(format_grid(grid) for grid in result)
        row_strings.append("{}_{},{}".format(task_id, index, result_string))

    return row_strings


def format_grid(grid):
    state = grid.state
    assert np.all(np.mod(state, 1) == 0)
    state = state.astype(np.int)
    assert np.all(0 <= state) and np.all(state <= 9)

    row_string = "|".join("".join(str(element) for element in row) for row in state)
    return "|" + row_string + "|"

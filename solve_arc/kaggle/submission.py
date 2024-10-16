import numpy as np

from ..function_graph_solver.solver import solve, Constraint
from ..language import Grid
from .dataset import load_tasks
from .timeout import timeout


DEFAULT_RESULT = Grid.empty((2, 2))


def generate_submission(
    data_path,
    max_seconds_per_task,
    max_score=None,
    task_range=slice(None, None, None),
    **kwargs,
):
    with open("submission.csv", "w") as submission:
        submission.write("output_id,output\n")

        tasks = load_tasks(data_path)
        selected_task_ids = sorted(tasks.keys())[task_range]

        score = 0
        for task_id, task in tasks.items():
            print(task_id, end=": ")
            constraints = [
                Constraint(Grid(subtask["input"]), Grid(subtask["output"]))
                for subtask in task["train"]
            ]

            solution = None
            max_score_reached = max_score is not None and score >= max_score

            if task_id in selected_task_ids and not max_score_reached:
                solution = timeout(max_seconds_per_task)(solve)(constraints, **kwargs)

            if solution is not None:
                print(solution, end=" -> ")
                results = [solution(Grid(subtask["input"])) for subtask in task["test"]]
                results_valid = all([result is not None for result in results])
                if results_valid:
                    print("valid")
                    score += 1
                else:
                    print("invalid")
            else:
                results = [None] * len(task["test"])
                print("no solution")

            results = [
                result if result is not None else DEFAULT_RESULT for result in results
            ]
            for row_string in format_results(task_id, results):
                submission.write(row_string + "\n")

    print(
        "score: {}/{} (kaggle score: {})".format(
            score, len(tasks), (1 - score / len(tasks))
        )
    )


def format_results(task_id, results):
    row_strings = []
    for index, result in enumerate(results):

        if not hasattr(result, "__len__"):
            result = [result]

        result += [DEFAULT_RESULT] * (3 - len(result))

        result_string = " ".join(format_grid(grid) for grid in result)
        row_strings.append("{}_{},{}".format(task_id, index, result_string))

    return row_strings


def format_grid(grid):
    state = grid.state
    assert np.all(np.mod(state, 1) == 0)
    state = state.astype(int)
    assert np.all(0 <= state) and np.all(state <= 9)

    row_string = "|".join("".join(str(element) for element in row) for row in state)
    return "|" + row_string + "|"

from itertools import islice
import time

import click
import numpy as np


from ..function_graph_solver.sampling_search import solve, Constraint
from ..language import Grid
from .dataset import load_tasks


def generate_submission(data_path, max_depth=4):
    with open("submission.csv", "w") as submission:
        submission.write("output_id,output\n")

        tasks = load_tasks(data_path)

        score = 0
        for task_id, task in tasks.items():
            print(task_id, end=": ")
            subtasks = task["train"]
            constraints = [
                Constraint(Grid(subtask["input"]), Grid(subtask["output"]))
                for subtask in task["train"]
            ]

            solution = solve(constraints, max_depth=max_depth)

            if solution is not None:
                print(solution, end=" -> ")
                results = [solution(Grid(subtask["input"])) for subtask in task["test"]]
                results_valid = all([result is not None for result in results])
                if results_valid:
                    print("valid")
                    score += 1
                    for row_string in format_results(task_id, results):
                        submission.write(row_string + "\n")
                else:
                    print("invalid")
            else:
                print("no solution")

    print("score: {}/{} (kaggle score: {})".format(score, len(tasks), (1 - score / len(tasks))))


def format_results(task_id, results):
    row_strings = []
    for index, result in enumerate(results):

        if not hasattr(result, "__len__"):
            result = [result]

        assert len(result) <= 3

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

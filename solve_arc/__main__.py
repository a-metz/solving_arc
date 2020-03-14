from itertools import islice
import time

import click

from .solver.tree_search import solve, Constraint
from .dataset.arc_loader import arc_tasks
from .language.argument import extract_scalar


@click.command()
@click.argument("task_ids", nargs=-1)
def main(task_ids):

    if not task_ids:
        tasks = arc_tasks().items()
    else:
        tasks = [(task_id, arc_tasks()[task_id]) for task_id in task_ids]

    score = 0
    for task_id, (train_subtasks, test_subtasks) in tasks:
        print(task_id, end=" ", flush=True)
        constraints = [Constraint(*subtask) for subtask in train_subtasks]

        start = time.time()
        # iterative deepening
        for max_depth in range(5):
            if time.time() > start + 0.5:
                print("timeout")
                break

            print(end=".", flush=True)

            solution = solve(constraints, max_depth)

            if solution is not None:
                valid = check_solution(solution, train_subtasks)
                if valid:
                    score += 1
                    print("found valid solution")
                print(
                    "found", "valid" if valid else "invalid", "solution",
                )
                print(solution)
                break
        else:
            print("no solution")

    print("score: {}/{} (kaggle score: {})".format(score, len(tasks), (1 - score / len(tasks))))


def check_solution(solution, subtasks):
    return all([extract_scalar(solution(subtask.input)) == subtask.output for subtask in subtasks])


main()

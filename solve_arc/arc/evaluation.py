from itertools import islice

from func_timeout import func_timeout, FunctionTimedOut
import click

from .loader import training_tasks, evaluation_tasks
from ..function_graph_solver.sampling_search import solve, Constraint


@click.command()
@click.argument("task_ids", nargs=-1)
def evaluate(task_ids):

    if not task_ids:
        print("evaluating performance on training tasks")
        evaluate(loader.training_tasks().items())
        print("evaluating performance on evaluation tasks")
        evaluate(loader.evaluation_tasks().items())
    else:
        all_tasks = {**loader.training_tasks(), **loader.evaluation_tasks()}
        evaluate([(task_id, all_tasks[task_id]) for task_id in task_ids])


def _evaluate(tasks):
    score = 0
    for task_id, (train_subtasks, test_subtasks) in tasks:
        print(task_id, end=" ", flush=True)
        constraints = [Constraint(*subtask) for subtask in train_subtasks]

        try:
            solution = func_timeout(timeout=3, func=solve, args=(constraints, 5))
            if solution is not None:
                valid = check_solution(solution, train_subtasks)
                if valid:
                    score += 1
                    print("found valid solution")
                else:
                    print("found invalid solution")
                print(solution)
            else:
                print("no solution")

        except FunctionTimedOut:
            print("timeout")

    print("score: {}/{} (score: {})".format(score, len(tasks), (1 - score / len(tasks))))


def check_solution(solution, subtasks):
    return all(solution(subtask.input) == subtask.output for subtask in subtasks)

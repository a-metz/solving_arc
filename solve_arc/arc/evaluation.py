from itertools import islice
import logging
from datetime import datetime

from func_timeout import func_timeout, FunctionTimedOut
import click

from .loader import training_tasks, evaluation_tasks
from .solved_tasks import SOLVED_TASK_IDS
from ..function_graph_solver.sampling_search import solve, Constraint


logging.basicConfig(format="%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option("--debug/--no-debug", default=False)
@click.option("--max-seconds-per-task", default=10.0)
@click.option("--max-search-depth", default=5)
@click.argument("args", nargs=-1)
def evaluate(debug, args, **kwargs):
    if debug:
        logging.getLogger("solve_arc").setLevel(level=logging.DEBUG)

    if len(args) > 0:
        if args[0] == "solved":
            logger.info("evaluating performance on known solved tasks")
            _evaluate(_get_tasks(SOLVED_TASK_IDS), **kwargs)
        else:
            logger.info("evaluating performance on {}", str(args))
            _evaluate(_get_tasks(args), **kwargs)
    else:
        logger.info("evaluating performance on training tasks")
        _evaluate(training_tasks().items(), **kwargs)
        logger.info("evaluating performance on evaluation tasks")
        _evaluate(evaluation_tasks().items(), **kwargs)


def _get_tasks(task_ids):
    all_tasks = {**training_tasks(), **evaluation_tasks()}
    return [(task_id, all_tasks[task_id]) for task_id in task_ids]


def _evaluate(tasks, max_seconds_per_task=10, max_search_depth=5):
    score = 0
    solved = []
    start_time = datetime.now()
    for task_id, (train_subtasks, test_subtasks) in tasks:
        logger.info("solving {}".format(task_id))
        constraints = [Constraint(*subtask) for subtask in train_subtasks]

        try:
            solution = timeout(
                timeout=max_seconds_per_task, func=solve, args=(constraints, max_search_depth)
            )
            if solution is not None:
                valid = check_solution(solution, train_subtasks)
                if valid:
                    score += 1
                    solved.append(task_id)
                    logger.info("found valid solution: {}".format(solution))
                else:
                    logger.info("found invalid solution: {}".format(solution))
            else:
                logger.info("no solution")

        except FunctionTimedOut:
            logger.info("timeout")

    logger.info("solved: {}".format(", ".join(solved)))
    logger.info("elapsed time: {}".format(datetime.now() - start_time))
    logger.info("score: {}/{} ({})".format(score, len(tasks), (1 - score / len(tasks))))

    return solved


def timeout(timeout, func, args):
    if timeout:
        return func_timeout(timeout, func, args)
    else:
        return func(*args)


def check_solution(solution, subtasks):
    return all(solution(subtask.input) == subtask.output for subtask in subtasks)

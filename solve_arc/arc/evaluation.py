from itertools import islice
from datetime import datetime
from statistics import mean
import logging

from func_timeout import func_timeout, FunctionTimedOut
import click

from .loader import training_tasks, evaluation_tasks
from .task_ids import SOLVED_TASK_IDS, REGRESSION_TASK_IDS
from ..function_graph_solver.solver import solve, Constraint, Statistics


logging.basicConfig(format="%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option("--debug/--no-debug", default=False)
@click.option("--max-seconds-per-task", default=10.0)
@click.option("--search-strategy", default="sampling")
@click.option("--max-depth", default=5)
@click.option("--max-usages", default=10)
@click.option("--max-steps", default=50000)
@click.argument("args", nargs=-1)
def evaluate(debug, args, **kwargs):
    if debug:
        logging.getLogger("solve_arc").setLevel(level=logging.DEBUG)

    if len(args) > 0:
        if args[0] == "solved":
            logger.info("evaluating performance on known solved tasks")
            _evaluate(_get_tasks(SOLVED_TASK_IDS), **kwargs)
        elif args[0] == "unsolved":
            logger.info("evaluating performance on unsolved tasks")
            _evaluate(_get_all_tasks(except_task_ids=SOLVED_TASK_IDS), **kwargs)
        elif args[0] == "regression":
            logger.info("evaluating performance on regression tasks")
            _evaluate(_get_tasks(REGRESSION_TASK_IDS), **kwargs)
        elif args[0] == "training":
            logger.info("evaluating performance on training tasks")
            _evaluate(training_tasks().items(), **kwargs)
        elif args[0] == "evaluation":
            logger.info("evaluating performance on evaluation tasks")
            _evaluate(evaluation_tasks().items(), **kwargs)
        else:
            logger.info("evaluating performance on {}".format(", ".join(args)))
            _evaluate(_get_tasks(args), **kwargs)
    else:
        logger.info("evaluating performance on all tasks")
        _evaluate(_get_all_tasks(), **kwargs)
        logger.info("evaluating performance on evaluation tasks")
        _evaluate(evaluation_tasks().items(), **kwargs)


def _get_tasks(task_ids):
    all_tasks = {**training_tasks(), **evaluation_tasks()}
    return [(task_id, all_tasks[task_id]) for task_id in task_ids]


def _get_all_tasks(except_task_ids=tuple()):
    all_tasks = {**training_tasks(), **evaluation_tasks()}
    task_ids = set(all_tasks.keys()) - set(except_task_ids)
    return [(task_id, all_tasks[task_id]) for task_id in task_ids]


def _evaluate(tasks, max_seconds_per_task=10, **kwargs):
    score = 0
    solved = []
    statistics = []
    start_time = datetime.now()
    for task_id, (train_subtasks, test_subtasks) in tasks:
        logger.info("solving {}".format(task_id))
        constraints = [Constraint(*subtask) for subtask in train_subtasks]

        try:
            solution = timeout(
                timeout=max_seconds_per_task,
                func=solve,
                args=(constraints,),
                kwargs=kwargs,
            )
            if solution is not None:
                statistics.append(solution.statistics)
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
    if len(statistics) > 0:
        logger.info("statistics mean: {!s}".format(reduce_statistics(statistics, mean)))
    logger.info("score: {}/{} ({})".format(score, len(tasks), (1 - score / len(tasks))))

    return solved


def reduce_statistics(statistics, func):
    return Statistics(
        *[
            func(element)
            for element in zip(*[stat for stat in statistics if stat is not None])
        ]
    )


def timeout(timeout, func, args, kwargs):
    if timeout:
        return func_timeout(timeout=timeout, func=func, args=args, kwargs=kwargs)
    else:
        return func(*args, **kwargs)


def check_solution(solution, subtasks):
    return all(solution(subtask.input) == subtask.output for subtask in subtasks)

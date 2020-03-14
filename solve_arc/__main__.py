from itertools import islice

from .solver.tree_search import solve, Constraint
from .dataset.arc_loader import arc_tasks

tasks = islice(arc_tasks().items(), 10)

for task_id, (train_subtasks, test_subtasks) in tasks:
    print(".")
    constraints = [Constraint(*subtask) for subtask in train_subtasks]
    solution = solve(constraints, max_depth=4)
    if solution is not None:
        valid = all([solution(subtask.input) == subtask.output for subtask in test_subtasks])
        if valid:
            print("found valid solution for task {}".format(task_id))

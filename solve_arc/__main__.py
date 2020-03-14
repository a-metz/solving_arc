from itertools import islice

from .solver.tree_search import solve, Constraint
from .dataset.arc_loader import arc_tasks

tasks = arc_tasks().items()

for task_id, (train_subtasks, test_subtasks) in tasks:
    print(task_id, end=": ", flush=True)
    constraints = [Constraint(*subtask) for subtask in train_subtasks]
    solution = solve(constraints, max_depth=3)
    if solution is not None:
        valid = all([solution(subtask.input) == subtask.output for subtask in test_subtasks])
        print("found", "valid" if valid else "invalid", "solution")
    else:
        print("no solution")

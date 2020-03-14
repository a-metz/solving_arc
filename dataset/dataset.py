import collections
import os
import json

from schema import Schema, Use, And
import numpy as np

from ..language.grid import Grid

Task = collections.namedtuple("Task", ["train", "test"])
Subtask = collections.namedtuple("Subtask", ["input", "output"])

grid_schema = Schema(And([[int]], Use(Grid)))
subtask_schema = Schema(
    And({"input": grid_schema, "output": grid_schema}, Use(lambda dict_: Subtask(**dict_)))
)
task_schema = Schema(
    And({"train": [subtask_schema], "test": [subtask_schema]}, Use(lambda dict_: Task(**dict_)))
)


def load_dir(path):
    files_in_path = sorted(os.listdir(path))

    tasks = {}
    for file in sorted(os.listdir(path)):
        file_root, file_extension = os.path.splitext(file)

        if file_extension == ".json":
            tasks[file_root] = load_file(os.path.join(path, file))

    return tasks


def load_file(path):
    raw_task = json.load(open(path, "r"))
    return task_schema.validate(raw_task)

import os
import json


def load_tasks(path):
    files_in_path = sorted(os.listdir(path))

    tasks = {}
    for file in sorted(os.listdir(path)):
        file_root, file_extension = os.path.splitext(file)

        if file_extension == ".json":
            tasks[file_root] = json.load(open(os.path.join(path, file), "r"))

    return tasks

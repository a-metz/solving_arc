from .dataset import load_tasks

_tasks = None


def tasks():
    # use singleton to avoid reloading dataset (which takes long)
    global _tasks
    if _tasks is None:
        _tasks = load_tasks("dataset/data/training")

    return _tasks


def train_and_test_subtasks(task_id):
    yield from tasks()[task_id].train
    yield from tasks()[task_id].test

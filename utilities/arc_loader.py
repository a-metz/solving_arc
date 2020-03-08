from ..utilities.dataset import load_dir

_tasks = None


def arc_tasks():
    # use singleton to avoid reloading dataset (which takes long)
    global _tasks
    if _tasks is None:
        _tasks = load_dir("arc_dataset/data/training")

    return _tasks


def train_and_test_subtasks(task_id):
    yield from arc_tasks()[task_id].train
    yield from arc_tasks()[task_id].test

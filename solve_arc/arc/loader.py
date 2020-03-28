from .dataset import load_tasks

_training_tasks = None
_evaluation_tasks = None


def training_tasks():
    # use singleton to avoid reloading dataset (which takes long)
    global _training_tasks
    if _training_tasks is None:
        _training_tasks = load_tasks("dataset/data/training")

    return _training_tasks


def evaluation_tasks():
    # use singleton to avoid reloading dataset (which takes long)
    global _evaluation_tasks
    if _evaluation_tasks is None:
        _evaluation_tasks = load_tasks("dataset/data/evaluation")

    return _evaluation_tasks

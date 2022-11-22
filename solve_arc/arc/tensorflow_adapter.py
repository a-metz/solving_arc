from itertools import chain, islice

import tensorflow as tf

from .loader import all_tasks


def get_all_grids(limit=None):
    grids = []
    for task in islice(all_tasks().values(), limit):
        subtask_iter = chain(task.train, task.test)
        for subtask in subtask_iter:
            grids.append(subtask.input)
            grids.append(subtask.output)

    return grids


def grids_to_tensor(grids):
    return tf.ragged.constant([grid.state for grid in grids])


def get_all_grids_dataset(limit=None):
    return tf.data.Dataset.from_tensor_slices(grids_to_tensor(get_all_grids(limit)))

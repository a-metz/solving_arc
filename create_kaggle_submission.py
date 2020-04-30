#!/usr/bin/env python3
import os
import git

parameters = {
    "data_path": "/kaggle/input/abstraction-and-reasoning-challenge/test",
    "max_search_depth": 10,
    "max_seconds_per_task": 90,
    "max_expansions_per_node": 20,
    "task_range": slice(None, None, None),
}

filename_regex = r"^(?!(test_))[a-z_]+\.py\$"
tmp_file = "/tmp/output.py"
commit_hash = git.Repo().head.object.hexsha

# TODO: directly call kagglize-module main
command = 'kagglize-module --no-import --output-file="{}" --filename-regex="{}" solve_arc/'.format(
    tmp_file, filename_regex
)
print("running '{}'".format(command))
return_value = os.system(command)
if return_value != 0:
    raise Exception("kagglize-module failed".format(command))

header = """
# kaggle submission generated with kagglize-module
# original code available at https://github.com/wahtak/solving_arc (publicly accessable after competition)
# commit hash {}

parameters = {!r}

"""

footer = """
from solve_arc.kaggle.submission import generate_submission
generate_submission(**parameters)
"""

filename = "kaggle_submission_{}.py".format(commit_hash[:7])
with open(filename, "w") as submission:
    submission.write(header.format(commit_hash, parameters))
    submission.write(open(tmp_file, "r").read())
    submission.write(footer)


# TODO: optimize parameters by grid search
# TODO: automatically upload with kaggle API

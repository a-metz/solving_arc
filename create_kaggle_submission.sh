#!/usr/bin/env bash

kagglize-module --no-import --output-file=kaggle_submission.py solve_arc/
echo >> kaggle_submission.py
echo "from solve_arc.kaggle.submission import generate_submission" >> kaggle_submission.py
echo "generate_submission('/kaggle/input/abstraction-and-reasoning-challenge/test', max_search_depth=10, max_seconds_per_task=90, max_expansions_per_node=20)" >> kaggle_submission.py

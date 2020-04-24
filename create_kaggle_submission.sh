#!/usr/bin/env bash

kagglize-module --no-import --output-file=kaggle_submission.py solve_arc/
echo "from solve_arc.kaggle.submission import generate_submission" >> kaggle_submission.py
echo "generate_submission('/kaggle/input/abstraction-and-reasoning-challenge/test', max_seconds_per_task=120, max_search_depth=10)" >> kaggle_submission.py

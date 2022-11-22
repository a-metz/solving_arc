# Solving ARC

![Pytest badge](https://github.com/wahtak/solving_arc/workflows/Pytest/badge.svg)

## Setup

Install requirements:
```
pip install --user -r requirements.txt
```

## Usage

Run tests:
```
pytest
```

Run tests including slow test:
```
pytest --runslow
```

Print help:
```
python -m solve_arc --help
```

Run on known solved tasks:
```
python -m solve_arc solved
```

Generate code for kaggle submission to `kaggle_submission.py`:
```
./create_kaggle_submission.py
```

Format code:
```
black .
```


## TODO

  * expand step by step: sample random operation (weighted), then random args for operation (weighted)
  * apply operations for scalar grid/selection to sequences
  * colors / color sequences as operation result
  * color constants as permanent nodes in graph (?)
  * targets for all constraints as one sequence node in graph
  * mapping operation for mapping sequence to sequence
    (i.e. map colors to elements in grid sequence: take_for_color(grids, color))

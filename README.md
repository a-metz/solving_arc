# Solving ARC

![Pytest badge](https://github.com/wahtak/solving_arc/workflows/Pytest/badge.svg)


## Usage

Run tests:
```
cd <repository root dir>
pytest
```

Run tests including slow test:
```
cd <repository root dir>
pytest --runslow
```

Print help:
```
cd <repository root dir>
python -m solve_arc --help
```

Run on known solved tasks:
```
cd <repository root dir>
python -m solve_arc solved
```

Generate code for kaggle submission to `kaggle_submission.py`:
```
cd <repository root dir>
./create_kaggle_submission.sh
```


## TODO

  * expand step by step: sample random operation (weighted), then random args for operation (weighted)
  * apply operations for scalar grid/selection to sequences
  * colors / color sequences as operation result
  * color constants as permanent nodes in graph (?)
  * targets for all constraints as one sequence node in graph
  * mapping operation for mapping sequence to sequence
    (i.e. map colors to elements in grid sequence: take_for_color(grids, color))

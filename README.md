# Solving ARC

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

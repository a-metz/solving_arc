from pathlib import Path

output = Path.cwd().joinpath("kaggle.py").open("w")
output.write("from pathlib import Path\n\n")
output.write("path = Path.cwd()\n")
output.write("print('generating files to', path)\n")

for input_path in Path.cwd().joinpath("solve_arc").glob("**/*.py"):
    if input_path.name[:5] == "test_":
        continue

    relative_path = input_path.relative_to(Path.cwd())
    output.write("\n")
    output.write("# {}\n".format(relative_path))
    output.write(
        "path.joinpath('{}').mkdir(parents=True, exist_ok=True)\n".format(relative_path.parent)
    )
    output.write("path.joinpath('{}').open('w').write(".format(relative_path))
    output.write(repr(input_path.read_text()))
    output.write(")\n")

output.write("\n\nfrom solve_arc.kaggle.submission import generate_submission\n")
output.write(
    "generate_submission('/kaggle/input/abstraction-and-reasoning-challenge/test', max_seconds_per_task=10, max_search_depth=10)\n"
)

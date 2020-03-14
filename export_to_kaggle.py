from pathlib import Path

output = Path.cwd().joinpath("kaggle.py").open("w")
output.write("from pathlib import Path\n\n")

for input_path in Path.cwd().joinpath("solve_arc").glob("**/*.py"):
    if input_path.name[:5] == "test_":
        continue

    relative_path = input_path.relative_to(Path.cwd())
    output.write("\n")
    output.write("# {}\n".format(relative_path))
    output.write("print('{}')\n".format(relative_path))
    output.write(
        "Path.cwd().joinpath('{}').mkdir(parents=True, exist_ok=True)\n".format(
            relative_path.parent
        )
    )
    output.write("open('{}', 'w').write('''\n".format(relative_path))
    output.write(input_path.read_text())
    output.write("    ''')\n")

output.write("\nimport solve_arc\n")

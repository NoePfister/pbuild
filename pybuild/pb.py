import os
import pprint
import subprocess
from os import PathLike
from pathlib import Path


def parse_clang_h_output(output: str) -> list[tuple[int, str]]:
    splits = []

    for line in output.split("\n"):
        points = 0
        path = ""
        in_path = False
        start_pos = 0

        if "llvm" in line.lower():
            continue
        if "program files" in line.lower():
            continue

        for i, char in enumerate(line):
            if in_path:
                break
            # TODO: Breaks if path start with point: '../main.c'
            match char:
                case ".":
                    points += 1
                case " ":
                    continue
                case _:
                    in_path = True
                    start_pos = i

        path = line[start_pos:]
        path = clean_path(path)
        splits.append((points, path))

    return splits


def clean_path(path: str) -> str:

    return path.replace("\\\\", "/").replace("\\", "/").lstrip("/")


def generate_dependencies(input: list[tuple[int, str]]):
    files: list[tuple[str, tuple[str]]] = []
    level = 2

    for i, file in enumerate(input):
        if file[1] == "":
            continue

        if file[0] > level:
            level = file[0]
            continue
        dependencies = []
        for j, file2 in enumerate(input[i + 1 :]):
            if file2[0] == 1 + file[0]:
                dependencies.append(file2[1])
            else:
                break
        files.append((file[1], tuple(dependencies)))

    main_deps = []
    for dep in input:
        if dep[0] == 2:
            main_deps.append(dep[1])

    files.insert(0, ("main.c", tuple(list(set(main_deps)))))

    return list(set(tuple(files)))


def main():
    print("[PYBUILD] Build Starting ...")

    with open("output.txt", "w") as f:
        subprocess.run(["clang", "main.c", "-H"], stdout=f, stderr=f)

    with open("output.txt", "r") as f:
        parsed = parse_clang_h_output(f.read())
        # print(parsed)
        dependencies = generate_dependencies(parsed)
        pprint.pprint(dependencies)
        print(len(dependencies))


if __name__ == "__main__":
    main()

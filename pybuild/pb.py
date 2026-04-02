import subprocess


def parse_clang_h_output(output: str):
    splits = []
    print(output)
    for line in output.split("\n"):
        splits.append(line.strip("").split("."))
    print(splits)


def main():
    print("[PYBUILD] Build Starting ...")

    with open("output.txt", "w") as f:
        subprocess.run(["clang", "main.c", "-H"], stdout=f, stderr=f)

    with open("output.txt", "r") as f:
        parsed = parse_clang_h_output(f.read())


if __name__ == "__main__":
    main()

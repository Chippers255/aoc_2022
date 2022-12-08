from tqdm import tqdm


def dir_to_string(cwd: list) -> str:
    return '/'.join(cwd).replace("//", "/")


def build_directory(tree: dict, cwd: str) -> dict:
    """who is your daddy and what does he do?"""
    cwd = dir_to_string(cwd)
    if cwd not in tree:
        tree[cwd] = 0
    return tree


def size_rollup(tree: dict, cwd: str, file_size: int) -> dict:
    """stupid flanders and his sexy recursion"""
    cwd_str = dir_to_string(cwd)
    tree[cwd_str] += file_size
    if cwd_str != "/":
        tree = size_rollup(tree, cwd[:-1], file_size)
    return tree


if __name__ == "__main__":
    DIRECTORY = {}  # fuck using real trees
    CWD = []

    with open("input.txt") as f:
        for row in tqdm(f):
            fixed_row = row.replace("\n", "").split(" ")
            if fixed_row[1] == "cd": # change dir
                if fixed_row[2] == "..":
                    CWD.pop()
                elif fixed_row[2] == "/":
                    CWD = ["/"]
                else:
                    CWD.append(fixed_row[2])
                DIRECTORY = build_directory(DIRECTORY, CWD)
            elif fixed_row[0].isnumeric():
                DIRECTORY = size_rollup(DIRECTORY, CWD, int(fixed_row[0]))
            else: # don't let the noise distract you
                pass
    # part 1
    filtered_dir = {k: v for k, v in DIRECTORY.items() if v <= 100000}
    print(sum(filtered_dir.values()))

    # part 2
    unused = 70000000 - DIRECTORY["/"]
    filtered_dir = {k: v for k, v in DIRECTORY.items() if (v + unused) >= 30000000}
    print(min(filtered_dir.values()))

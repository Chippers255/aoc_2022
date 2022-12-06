import re


def elf_crane_9000(supply_stacks, move):
    # move 3 from 4 to 6
    fr = move[1] - 1
    to = move[2] - 1
    for _ in range(move[0]):
        supply_stacks[to].insert(0, supply_stacks[fr].pop(0))
    return supply_stacks


def elf_crane_9001(supply_stacks, move):
    # move 3 from 4 to 6
    fr = move[1] - 1
    to = move[2] - 1
    supply_stacks[to] = supply_stacks[fr][: move[0]] + supply_stacks[to]
    supply_stacks[fr] = supply_stacks[fr][move[0] :]
    return supply_stacks


def manifest_parser(file_name):
    supply_stacks = [[], [], [], [], [], [], [], [], []]
    moves = []

    with open(file_name, "r") as f:
        for row in f:
            fixed_row = row.replace("\n", "")
            if "move" in fixed_row:
                fixed_row = [int(x) for x in re.findall(r"[0-9]+", fixed_row)]
                moves.append(fixed_row)
            elif fixed_row == "":
                pass
            elif "[" not in fixed_row:
                pass
            else:
                stack = 0
                for col in range(1, len(row), 4):
                    if row[col] != " ":
                        supply_stacks[stack].append(row[col])
                    stack += 1

    return supply_stacks, moves


if __name__ == "__main__":
    # part 1
    supply_stacks, moves = manifest_parser("input.txt")
    for move in moves:
        supply_stacks = elf_crane_9000(supply_stacks, move)
    print("".join([s.pop(0) for s in supply_stacks]))

    # part 2
    supply_stacks, moves = manifest_parser("input.txt")
    for move in moves:
        supply_stacks = elf_crane_9001(supply_stacks, move)
    print("".join([s.pop(0) for s in supply_stacks]))

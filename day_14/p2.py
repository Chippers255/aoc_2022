import numpy


def parse_input() -> list:
    lines = []
    with open("input.txt", "r") as f:
        for row in f:
            fixed_row = row.strip()
            fixed_row = fixed_row.split(" -> ")
            fixed_row = [
                (int(x.split(",")[1]), int(x.split(",")[0])) for x in fixed_row
            ]
            for i in range(1, len(fixed_row)):
                lines.append([fixed_row[i - 1], fixed_row[i]])
    return lines


def line_me(start: tuple, end: tuple) -> list:
    print(start, end)
    if start[0] == end[0]:
        xx = [start[0]]
    else:
        s = sorted([start[0], end[0]])
        xx = range(s[0], s[1] + 1)

    if start[1] == end[1]:
        yy = [start[1]]
    else:
        s = sorted([start[1], end[1]])
        yy = range(s[0], s[1] + 1)
    rocks = []
    print(xx)
    print(yy)
    print()
    for x in xx:
        for y in yy:
            rocks.append((x, y))
    return rocks


def build_map(rocks: list) -> list:
    x_max = 0
    y_min = 999999
    y_max = 0
    for i in rocks:
        x_max = i[0] if i[0] > x_max else x_max
        y_min = i[1] if i[1] < y_min else y_min
        y_max = i[1] if i[1] > y_max else y_max
    map = []
    for x in range(x_max + 3):
        row = []
        for y in range(y_min - 1000, y_max + 1000):
            if (x, y) == (0, 500):
                row.append("+")
            elif x == x_max+2:
                row.append("#")
            elif (x, y) in rocks:
                row.append("#")
            else:
                row.append(".")
        map.append(row)
    return map


def next_space(cur_pos: tuple, map: list) -> tuple:
    if map[cur_pos[0] + 1][cur_pos[1]] == ".":
        return next_space((cur_pos[0] + 1, cur_pos[1]), map)
    if map[cur_pos[0] + 1][cur_pos[1] - 1] == ".":
        return next_space((cur_pos[0] + 1, cur_pos[1] - 1), map)
    if map[cur_pos[0] + 1][cur_pos[1] + 1] == ".":
        return next_space((cur_pos[0] + 1, cur_pos[1] + 1), map)
    return cur_pos

def drop_sand(map: list, start) -> list:
    ns = next_space(start, map)
    if ns == start:
        return map, True
    map[ns[0]][ns[1]] = "o"
    return map, False

if __name__ == "__main__":
    lines = parse_input()
    rocks = []
    for i in lines:
        rocks.extend(line_me(i[0], i[1]))
    map = build_map(rocks)
    c = 0
    for i in range(len(map[0])):
        if map[0][i] == "+":
            start = (0,i)
    #import time
    while True:
        #print("\033c")
        map, done = drop_sand(map, start)
        c += 1
        #for r in map:
        #    print("".join(r))
        if done:
            break
        #time.sleep(0.5)
    for r in map:
        print("".join(r))
    print()
    print(c)

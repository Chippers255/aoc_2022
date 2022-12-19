import csv
import math


def sign(n: int) -> int:
    """And the sign said "Long-haired freaky people need not apply"."""
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        return 0


def move_head(cur_pos: tuple, dir: str, dis: int) -> tuple:
    "What is love? Baby don't hurt me, don't hurt me, no more."
    x, y = cur_pos
    if dir == "U":
        y += dis
    if dir == "D":
        y -= dis
    if dir == "R":
        x += dis
    if dir == "L":
        x -= dis
    return (x, y)


def move_tail(cur_pos: tuple, head_pos: tuple) -> tuple:
    """I like to move it, move it. You like to... MOVE IT."""
    dis = math.dist(head_pos, cur_pos)
    if dis < 2:
        return cur_pos
    else:
        pos_dif = tuple([x[0] - x[1] for x in zip(head_pos, cur_pos)])
        dif_x = 1 * sign(pos_dif[0])
        dif_y = 1 * sign(pos_dif[1])
        new_pos = tuple([sum(x) for x in zip(cur_pos, (dif_x, dif_y))])
        return new_pos


def book_keeper(records: dict, new_pos: tuple) -> dict:
    """The silence is golden. To books I am beholden. I know I'm bad, cuz of the knowledge that I'm holdin!"""
    if new_pos in records:
        records[new_pos] += 1
    else:
        records[new_pos] = 0
    return records


if __name__ == "__main__":
    head_pos = (0, 0)
    # tail_pos = (0,0)
    head_visits = {(0, 0): 1}
    # tail_visits = {(0,0): 1}
    other_pos = [(0, 0) for _ in range(9)]
    other_visits = [{(0, 0): 1} for _ in range(9)]

    with open("input.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            for i in range(int(row[1])):
                head_pos = move_head(head_pos, row[0], 1)
                head_visits = book_keeper(head_visits, head_pos)
                # tail_pos = move_tail(tail_pos, head_pos)
                # tail_visits = book_keeper(tail_visits, tail_pos)
                for i in range(9):
                    relative_head = head_pos if i == 0 else other_pos[i - 1]
                    other_pos[i] = move_tail(other_pos[i], relative_head)
                    other_visits[i] = book_keeper(other_visits[i], other_pos[i])

    # part 1
    # print(len(tail_visits))
    print(len(other_visits[0]))

    # part 2
    print(len(other_visits[8]))

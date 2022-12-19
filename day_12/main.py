import math
import numpy
from typing import Tuple
import time

def make_numbers(char: str) -> int:
    """Letter can be number too you know."""
    if char == "E":
        return 26
    elif char == "S":
        return 1
    else:
        return ord(char) - 96


def build_landscape(file_name: str) -> numpy.array:
    """No Bob the Builders were harmed in the making of this numpy array."""
    landscape = []
    with open(file_name, "r") as f:
        for row in f:
            landscape.append(list(row.strip()))
    landscape = numpy.array(landscape)
    start = numpy.where(landscape=="S")
    start = (start[0][0], start[1][0])
    goal = numpy.where(landscape=="E")
    goal = (goal[0][0], goal[1][0])

    vect = numpy.vectorize(make_numbers)
    return vect(landscape), start, goal


def check_power_level(position: tuple, goal: tuple, map: numpy.array) -> float:
    """something over 6000"""
    #return map[goal[0], goal[1]] - map[start[0], start[1]]
    #return math.dist(position, goal)
    return abs(goal[0] - position[0]) + abs(goal[1] - position[1])
    #return math.dist(position, goal) + map[goal[0], goal[1]] - map[start[0], start[1]]


def popping(pq: list) -> Tuple[tuple, float, list]:
    """There is a subreddit dedicated to this."""
    pq = sorted(pq, key=lambda x: x[1], reverse=True)
    smol_pos, smol_score = pq.pop()
    return smol_pos, smol_score, pq


def look(position: tuple, map: numpy.array) -> list:
    """I can see clearly now the rain has gone."""
    x, y = position
    max_x = len(map) - 1
    max_y = len(map[0]) - 1
    around = [
        (x, y+1),
        (x+1, y),
        (x, y-1),
        (x-1, y),
    ]

    valid_pos = []
    for xx, yy in around:
        if xx >= 0 and xx <= max_x and yy >= 0 and yy <= max_y:
            if (map[xx, yy] - map[x, y]) <= 1:
                valid_pos.append((xx,yy))
    return valid_pos


def a_ster(start: tuple, goal: tuple, map: numpy.array):
    """Thanks wiki-bro... maybe I should donate that $2 they keep asking for."""
    # What if all data structures were dictionaries... except, I guess, my queue
    pq = [(start, check_power_level(start, goal, map)),]
    came_from = {}
    travel_distance = {start: 0}
    estimated_scores = {start: check_power_level(start, goal, map)}
    import copy
    mm = copy.deepcopy(landscape)

    while len(pq) > 0:
        cur_pos, priority, pq = popping(pq)
        if cur_pos == goal:
            break
        score = travel_distance[cur_pos] + 1
        mm[cur_pos[0], cur_pos[1]] = -10
        for neighbour in look(cur_pos, map):
            if neighbour not in travel_distance or score < travel_distance[neighbour]:
                mm[neighbour[0], neighbour[1]] = -18
                came_from[neighbour] = cur_pos
                travel_distance[neighbour] = score
                priority = score + check_power_level(neighbour, goal, map)
                estimated_scores[neighbour] = priority
                pq.append((neighbour, priority))

    if cur_pos != goal:
        return [x for x in range(999999)]
    path = []
    cur_pos = goal
    while cur_pos != start:
        path.append(cur_pos)
        cur_pos = came_from[cur_pos]
    path.reverse()
    return path


if __name__ == "__main__":
    """And. Here. We. Go!"""
    # part 1
    landscape, start, goal = build_landscape("test.txt")
    path = a_ster(start, goal, landscape)
    print(len(path))

    # part 2
    best = 99999
    landscape, _, goal = build_landscape("test.txt")
    starts = numpy.where(landscape==1)
    for i in range(len(starts[0])):
        start = (starts[0][i], starts[1][i])
        path = a_ster(start, goal, landscape)
        if len(path) < best:
            best = len(path)
    print(best)

import numpy


def big_chungus(trees: list, min_height: int) -> bool:
    """https://i.kym-cdn.com/photos/images/facebook/001/447/699/3a0.png"""
    wee_folk = len([i for i in trees if i >= min_height])
    return wee_folk == 0


def failed_sneak_roll(grid: list, row: int, col: int) -> bool:
    """Is A Failed Stealth Check Worse Than Not Sneaking?"""
    if big_chungus(grid[row, :col], grid[row][col]): # left
        return True
    if big_chungus(grid[row, col+1:], grid[row][col]): # right
        return True
    if big_chungus(grid[:row, col], grid[row][col]): # up
        return True
    if big_chungus(grid[row+1:, col], grid[row][col]): # down
        return True
    return False


#lst.reverse()
def view_distance(trees: list, min_height: int) -> int:
    """Can't See The Forest For The Trees"""
    cps = 0
    for i in range(len(trees)):
        if trees[i] < min_height:
            cps = 1 if i == 0 else cps + 1
        else:
            cps = 1 if i == 0 else cps + 1
            return cps
    return cps


def don_cheadle_score(grid: list, row: int, col: int) -> int:
    """https://www.youtube.com/watch?v=TwJaELXadKo"""
    cps = view_distance(list(reversed(grid[row, :col])), grid[row][col]) # left
    cps *= view_distance(grid[row, col+1:], grid[row][col]) # right
    cps *= view_distance(list(reversed(grid[:row, col])), grid[row][col]) # up
    cps *= view_distance(grid[row+1:, col], grid[row][col]) # down
    return cps


if __name__ == "__main__":
    grid = []
    largest_cps = 0
    with open("input.txt", "r") as f:
        for row in f:
            fixed_row = list(map(int, list(row.strip())))
            grid.append(fixed_row)
    grid = numpy.array(grid)

    row_edge = len(grid) - 1
    col_edge = len(grid[0]) - 1

    count = 0
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if row in [0, row_edge] or col in [0, col_edge] or failed_sneak_roll(grid, row, col):
                count += 1
            largest_cps = max([largest_cps, don_cheadle_score(grid, row, col)])
    print(count)
    print(largest_cps)
    print()

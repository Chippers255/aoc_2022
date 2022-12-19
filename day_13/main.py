import ast
import types


def make_iterator(some_list):
    """Makes my evaluation function easier."""
    return (v if type(v) == int else make_iterator(v) for v in some_list)


def get_data() -> list:
    """Parse that input in the cheap way brother."""
    pairs = []
    with open("input.txt", "r") as f:
        current_pair = []
        for row in f:
            fixed_row = row.strip()
            if fixed_row == "":
                pairs.append(current_pair)
                current_pair = []
            else:
                # Why parse the data when it is already valid python code that we can evaluate?
                fixed_row = ast.literal_eval(fixed_row)
                fixed_row = make_iterator(fixed_row)
                current_pair.append(fixed_row)
        pairs.append(current_pair)
        current_pair = []
    return pairs

def get_data_2() -> list:
    """Parse that input in the cheap way brother."""
    packages = []
    with open("input.txt", "r") as f:
        for row in f:
            fixed_row = row.strip()
            if fixed_row == "":
                continue
            else:
                # Why parse the data when it is already valid python code that we can evaluate?
                packages.append(ast.literal_eval(fixed_row))
    return packages


def smol_left(left, right):
    """Recursion and iteration..."""
    if left is None and (type(right) == int or isinstance(right, types.GeneratorType)):
        return True
    if (type(left) == int or isinstance(left, types.GeneratorType)) and right is None:
        return False

    if isinstance(left, types.GeneratorType) and isinstance(right, types.GeneratorType):
        c = 0
        while True:
            c += 1
            l = next(left, None)
            r = next(right, None)
            if l is None and r is None:
                break
            res = smol_left(l, r)
            if res is not None:
                return res

    if type(left) == int and type(right) == int:
        if left < right:
            return True
        if left > right:
            return False

    if isinstance(left, types.GeneratorType) and type(right) == int:
        return smol_left(left, (v for v in [right]))

    if isinstance(right, types.GeneratorType) and type(left) == int:
        return smol_left((v for v in [left]), right)

    return None


def michael_buble(packages):
    """Back to basics baby, also I can't think of another sort function that works with this evaluation I wrote (smol_left)."""
    num_packages = len(packages)
    for i in range(num_packages - 1):
        for j in range(0, num_packages - i - 1):
            a = make_iterator(packages[j])
            b = make_iterator(packages[j+1])
            if not smol_left(a, b):
                packages[j], packages[j + 1] = packages[j + 1], packages[j]
    return packages


if __name__ == "__main__":
    packages = get_data()

    # Part 1
    score = 0
    for p in range(len(packages)):
        a = packages[p][0]
        b = packages[p][1]
        res = smol_left(a, b)
        if res:
            score += p + 1
    print(score)
    print()

    # Part 2
    package_list = get_data_2()
    package_list.append([[2]])
    package_list.append([[6]])
    package_list = michael_buble(package_list)
    score = []
    for p in range(len(package_list)):
        if package_list[p] == [[2]] or package_list[p] == [[6]]:
            score.append(p+1)
    print(score[0] * score[1])

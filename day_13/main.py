import ast
import types

def make_iterator(some_list):
    return (v if type(v) == int else make_iterator(v) for v in some_list)

def get_data() -> list:
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

def smol_left(left, right, depth):
        print(depth, left, right)
        if left is None and (type(right) == int or isinstance(right, types.GeneratorType)):
            print(depth, "left is empty and right is not")
            return True
        if (type(left) == int or isinstance(left, types.GeneratorType)) and right is None:
            print(depth, "right is empty and left is not")
            return False
        
        if isinstance(left, types.GeneratorType) and isinstance(right, types.GeneratorType):
            print(depth, "both sides are lists")
            c = 0
            while True:
                c += 1
                print(depth, f"loop iteration {c}")
                l = next(left, None)
                r = next(right, None)
                if l is None and r is None:
                    print(depth, "both sides are None")
                    break
                res = smol_left(l, r, depth+1)
                if res is not None:
                    return res
                else:
                    print(depth, "NOTHING")
        
        if type(left) == int and type(right) == int:
            print(depth, "both sides are ints")
            if left < right:
                return True
            if left > right:
                return False
        
        if isinstance(left, types.GeneratorType) and type(right) == int:
            print(depth, "left is a list and right is an int")
            return smol_left(left, (v for v in [right]), depth+1)

        if isinstance(right, types.GeneratorType) and type(left) == int:
            print(depth, "left is an int and right is a list")
            return smol_left((v for v in [left]), right, depth+1)

        if left is None and right is None:
            print(depth, "both sides are None")
            return None

        print(depth, "could not find a case")
        return None

if __name__ == "__main__":
    packages = get_data()
    score = 0
    for p in range(len(packages)):
        print("---------------------------------------------------------")
        print("Pair", p)
        a = packages[p][0]
        b = packages[p][1]
        res = smol_left(a,b,0)
        print()
        print(res)
        print()
        print()
        if res:
            score += (p + 1)
    print(score)
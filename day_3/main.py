import csv


def weirdo_to_value(weirdo: str) -> int:
    return ord(weirdo) - 38 if weirdo.isupper() else ord(weirdo) - 96


# part 1
priority_sum = 0
with open("input.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        row_list = list(row[0])
        half = int(len(row_list) / 2)
        c1 = set(row_list[:half])
        c2 = set(row_list[half:])
        weirdo = c1.intersection(c2).pop()
        priority_sum += weirdo_to_value(weirdo)
print(priority_sum)


# part 2
priority_sum = 0
row_peeps = []
with open("input.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        row_list = list(row[0])
        row_peeps.append(row_list)
        if len(row_peeps) == 3:
            sack_1 = set(row_peeps[0])
            sack_2 = set(row_peeps[1])
            sack_3 = set(row_peeps[2])
            weirdo = sack_1.intersection(sack_2).intersection(sack_3).pop()
            priority_sum += ord(weirdo) - 38 if weirdo.isupper() else ord(weirdo) - 96
            row_peeps = []
print(priority_sum)

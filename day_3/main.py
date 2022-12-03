import csv

priority_sum = 0

with open("input.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        row_list = list(row[0])
        half = int(len(row_list) / 2)
        c1 = set(row_list[:half])
        c2 = set(row_list[half:])
        weirdo = list(c1.intersection(c2))[0]
        priority_sum += ord(weirdo) - 38 if weirdo.isupper() else ord(weirdo) - 96

print(priority_sum)

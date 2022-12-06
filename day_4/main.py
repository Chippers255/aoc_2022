import csv

i_like_pears = 0
i_like_wraps = 0
with open("input.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        elf_1 = row[0].split('-')
        elf_2 = row[1].split('-')
        elf_1 = set(range(int(elf_1[0]), int(elf_1[1]) + 1))
        elf_2 = set(range(int(elf_2[0]), int(elf_2[1]) + 1))
        if elf_1.issubset(elf_2) or elf_2.issubset(elf_1):
            i_like_pears += 1
        if len(elf_1.intersection(elf_2)) > 0:
            i_like_wraps += 1
print(i_like_pears)
print(i_like_wraps)

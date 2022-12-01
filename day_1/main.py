import csv

elf_list = []
current_elf = 0

with open("input.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) > 0:
            current_elf += int(row[0])
        else:
            elf_list.append(current_elf)
            current_elf = 0

elf_list.sort(reverse=True)

fattest_elf = elf_list[0]
top_3_fatties = sum(elf_list[:3])

print(fattest_elf)
print(top_3_fatties)

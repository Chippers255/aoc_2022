import tqdm

class Monkey:
    def __init__(self, starting_items: list, operation, check: int, next: tuple) -> None:
        self.items = starting_items
        self.operation = operation
        self.check = check
        self.current_item = None
        self.true_monke, self.false_monke = next
        self.inspection_count = 0
    
    def test(self, x: int) -> bool:
        if x % self.check == 0:
            return True
        return False

    def run_round(self, x) -> list:
        send_it = []
        while len(self.items) > 0:
            i = self.items.pop(0)
            i = self.operation(i)
            self.inspection_count += 1
            i = int(i%x) # only figured this out thanks to chatgpt, so I am not submitting my answer
            if self.test(i):
                send_it.append((i, self.true_monke))
            else:
                send_it.append((i, self.false_monke))
        return send_it

if __name__ == "__main__":
    """
    monkeys = [
        Monkey([77,69,76,77,50,58], lambda x: x * 11, 5, (1,5)),
        Monkey([75,70,82,83,96,64,62], lambda x: x + 8, 17, (5,6)),
        Monkey([53], lambda x: x * 3, 2, (0,7)),
        Monkey([85,64,93,64,99], lambda x: x + 4, 7, (7,2)),
        Monkey([61,92,71], lambda x: x * x, 3, (2,3)),
        Monkey([79,73,50,90], lambda x: x + 2, 11, (4,6)),
        Monkey([50,89], lambda x: x + 3, 13, (4,3)),
        Monkey([83,56,64,58,93,91,56,65], lambda x: x + 5, 19, (1,0))
    ]
    """
    monkeys = [
        Monkey([79,98], lambda x: x * 19, 23, (2,3)),
        Monkey([54,65,75,74], lambda x: x + 6, 19, (2,0)),
        Monkey([79,60,97], lambda x: x * x, 13, (1,3)),
        Monkey([74], lambda x: x + 3, 17, (0,1))
    ]

    val = 23*19*13*17

    for round in range(10000):
        for m in monkeys:
            new_items = m.run_round(val)
            for i, n in new_items:
                monkeys[n].items.append(i)
        if round + 1 in [1,20,1000,2000,3000,4000,5000,6000,7000,8000,9000]:
            print(round + 1)
            print([m.inspection_count for m in monkeys])
            print()

    monkeys.sort(key=lambda x: x.inspection_count, reverse=True)
    print([m.inspection_count for m in monkeys])
    print(monkeys[0].inspection_count * monkeys[1].inspection_count)

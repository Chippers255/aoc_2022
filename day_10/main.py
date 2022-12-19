from typing import Tuple

class ElfishComputationException(Exception):
    """
    If you try to knock me, you'll get mocked.
    I'll stir fry you in my wok.
    Your knees'll start shaking and your fingers pop.
    Like a pinch on the neck of Mr. Spock.
    """
    pass

class CPU:
    """I made a class because Taras says he prefers OO over functions. Also here is a tune...
    
    We are the Priests of the Temples of Syrinx.
    Our great computers fill the hallowed halls.
    We are the Priests of the Temples of Syrinx.
    All the gifts of life are held within our walls.
    """

    def __init__(self, command_list: list) -> None:
        """
        You don’t get something for nothing.
        You don’t get freedom for free.
        You won’t get wise.
        With the sleep still in your eyes.
        No matter what your dreams might be.
        """
        self.clock = 0
        self.X = 1
        self.command_list = command_list
        self.busy = 0
        self.current_job = None
        self.memory = 0
        self.screen = []

    def run_command(self) -> None:
        """
        Master, master.
        Master of puppets, I'm pulling your strings.
        Twisting your mind and smashing your dreams.
        Blinded by me, you can't see a thing.
        Just call my name 'cause I'll hear you scream.
        """
        command = self.command_list.pop(0).split(" ")
        if command[0] == "noop":
            self.current_job = "noop"
            self.busy = 1
            self.memory = 0
        elif command[0] == "addx":
            self.current_job = "addx"
            self.busy = 2
            self.memory = int(command[1])
        else:
            raise ElfishComputationException("DOES NOT COMPUTE")

    def tick(self) -> Tuple[int, int]:
        """
        Time goes by so slowly for those who wait.
        No time to hesitate.
        Those who run seem to have all the fun.
        I'm caught up, I don't know what to do
        """
        self.clock += 1
        if self.clock % 40 == 1:
            self.screen.append([])
        if ((self.clock % 40) - 1) in [self.X-1, self.X, self.X+1]:
            self.screen[-1].append("#")
        else:
            self.screen[-1].append(".")
        ogX = self.X
        if self.current_job is None:
            self.run_command()
        self.busy -= 1
        if self.busy == 0:
            self.current_job = None
            self.X += self.memory
        return self.clock, ogX


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        cpu = CPU([c.strip() for c in f])
    siggys = 0
    while True: # a risky move
        clock, X = cpu.tick()
        if clock in [20,60,100,140,180,220]:
            print(clock, X)
            siggys += (clock * X)
        if len(cpu.command_list) <= 0 and cpu.current_job is None:
            break
    print()
    print(siggys)
    print()
    for i in cpu.screen:
        print(''.join(i))
import brain
import names
import math
import numpy
import random


class Human:
    def __init__(self, new_brain: brain.Brain, goal: tuple, bounds: tuple, family_name: str = None) -> None:
        self.first_name = names.get_first_name()
        self.last_name = names.get_last_name() if family_name is not None else family_name
        self.brain = new_brain
        self.goal = goal
        self.travel_distance = 0
        self.goal_distance = None
        self.x_max, self.y_max = bounds
        self.height = 1
        self.moves =  {
            "Order": "",
            "BAD": 0
        }
        self.position = (0,0)
        #self.position = (random.randint(0,self.x_max), random.randint(0, self.y_max))
        self.get_bearings()
        self.visits = {self.position: 1}
        #self.rando_start_refresh()


    def rando_start_refresh(self):
        self.position = (random.randint(0,self.x_max), random.randint(0, self.y_max))
        self.get_bearings()
        self.visits = {self.position: 1}
        while self.goal_distance < 2.0:
            self.position = (random.randint(0,self.x_max), random.randint(0, self.y_max))
            self.get_bearings()
            self.visits = {self.position: 1}

    def get_bearings(self) -> None:
        """Using GPS let's figure out how far away from E we are"""
        self.goal_distance = math.dist(self.position, self.goal)
    
    def look(self, map):
        x, y = self.position
        inputs = [
            map[x,y],
            map[self.goal[0], self.goal[1]],
            self.goal[0] - x,
            self.goal[1] - y
        ]

        around = [
            (x, y+1),
            (x+1, y+1),
            (x+1, y),
            (x+1, y-1),
            (x, y-1),
            (x-1, y-1),
            (x-1, y),
        ]

        for xx, yy in around:
            if xx >= 0 and xx <= self.x_max and yy >= 0 and yy <= self.y_max:
                n = map[xx, yy] - map[x, y]
                inputs.append(n if n <= 1 else -30)
            else:
                inputs.append(-30)

        """for i in range(x-3, x+4):
            if i != x:
                if i >= 0 and i <= self.x_max:
                    inputs.append(map[i, y] - map[x, y])
                else:
                    inputs.append(-30)

        for i in range(y-3, y+4):
            if i != y:
                if i >= 0 and i <= self.y_max:
                    inputs.append(map[x, i] - map[x, y])
                else:
                    inputs.append(-30)"""
        
        inputs = numpy.array(inputs)
        inputs.astype(numpy.float64)
        return inputs

    '''def look(self, map: numpy.array) -> list:
        """Get the input array our brain needs to think."""
        x, y = self.position

        inputs = [
            x,
            y,
            map[x, y],
            self.goal[0],
            self.goal[1],
            map[self.goal[0], self.goal[1]],
            map[self.goal[0], self.goal[1]] - map[x, y],
            self.goal_distance,
            self.goal[0] - x,
            self.goal[1] - y,
        ]
        for i in range(x-3, x+4):
            if i >= 0 and i <= self.x_max:
                inputs.append(map[i, y] - map[x, y])
            else:
                inputs.append(-5)
        for i in range(y-3, y+4):
            if i >= 0 and i <= self.y_max:
                inputs.append(map[x, i] - map[x, y])
            else:
                inputs.append(-5)
        #if map[x, y] == 9:
        #    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        #    print(map)
        #    print(inputs)
        #    exit(0)
        inputs = numpy.array(inputs)
        inputs.astype(numpy.float64)
        return inputs'''
        
    def valid_move(self, move: str, map: numpy.array) -> bool:
        ogx, ogy = self.position
        height = map[ogx, ogy]
        x = ogx - 1 if move == "U" else ogx
        x = x + 1 if move == "D" else x
        y = ogy - 1 if move == "L" else ogy
        y = y + 1 if move == "R" else y
        if x < 0 or x > self.x_max or y < 0 or y > self.y_max:
            return False, ogx, ogy
        new_height = map[x, y]
        if abs(new_height - height) > 1:
            return False, ogx, ogy
        return True, x, y

    def move(self, map: numpy.array):
        if self.goal_distance != 0.0:
            input = self.look(map)
            move = self.brain.think(input)

            valid, x, y = self.valid_move(move, map)
            if valid:
                self.position = (x,y)
                self.get_bearings()
                self.travel_distance += 1
                self.moves["Order"] += move
                self.height = map[x, y]
                if (x,y) in self.visits:
                    self.visits[(x,y)] += 1
                else:
                    self.visits[(x,y)] = 1
            else:
                self.moves["BAD"] += 1
    
    def sim(self, map: numpy.array):
        pass


    def check_power_level(self) -> float:
        """IT'S OVER 9000"""
        #return (self.goal_distance + (self.moves["BAD"]*1.5) + self.travel_distance - self.height) * max(self.visits.values())
        #return 0 - self.height + (self.moves["BAD"] / 5.0)
        return -self.height

    def mind_meld(self, other_human):
        """Even Mr. Spock can't keep a straight face at this one."""
        family_name = self.last_name if self.check_power_level() < other_human.check_power_level() else other_human.last_name
        new_brain = brain.Brain()
        new_brain.wrinkles = self.brain.wrinkles
        f = numpy.frompyfunc(wrinkle_baby,2,1)

        # I couldn't think of a sexy way to do this so sue me
        for w in range(len(self.brain.weights)):
            new_brain.weights.append({
                "W": f(self.brain.weights[w]["W"],other_human.brain.weights[w]["W"]),
                "B": f(self.brain.weights[w]["B"],other_human.brain.weights[w]["B"])
            })
        return Human(new_brain, self.goal, (self.x_max, self.y_max), family_name)

def wrinkle_baby(weight, other_weight):
    if numpy.random.rand() <= 0.05:
        return numpy.random.uniform(-1.0, 1.0)
    else:
        return random.choice([weight, other_weight])

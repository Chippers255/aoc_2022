import copy
import random

import brain
import human
import numpy

BEST_GUY = None


def make_numbers(char: str) -> int:
    if char == "E":
        return 27
    else:
        return ord(char) - 96


def build_landscape(file_name: str) -> numpy.array:
    landscape = []
    with open(file_name, "r") as f:
        for row in f:
            landscape.append(list(row.strip()))
    landscape = numpy.array(landscape)
    vect = numpy.vectorize(make_numbers)
    return vect(landscape)


def generate_human() -> human.Human:
    b = (
        brain.Brain()
        .add_layer(brain.BrainWrinkle(11, 64, function="softmax"))
        .add_layer(brain.BrainWrinkle(64, 32, function="softmax"))
        .add_layer(brain.BrainWrinkle(32, 8, function="softmax"))
        .add_layer(brain.BrainWrinkle(8, 4, function="softmax"))
        .build()
    )
    return human.Human(b, (2, 5), (4, 7))


def generate_population(size):
    population = []
    for _ in range(size):
        population.append(generate_human())
    return population


def run_population(population, landscape, rounds):
    for _ in range(rounds):
        for h in population:
            h.move(landscape)
    return population


def next_generation(population):
    global BEST_GUY
    population.sort(key=lambda h: h.check_power_level(), reverse=False)
    breeding_pop = copy.deepcopy(population[:50])
    # breeding_pop.extend(copy.deepcopy(population[-5:-1]))

    if BEST_GUY is None:
        BEST_GUY = copy.deepcopy(population[0])
        print("NEW BEST GUY")
    if BEST_GUY.check_power_level() > population[0].check_power_level():
        BEST_GUY = copy.deepcopy(population[0])
        print("NEW BEST GUY")
    breeding_pop.append(copy.deepcopy(BEST_GUY))
    print(population[0].check_power_level())
    print(population[0].position)
    print(population[0].travel_distance)
    print(population[0].moves)
    new_population = copy.deepcopy(population[:50])
    while len(new_population) < 200:
        a = random.choice(breeding_pop)
        b = random.choice(breeding_pop)
        new_population.append(a.mind_meld(b))
    new_population.extend(generate_population(20))
    for h in new_population:
        h.position = (0, 0)
        # h.rando_start_refresh()
        h.travel_distance = 0
        h.get_bearings()
        h.height = 1
        h.moves = {"Order": "", "BAD": 0}
    return new_population


if __name__ == "__main__":
    landscape = build_landscape("test.txt")

    population = generate_population(1000)
    for i in range(50):
        print(i)
        population = run_population(population, landscape, 50)
        population = next_generation(population)
        print()

    print("--------------------------------------------------------------")
    print("BEST GUY TIME")
    print()
    print(landscape)
    print()
    BEST_GUY.position = (0, 0)
    BEST_GUY.travel_distance = 0
    BEST_GUY.get_bearings()
    BEST_GUY.moves = {"Order": "", "BAD": 0}
    for _ in range(50):
        BEST_GUY.move(landscape)
    print(BEST_GUY.check_power_level())
    print(BEST_GUY.position)
    print(BEST_GUY.travel_distance)
    print(BEST_GUY.moves)
    print()

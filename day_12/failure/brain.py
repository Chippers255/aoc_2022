import math
import random
import time
import typing

import numpy


class BrainWrinkle:
    def __init__(
        self, input_size: int, output_size: int, function: str = "relu"
    ) -> None:
        """Store all required layer data so it can be accessed easily."""
        self.input = input_size
        self.output = output_size
        self.function = function

    @staticmethod
    def relu(inputs: numpy.array) -> numpy.array:
        """An activation function for all hidden layers that returns only positive values or zero."""
        return numpy.maximum(0, inputs)

    @staticmethod
    def softmax(inputs: numpy.array):
        """An activation function for the output layer to get the most probable direction to move."""
        inputs = inputs.astype(numpy.float64)
        try:
            return numpy.exp(inputs) / numpy.sum(numpy.exp(inputs))
        except Exception as err:
            print(inputs)
            print(type(inputs))
            raise (err)

    def think(
        self, inputs: numpy.array, weights: numpy.array, bias: numpy.array
    ) -> numpy.array:
        """Thinking is hard, especially with loops, so use a dot product. This is the bit that would run on
        a GPU if I knew how to do that."""
        thought = numpy.dot(inputs, weights)
        thought = thought + bias
        return self.relu(thought) if self.function == "relu" else self.softmax(thought)


class Brain:
    def __init__(self) -> None:
        """What does a network look like? Does it look like a bitch? O_o"""
        self.wrinkles = []
        self.weights = []

    def add_layer(self, wrinkle: BrainWrinkle) -> None:
        """Who needs a well defined path finding algorith when I can just add more layers?"""
        self.wrinkles.append(wrinkle)
        return self

    def build(self) -> None:
        """Did I seriously just use a builder pattern?"""
        numpy.random.seed(int(time.time()))
        for wrinkle in self.wrinkles:
            self.weights.append(
                {
                    "W": numpy.random.uniform(
                        -1.0, 1.0, size=(wrinkle.input, wrinkle.output)
                    ),
                    "B": numpy.zeros((1, wrinkle.output)),
                }
            )
        return self

    @staticmethod
    def _translate_thought(thought: numpy.array) -> str:
        """Reality can be what ever I make it."""
        max_index = thought.argmax()
        if max_index == 0:
            return "R"
        elif max_index == 1:
            return "D"
        elif max_index == 2:
            return "L"
        elif max_index == 3:
            return "U"
        else:
            raise Exception("somethings wrong I can feel it")

    def think(self, data: numpy.array):
        """Just because you have the ability to think doesn't make you intelligent..."""
        result = data

        for i in range(len(self.wrinkles)):
            input = result
            result = self.wrinkles[i].think(
                input, self.weights[i]["W"], self.weights[i]["B"]
            )

        return self._translate_thought(result)

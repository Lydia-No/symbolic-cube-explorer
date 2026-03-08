class Hypercube:
    """
    Generic N-dimensional hypercube state space.
    """

    def __init__(self, dimension):
        self.dimension = dimension
        self.states = 2 ** dimension

    def apply_axis_flip(self, state, axis):
        return state ^ (1 << axis)

    def neighbors(self, state):
        return [
            self.apply_axis_flip(state, axis)
            for axis in range(self.dimension)
        ]
import random


class Hypercube:

    def __init__(self, dim):
        self.dim = dim
        self.vertices = 2 ** dim

    def neighbors(self, v):
        """
        Return vertices reachable by flipping one bit.
        """
        result = []

        for i in range(self.dim):
            result.append(v ^ (1 << i))

        return result

    def random_walk(self, steps=1000):
        """
        Perform a random walk and emit symbolic sequence
        based on which dimension flipped.
        """

        position = 0
        sequence = []

        for _ in range(steps):

            neighbors = self.neighbors(position)

            next_v = random.choice(neighbors)

            diff = position ^ next_v

            dimension = diff.bit_length() - 1

            symbol = chr(65 + dimension)

            sequence.append(symbol)

            position = next_v

        return sequence

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

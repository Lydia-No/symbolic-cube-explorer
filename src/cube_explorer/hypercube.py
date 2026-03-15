import random
import string


class Hypercube:
    """
    Fast hypercube walker using integer bit operations.
    Vertices are integers in [0, 2^dim).
    """

    def __init__(self, dim: int):

        if dim < 1:
            raise ValueError("Dimension must be >= 1")

        self.dim = dim
        self.symbols = list(string.ascii_uppercase[:dim])

    def random_walk(self, steps: int, return_vertices=False):
        """
        Generate symbolic sequence from hypercube walk.
        """

        vertex = random.randrange(1 << self.dim)

        seq = []
        vertices = [vertex]

        for _ in range(steps):

            d = random.randrange(self.dim)

            vertex ^= 1 << d

            seq.append(self.symbols[d])
            vertices.append(vertex)

        if return_vertices:
            return seq, vertices

        return seq

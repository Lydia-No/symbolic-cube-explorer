from .grammar import simple_letters
from .utils import score_sequence


class CubeGraph:

    def __init__(self):

        self.vertex_neighbors = {

            0:[1,2,4],
            1:[0,3,5],
            2:[0,3,6],
            3:[1,2,7],
            4:[0,5,6],
            5:[1,4,7],
            6:[2,4,7],
            7:[3,5,6]

        }

        edges = [

            (0,1),(0,2),(0,4),
            (1,3),(1,5),
            (2,3),(2,6),
            (3,7),
            (4,5),(4,6),
            (5,7),
            (6,7)

        ]

        self.edge_letters = {}

        for e,l in zip(edges,simple_letters):
            self.edge_letters[tuple(sorted(e))] = l


    def edge_letter(self,v1,v2):

        return self.edge_letters[tuple(sorted((v1,v2)))]


class SymbolicWalker:

    def __init__(self,cube):

        self.cube = cube


    def concept_seed(self,word):

        return sum(ord(c) for c in word) % 8


    def walk(self,start,steps=6):

        current = start
        path = [current]
        seq = []

        for i in range(steps):

            neighbors = self.cube.vertex_neighbors[current]
            nxt = neighbors[i % 3]

            letter = self.cube.edge_letter(current,nxt)

            seq.append(letter)

            current = nxt
            path.append(current)

        return path,seq


    def run_concept(self,concept):

        start = self.concept_seed(concept)

        path,seq = self.walk(start)

        score = score_sequence(seq)

        return start,path,seq,score
def run_symbol_sequence(start_state, sequence, apply_symbol):
    state = start_state
    path = [state]

    for symbol in sequence:
        state = apply_symbol(state, symbol)
        path.append(state)

    return path

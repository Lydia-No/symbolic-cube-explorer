import random


class CubeGraph:
    def __init__(self, dim=4, forbidden_states=None, forbidden_transitions=None):
        self.dim = dim
        self.forbidden_states = set(forbidden_states) if forbidden_states else set()
        self.forbidden_transitions = set(forbidden_transitions) if forbidden_transitions else set()

    def random_vertex(self):
        while True:
            v = "".join(random.choice("01") for _ in range(self.dim))
            if v not in self.forbidden_states:
                return v

    def neighbors(self, state):
        neighbors = []

        for i in range(len(state)):
            flipped = list(state)
            flipped[i] = "1" if state[i] == "0" else "0"
            new_state = "".join(flipped)

            if new_state in self.forbidden_states:
                continue

            # --- transition constraint ---
            if (state, new_state) in self.forbidden_transitions:
                continue

            neighbors.append(new_state)

        return neighbors

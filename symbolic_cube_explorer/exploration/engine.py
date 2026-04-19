import random
from collections import defaultdict, Counter


class ExplorationEngine:
    def __init__(self, cube):
        self.cube = cube
        self.visit_counts = Counter()
        self.transition_counts = defaultdict(Counter)

    def step(self, state):
        neighbors = self.cube.neighbors(state)
        if not neighbors:
            return state

        # --- bias: prefer less visited states ---
        weights = []
        for n in neighbors:
            count = self.visit_counts[n]
            weight = 1 / (1 + count)
            weights.append(weight)

        total = sum(weights)
        probs = [w / total for w in weights]

        next_state = random.choices(neighbors, probs)[0]

        self.visit_counts[next_state] += 1
        self.transition_counts[state][next_state] += 1

        return next_state

    def walk(self, start, steps=100):
        state = start
        trajectory = [state]

        for _ in range(steps):
            state = self.step(state)
            trajectory.append(state)

        return trajectory

    def entropy(self):
        total = sum(self.visit_counts.values())
        if total == 0:
            return 0.0

        import math
        probs = [c / total for c in self.visit_counts.values()]
        return -sum(p * math.log(p + 1e-12) for p in probs)

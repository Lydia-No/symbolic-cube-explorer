import math


def find_cycle(path):
    """
    Detect first cycle in trajectory.
    """
    visited = {}

    for i, state in enumerate(path):

        if state in visited:
            start = visited[state]
            return path[start:i]

        visited[state] = i

    return None


def state_coverage(path, total_states):
    """
    Fraction of cube explored.
    """
    return len(set(path)) / total_states


def transition_counts(path):
    """
    Count transitions between states.
    """
    counts = {}

    for a, b in zip(path[:-1], path[1:]):
        key = (a, b)
        counts[key] = counts.get(key, 0) + 1

    return counts


def trajectory_entropy(path):
    """
    Shannon entropy of visited states.
    """

    counts = {}

    for state in path:
        counts[state] = counts.get(state, 0) + 1

    total = len(path)

    entropy = 0

    for c in counts.values():

        p = c / total

        entropy -= p * math.log2(p)

    return entropy

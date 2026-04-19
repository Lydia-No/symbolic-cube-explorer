class HamiltonianExplorer:
    def __init__(self, cube):
        self.cube = cube
        self.vertex_count = 1 << cube.dims

    def find_paths(self, start=None):
        starts = [start] if start is not None else list(range(self.vertex_count))
        all_paths = []

        for s in starts:
            self._dfs([s], {s}, all_paths)

        unique = []
        seen = set()

        for path in all_paths:
            key = tuple(path)
            if key not in seen:
                seen.add(key)
                unique.append(path)

        return unique

    def _dfs(self, path, visited, all_paths):
        if len(path) == self.vertex_count:
            all_paths.append(path[:])
            return

        current = path[-1]
        for neighbor in self.cube.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                self._dfs(path, visited, all_paths)
                path.pop()
                visited.remove(neighbor)


def generate_hamiltonian_paths(cube, start=None):
    explorer = HamiltonianExplorer(cube)
    return explorer.find_paths(start=start)

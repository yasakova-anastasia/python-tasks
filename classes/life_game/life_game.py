

class LifeGame(object):
    """
    Class for Game life
    """
    def __init__(self, ocean: list[list[int]]):
        self.ocean = ocean

    def get_next_generation(self) -> list[list[int]]:
        self.ocean = [[self._get_next_ocean_elem(i, j)
                       for j in range(len(self.ocean[0]))]
                      for i in range(len(self.ocean))]
        return self.ocean

    def _get_next_ocean_elem(self, i: int, j: int) -> int:
        elem = self.ocean[i][j]
        neighbours = self._get_neighbours(i, j)

        val = {0: 2 if neighbours[2] == 3 else 3 if neighbours[3] == 3 else 0,
               1: 1,
               2: 2 if neighbours[elem] in [2, 3] else 0,
               3: 3 if neighbours[elem] in [2, 3] else 0}

        return val[elem]

    def _get_neighbours(self, i: int, j: int) -> dict[int, int]:
        neighbours = {0: 0, 1: 0, 2: 0, 3: 0}
        dirs = {(idx, jdx) for idx in range(-1, 2)
                for jdx in range(-1, 2) if idx or jdx}
        for k, l in dirs:
            if 0 <= i + l and i + l < len(self.ocean) and \
                    0 <= j + k and j + k < len(self.ocean[0]):
                neighbours[self.ocean[i + l][j + k]] += 1
        return neighbours

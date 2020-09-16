from itertools import count


PATH = 0
WALL = 1


class Cell:
    def __init__(self, coords, num_id, neighbors=None):
        self.coords = coords
        self.num_id = num_id
        if neighbors:
            self.neighbors = neighbors
        else:
            self.neighbors = []
        self.is_intersection = len(self.neighbors) > 2
        self.is_dead_end = len(self.neighbors) == 1

    def __str__(self):
        return f"""{self.num_id}"""

    def __repr__(self):
        a = f"""{self.num_id} :: Coords: {self.coords},  Neighbors: {self.neighbors},"""
        b = f"""Intersection: {self.is_intersection}, Dead End: {self.is_dead_end}"""
        return f"""{a} {b}"""


def visit_cell(coords, matrix):
    width, height = len(matrix[0]), len(matrix)
    row, col = coords

    if (row < 0 or row > height - 1) or (col < 0 or col > width - 1):
        return False
    elif matrix[row][col] == PATH:
        return (row, col)
    else:
        return False


def find_neighbors(coords, matrix):
    row, col = coords

    visited = (
        visit_cell((row - 1, col), matrix),  # North
        visit_cell((row + 1, col), matrix),  # South
        visit_cell((row, col - 1), matrix),  # East
        visit_cell((row, col + 1), matrix),  # West
    )
    return [v for v in visited if v]


def maze2cells(matrix):
    autoid = count(start=0, step=1)

    cells = list()
    for r_idx, row in enumerate(matrix):
        for c_idx, c in enumerate(row):
            coords = (r_idx, c_idx)

            if visit_cell(coords, matrix):
                cells.append(
                    Cell(
                        coords,
                        next(autoid),
                        neighbors=find_neighbors(coords, matrix),
                    )
                )
    return cells

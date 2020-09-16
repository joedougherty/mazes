from itertools import count
from collections import OrderedDict


PATH = 0
WALL = 1


class Cell:
    def __init__(self, coords, neighbors=None):
        self.coords = coords
        if neighbors:
            self.neighbors = neighbors
        else:
            self.neighbors = []

        # Derived Attributes
        self.row, self.col = self.coords
        self.is_intersection = len(self.neighbors) > 2
        self.is_dead_end = len(self.neighbors) == 1

    def __str__(self):
        #return f'''({self.row}, {self.col})'''
        return f"""Neighbors: {self.neighbors}, Intersection: {self.is_intersection}, Dead End: {self.is_dead_end}"""

    def __repr__(self):
        return f"""Neighbors: {self.neighbors}, Intersection: {self.is_intersection}, Dead End: {self.is_dead_end}"""


def discover_cell(coords, matrix):
    width, height = len(matrix[0]), len(matrix)
    row, col = coords

    if any((row < 0, row > height-1, col < 0, col > width-1)):
        return False
    elif matrix[row][col] == PATH:
        return (row, col)
    else:
        return False


def find_neighbors(coords, matrix):
    row, col = coords

    visited = (
        discover_cell((row-1, col), matrix),  # North
        discover_cell((row+1, col), matrix),  # South
        discover_cell((row, col-1), matrix),  # East
        discover_cell((row, col+1), matrix),  # West
    )
    return [v for v in visited if isinstance(v, tuple)]


def maze2adjlist(matrix):
    '''
    Given 
    '''
    cells = OrderedDict()

    for row_idx, row in enumerate(matrix):
        for col_idx, c in enumerate(row):
            coords = (row_idx, col_idx)
            if discover_cell(coords, matrix):
                new_cell = Cell(
                    coords, 
                    find_neighbors(coords, matrix)
                )
                cells.update({coords : new_cell})

    return cells



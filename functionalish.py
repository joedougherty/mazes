from itertools import count
from collections import OrderedDict



from classy import Cell



PATH = 0
WALL = 1


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

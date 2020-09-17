from itertools import count
from collections import OrderedDict


from classymaze import Cell
from mazeutils import ascii_maze2matrix, matrix2str



PATH = 0
WALL = 1


def find_neighbors(coords, matrix):
    row, col = coords

    visited = (
        discover_cell((row - 1, col), matrix),  # North
        discover_cell((row + 1, col), matrix),  # South
        discover_cell((row, col - 1), matrix),  # East
        discover_cell((row, col + 1), matrix),  # West
    )
    return [v for v in visited if isinstance(v, tuple)]


def discover_cell(coords, matrix):
    width, height = len(matrix[0]), len(matrix)
    row, col = coords

    if any((row < 0, row > height - 1, col < 0, col > width - 1)):
        return False
    elif matrix[row][col] == PATH:
        return (row, col)
    else:
        return False


def matrix2adjlist(matrix):
    adjlist = OrderedDict()

    for row_idx, row in enumerate(matrix):
        for col_idx, c in enumerate(row):
            coords = (row_idx, col_idx)
            if discover_cell(coords, matrix):
                new_cell = Cell(coords, find_neighbors(coords, matrix))
                adjlist.update({coords: new_cell})
    return adjlist


def bfs(adjlist, start_coords, goal_coords):
    to_visit = deque()
    visited = set()

    root = adjlist[start_coords]
    root.traversal_mode = True

    to_visit.append(root)

    while to_visit:
        cell = to_visit.popleft()
        visited.add(cell)

        if cell.coords == goal_coords:
            return cell

        # Find adjacent edges that haven't been visited
        for coords in cell.neighbors:
            next_cell = adjlist[coords]
            if next_cell not in visited:
                next_cell.prev = cell
                next_cell.traversal_mode = True
                to_visit.append(next_cell)
    return False


def shortest_path(adjlist, start_coords, goal_coords, root_to_leaf=True):
    path = []

    found = bfs(adjlist, start_coords, goal_coords)

    if not found:
        print("No path found!")
        return False

    path.append(found.coords)

    while found.prev:
        found = found.prev
        path.append(found.coords)

    if root_to_leaf:
        path.reverse()

    return path

from itertools import count
from collections import OrderedDict


from classymaze import Room
from mazeutils import str2nested_list, nested_list2str 



PATH, WALL = ' ', '#'


def find_neighbors(coords, nested_list):
    row, col = coords

    visited = (
        discover_room((row - 1, col), nested_list),  # North
        discover_room((row + 1, col), nested_list),  # South
        discover_room((row, col - 1), nested_list),  # East
        discover_room((row, col + 1), nested_list),  # West
    )
    return [v for v in visited if isinstance(v, tuple)]


def discover_room(coords, nested_list):
    width, height = len(nested_list[0]), len(nested_list)
    row, col = coords

    if any((row < 0, row > height - 1, col < 0, col > width - 1)):
        return False
    elif nested_list[row][col] == PATH:
        return (row, col)
    else:
        return False


def nested_list2adjlist(nested_list):
    adjlist = OrderedDict()

    for row_idx, row in enumerate(nested_list):
        for col_idx, c in enumerate(row):
            coords = (row_idx, col_idx)
            if discover_room(coords, nested_list):
                new_room = Room(coords, find_neighbors(coords, nested_list))
                adjlist.update({coords: new_room})
    return adjlist


def bfs(adjlist, start_coords, goal_coords):
    to_visit = deque()
    visited = set()

    root = adjlist[start_coords]
    root.traversal_mode = True

    to_visit.append(root)

    while to_visit:
        room = to_visit.popleft()
        visited.add(room)

        if room.coords == goal_coords:
            return room

        # Find adjacent edges that haven't been visited
        for coords in room.neighbors:
            next_room = adjlist[coords]
            if next_room not in visited:
                next_room.prev = room
                next_room.traversal_mode = True
                to_visit.append(next_room)
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

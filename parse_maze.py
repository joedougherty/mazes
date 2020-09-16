from itertools import count


from maze_utils import Cell, visit_cell, find_neighbors, maze2cells, PATH, WALL



def printable_map(m):  
    p = ''
    for row in m:
        p += ' '.join(row) + '\n'
    return p


def extract_path(maze):
    autoid = count(start=0, step=1)
    
    path = []
    for row in maze:
        new_row = []
        for col in row:
            if col == PATH:
                v = str(next(autoid)).zfill(2)
            else:
                v = ('  ')
            new_row.append(v)

        path.append(new_row)
    return path
                

# Source: https://py.checkio.org/en/mission/open-labyrinth/share/574bd1ded68c9705c5d6f07c6206be12/
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


adj_list = maze2cells(maze)

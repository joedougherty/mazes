from itertools import count


from maze_utils import maze2adjlist, PATH, WALL


def matrix2str(m):
    p = ""
    for row in m:
        p += " ".join(row) + "\n"
    return p


def extract_path(maze):
    autoid = count(start=0, step=1)
    highest = 0

    path = []
    for row in maze:
        new_row = []
        for col in row:
            if col == PATH:
                v = str(next(autoid)).zfill(2)
                highest = v
            else:
                v = "  "
            new_row.append(v)

        path.append(new_row)
    return (path, highest)


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


def example():
    ascii_rep, total_nodes = extract_path(maze)
    print(f'''\nTotal Nodes: {total_nodes}''')
    print(matrix2str(ascii_rep))


res = maze2adjlist(maze)

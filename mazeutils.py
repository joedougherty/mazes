def ascii_maze2matrix(ascii_maze, path, wall):
    matrix = []
    for row in ascii_maze.split('\n'):
        new_row = []
        for col in row:
            if col == path:
                new_row.append(0)
            elif col == wall:
                new_row.append(1)
        matrix.append(new_row)
    return matrix


def matrix2str(m):
    p = ""
    for row in m:
        p += " ".join([str(e) for e in row]) + "\n"
    return p

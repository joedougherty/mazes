'''
In general:
    str2matrix(matrix2str(X)) == matrix2str(str2matrix(X))
'''

def str2matrix(maze_str):
    return [list(e) for e in maze_str.split('\n')]


def matrix2str(m):
    p = ""
    for row in m:
        p += "".join([str(e) for e in row]) + "\n"
    return p

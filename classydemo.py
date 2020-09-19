from classymaze import Maze

from mazeutils import str2matrix, matrix2str


PATH, WALL = ' ', '#'

tiny = '''
######
#    #
# # ##
######
'''.strip()

demo = Maze(tiny, path=PATH, wall=WALL)

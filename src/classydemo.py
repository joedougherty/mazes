from classymaze import Maze


PATH, WALL = ' ', '#'

tiny = '''
######
#    #
# # ##
######
'''.strip()


demo = Maze(tiny, path=PATH, wall=WALL)

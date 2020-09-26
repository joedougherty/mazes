from functionalish import nested_list2adjlist, bfs
from mazeutils import str2nested_list, nested_list2str

from labyrinth import tiny, medium, big


PATH, WALL = ' ', '#'


adjlist = nested_list2adjlist(str2nested_list(tiny))
good_path = bfs(adjlist, (1,1), (2,3)) 
bad_path = bfs(adjlist, (1,1), (4,3)) # (4,3) is a WALL

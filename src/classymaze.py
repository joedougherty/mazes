from blessings import Terminal

from collections import OrderedDict, deque

from mazeutils import str2nested_list, nested_list2str


t = Terminal()


class Room:
    """
    A representation of a room in the maze.

    :param coords: Coordinates (row, col)
    :type  coords: tuple

    :param neighbors: List of neighboring rooms as coords (see above)
    :type  neighbors: list

    :param row: Row ID
    :type  row: int

    :param col: Col ID
    :type  col: int

    :param is_intersection: Does this room have more than 2 neighors?
    :type  is_intersection: bool

    :param is_dead_end: Does this room have exactly one neighbor?
    :type  is_dead_end: bool

    :param prev: Reference to previous Room or None
    :param type: Room or None
    """
    def __init__(self, coords, neighbors=None, traversal_mode=False):
        self.coords = coords
        if neighbors:
            self.neighbors = neighbors
        else:
            self.neighbors = []

        # Derived Attributes
        self.row, self.col = self.coords
        self.is_intersection = len(self.neighbors) > 2
        self.is_dead_end = len(self.neighbors) == 1

        # These don't come into play until the traversal stage
        self.prev = None
        self.traversal_mode = traversal_mode

    def __repr__(self):
        if self.traversal_mode and self.prev:
            return f"""{self.prev} -> {self.coords}"""
        elif self.traversal_mode and not self.prev:
            return f"""{self.coords}"""
        else:
            return f"""Neighbors={self.neighbors}, Intersection={self.is_intersection}, Dead End={self.is_dead_end}"""


class Maze:
    """
    Give me a matrix and I'll do some maze analysis. Sound good?

    :param matrix: Matrix representing the path/wall rooms that compose the maze
    :type  matrix: list

    :param path: Representation of path rooms
    :type  path: int

    :param wall: Representation of wall rooms
    :type  wall: int

    :param room_width: How wide the rooms are (function of max # of digits it takes to represent highest numbered node)
    :type  room_width: int
    """
    def __init__(self, input_maze, path=' ', wall='#', room_width=2):
        if isinstance(input_maze, str):
            self.maze_as_matrix = str2nested_list(input_maze)
        elif isistance(maze_as_matrix, list):
            self.maze_as_matrix = input_maze
        else:
            msg = 'Maze needs to be instantiated w/ a str or list of lists. I received: {maze_as_matrix} of type: {type(maze_as_matrix)}.'
            raise TypeError(msg)
        self.path = path
        self.wall = wall
        self.room_width = room_width
        self.adjlist = self.to_adjlist()

    def show_vertices(self, highlight_path=None):
        if not highlight_path:
            print(nested_list2str(self.diagram_path(self.room_width)))
        else:
            m = self.diagram_path(self.room_width, highlight_rooms=highlight_path)
            print(nested_list2str(m))

    def as_ascii(self, highlight_rooms=None):
        if not highlight_rooms:
            highlight_rooms = []

        new_rep = []
        for r_idx, row in enumerate(self.maze_as_matrix):
            new_row = []
            for c_idx, col in enumerate(row):
                if col == self.wall:
                    new_row.append("#")
                elif col == self.path and (r_idx, c_idx) in highlight_rooms:
                    new_row.append(t.bright_red("*"))
                elif col == self.path:
                    new_row.append(" ")
                else:
                    raise ValueError(
                        "Matrices must be composed of only {self.path} and {self.wall}!"
                    )
            new_rep.append(new_row)
        print(nested_list2str(new_rep))

    def count_path_nodes(self):
        """ Returns the total number of nodes that match `self.path` in self.maze_as_matrix. """
        return sum([r.count(self.path) for r in self.maze_as_matrix])

    def diagram_path(self, int_width=None, highlight_rooms=None):
        """
        A graphic representation of the nodes.
        """
        if not highlight_rooms:
            highlight_rooms = []

        if not int_width:
            int_width = self.room_width

        path = []
        for r_idx, row in enumerate(self.maze_as_matrix):
            new_row = []
            for c_idx, col in enumerate(row):
                row_rep, col_rep = str(r_idx).zfill(2), str(c_idx).zfill(2)

                coords_rep = f"""({row_rep}, {col_rep})"""
                if col == self.path and ((r_idx, c_idx) in highlight_rooms):
                    new_row.append(t.bold_red(coords_rep))
                elif col == self.path and (r_idx, c_idx) not in highlight_rooms:
                    new_row.append(coords_rep)
                else:
                    new_row.append(" " * 8)

            path.append(new_row)
        return path

    def discover_room(self, coords):
        """
        Given coords (row, col):
            if that room is a path room:
                return the coords (row, col)
            else:
                # it's out of bounds or not a path room
                return False
        """
        width, height = len(self.maze_as_matrix[0]), len(self.maze_as_matrix)
        row, col = coords

        if any((row < 0, row > height - 1, col < 0, col > width - 1)):
            return False
        elif self.maze_as_matrix[row][col] == self.path:
            return (row, col)
        else:
            return False

    def find_neighbors(self, coords):
        """
        Given coords (row, col):
            check the neighbors to the N, S, E, W
            if they contain coords, return them

        If no neighbors found, return []
        """
        row, col = coords

        visited = (
            self.discover_room((row - 1, col)),  # North
            self.discover_room((row + 1, col)),  # South
            self.discover_room((row, col - 1)),  # East
            self.discover_room((row, col + 1)),  # West
        )
        return [v for v in visited if isinstance(v, tuple)]

    def to_adjlist(self):
        """
        Creates an adjacency list from `self.maze_as_matrix`.

        Returns adjacenct list as a dict where:
            key -> coords,
            val -> Room objects (coords, found neighbors, etc.)

        # EXAMPLE #
        matrix = [
           [0, 1],
           [0, 1],
        ]

        simple = Maze(matrix, 0, 1)
        simple.to_adjlist()

        # RESULTS #
        OrderedDict([
            ((0, 0), (Neighbors=[(1, 0)], Intersection=False, Dead End=True),
            ((1, 0), (Neighbors=[(0, 0)], Intersection=False, Dead End=True)
        ])

        In this example, either way you start the only way to finish is to go to the other.
        """
        adjlist = OrderedDict()

        for row_idx, row in enumerate(self.maze_as_matrix):
            for col_idx, c in enumerate(row):
                coords = (row_idx, col_idx)
                if self.discover_room(coords):
                    new_room = Room(coords, self.find_neighbors(coords))
                    adjlist.update({coords: new_room})

        return adjlist

    def bfs(self, start_coords, goal_coords):
        """
        Explores the Adjancency List `self.adjlist` for a path from `start_coords` to `goal_coords`.

        If found, returns a reference to found Room at `goal_coords`.
        Otherwise, returns False.
        """
        to_visit = deque()
        visited = set()

        root = self.adjlist[start_coords]
        root.traversal_mode = True

        to_visit.append(root)

        while to_visit:
            room = to_visit.popleft()
            visited.add(room)

            if room.coords == goal_coords:
                return room

            # Find adjacent edges that haven't been visited
            for coords in room.neighbors:
                next_room = self.adjlist[coords]
                if next_room not in visited:
                    next_room.prev = room
                    next_room.traversal_mode = True
                    to_visit.append(next_room)

        return False

    def shortest_path(self, start_coords, goal_coords, root_to_leaf=True):
        rooms = []

        found = self.bfs(start_coords, goal_coords)

        if not found:
            print("No path found!")
            return False

        rooms.append(found.coords)

        while found.prev:
            found = found.prev
            rooms.append(found.coords)

        if root_to_leaf:
            rooms.reverse()

        return rooms

    def __repr__(self):
        height, width = len(self.maze_as_matrix), len(self.maze_as_matrix[0])
        total_rooms = self.count_path_nodes()

        desc = '''A {} x {} maze with {} rooms.\n`.as_ascii()` prints an ASCII representation of the maze.'''
        return desc.format(height, width, total_rooms)

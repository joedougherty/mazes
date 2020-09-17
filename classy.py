from blessings import Terminal


from collections import OrderedDict, deque


t = Terminal()


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


class Cell:
    """
    A representation of a cell in the maze.

    :param coords: Coordinates (row, col)
    :type  coords: tuple

    :param neighbors: List of neighboring cells as coords (see above)
    :type  neighbors: list

    :param row: Row ID
    :type  row: int

    :param col: Col ID
    :type  col: int

    :param is_intersection: Does this cell have more than 2 neighors?
    :type  is_intersection: bool

    :param is_dead_end: Does this cell have exactly one neighbor?
    :type  is_dead_end: bool

    :param prev: Reference to previous Cell or None
    :param type: Cell or None
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

        # This doesn't come into play until the traversal stage
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

    :param matrix: Matrix representing the path/wall cells that compose the maze
    :type  matrix: list

    :param path: Representation of path cells
    :type  path: int

    :param wall: Representation of wall cells
    :type  wall: int

    :param cell_width: How wide the cells are (function of max # of digits it takes to represent highest numbered node)
    :type  cell_width: int

    :param pretty_path: Representation of the path obtained by running `self.diagram_path`
    :type  pretty_path: str
    """

    def __init__(self, maze_as_matrix, path, wall, cell_width=2):
        self.matrix = maze_as_matrix
        self.path = path
        self.wall = wall
        self.cell_width = cell_width
        self.adjlist = self.to_adjlist()

    def show_vertices(self, highlight_path=None):
        if not highlight_path:
            print(matrix2str(self.diagram_path(self.cell_width)))
        else:
            m = self.diagram_path(self.cell_width, highlight_cells=highlight_path)
            print(matrix2str(m))

    def as_ascii(self, highlight_cells=None):
        if not highlight_cells:
            highlight_cells = []

        new_rep = []
        for r_idx, row in enumerate(self.matrix):
            new_row = []
            for c_idx, col in enumerate(row):
                if col == self.wall:
                    new_row.append("#")
                elif col == self.path and (r_idx, c_idx) in highlight_cells:
                    new_row.append(t.red("*"))
                elif col == self.path:
                    new_row.append(" ")
                else:
                    raise ValueError(
                        "Matrices must be composed of only {self.path} and {self.wall}!"
                    )
            new_rep.append(new_row)
        print(matrix2str(new_rep))

    def count_path_nodes(self):
        """ Returns the total number of nodes that match `self.path` in self.matrix. """
        return sum([r.count(self.path) for r in self.matrix])

    def diagram_path(self, int_width=None, highlight_cells=None):
        """
        A graphic representation of the nodes.
        """
        if not highlight_cells:
            highlight_cells = []

        if not int_width:
            int_width = self.cell_width

        path = []
        for r_idx, row in enumerate(self.matrix):
            new_row = []
            for c_idx, col in enumerate(row):
                row_rep, col_rep = str(r_idx).zfill(2), str(c_idx).zfill(2)

                coords_rep = f"""({row_rep}, {col_rep})"""
                if col == self.path and ((r_idx, c_idx) in highlight_cells):
                    new_row.append(t.bold_red(coords_rep))
                elif col == self.path and (r_idx, c_idx) not in highlight_cells:
                    new_row.append(coords_rep)
                else:
                    new_row.append(" " * 8)

            path.append(new_row)
        return path

    def discover_cell(self, coords):
        """
        Given coords (row, col):
            if that cell is a path cell:
                return the coords (row, col)
            else:
                # it's out of bounds or not a path cell
                return False
        """
        width, height = len(self.matrix[0]), len(self.matrix)
        row, col = coords

        if any((row < 0, row > height - 1, col < 0, col > width - 1)):
            return False
        elif self.matrix[row][col] == self.path:
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
            self.discover_cell((row - 1, col)),  # North
            self.discover_cell((row + 1, col)),  # South
            self.discover_cell((row, col - 1)),  # East
            self.discover_cell((row, col + 1)),  # West
        )
        return [v for v in visited if isinstance(v, tuple)]

    def to_adjlist(self):
        """
        Creates an adjacency list from `self.matrix`.

        Returns adjacenct list as a dict where:
            key -> coords,
            val -> Cell objects (coords, found neighbors, etc.)

        # EXAMPLE #
        matrix = [
           [0, 1],
           [0, 1],
        ]

        simple = Maze(matrix)
        simple.to_adlist()

        # RESULTS #
        OrderedDict([
            ((0, 0), (Neighbors=[(1, 0)], Intersection=False, Dead End=True),
            ((1, 0), (Neighbors=[(0, 0)], Intersection=False, Dead End=True)
        ])

        In this example, either way you start the only way to finish is to go to the other.
        """
        cells = OrderedDict()

        for row_idx, row in enumerate(self.matrix):
            for col_idx, c in enumerate(row):
                coords = (row_idx, col_idx)
                if self.discover_cell(coords):
                    new_cell = Cell(coords, self.find_neighbors(coords))
                    cells.update({coords: new_cell})

        return cells

    def bfs(self, start_coords, goal_coords):
        """
        Explores the Adjancency List `self.adjlist` for a path from `start_coords` to `goal_coords`.

        If found, returns a reference to found Cell at `goal_coords`.
        Otherwise, returns False.
        """
        to_visit = deque()
        visited = set()

        root = self.adjlist[start_coords]
        root.traversal_mode = True

        to_visit.append(root)

        while to_visit:
            cell = to_visit.popleft()
            visited.add(cell)

            if cell.coords == goal_coords:
                return cell

            # Find adjacent edges that haven't been visited
            for coords in cell.neighbors:
                next_cell = self.adjlist[coords]
                if next_cell not in visited:
                    next_cell.prev = cell
                    next_cell.traversal_mode = True
                    to_visit.append(next_cell)

        return False

    def shortest_path(self, start_coords, goal_coords, root_to_leaf=True):
        cell_list = []

        found = self.bfs(start_coords, goal_coords)

        if not found:
            return "No path found!"

        cell_list.append(found.coords)

        while found.prev:
            found = found.prev
            cell_list.append(found.coords)

        if root_to_leaf:
            cell_list.reverse()

        return cell_list

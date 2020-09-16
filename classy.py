from collections import OrderedDict
from itertools import count


class Cell:
    '''
    A representation of a cell in the maze.

    :param coords: Coordinates
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
    '''
    def __init__(self, coords, neighbors=None):
        self.coords = coords
        if neighbors:
            self.neighbors = neighbors
        else:
            self.neighbors = []

        # Derived Attributes
        self.row, self.col = self.coords
        self.is_intersection = len(self.neighbors) > 2
        self.is_dead_end = len(self.neighbors) == 1

    def __repr__(self):
        return f"""(Neighbors={self.neighbors}, Intersection={self.is_intersection}, Dead End={self.is_dead_end}"""


def matrix2str(m):
    p = ""
    for row in m:
        p += " ".join(row) + "\n"
    return p


class Maze:
    '''
    Give me a matrix and I'll do some maze analysis. Sound good?
    '''
    def __init__(self, maze_as_matrix, path, wall, cell_width=2):
        self.matrix = maze_as_matrix
        self.path = path
        self.wall = wall
        self.cell_width = cell_width
        self.pretty_path = matrix2str(self.diagram_path(self.cell_width))

    def count_path_nodes(self):
        ''' Returns the total number of nodes that match `self.path` in self.matrix '''
        return sum([r.count(self.path) for r in self.matrix])

    def diagram_path(self, int_width=None):
        ''' 
        A graphic representation of the nodes. 
        Each is assigned an autoincremented id when it is discovered.

        >>> print(pretty_matrix(self.extract_path())     
        '''
        if not int_width:
            int_width = self.cell_width

        autoid = count(start=0, step=1)

        path = []
        for row in self.matrix:
            new_row = []
            for col in row:
                if col == self.path:
                    v = str(next(autoid)).zfill(int_width)
                else:
                    #   int_width == 1, v = " "
                    #   int_width == 2, v = "  "
                    #   int_width == 3, v = "   ", etc.
                    v = " "*int_width 
                new_row.append(v)

            path.append(new_row)
        return path

    def discover_cell(self, coords):
        '''
        Given coords (row, col):
            if that cell is a path cell:
                return the coords (row, col)
            else:
                # it's out of bounds or not a path cell
                return False
        '''
        width, height = len(self.matrix[0]), len(self.matrix)
        row, col = coords

        if any((row < 0, row > height-1, col < 0, col > width-1)):
            return False
        elif self.matrix[row][col] == self.path:
            return (row, col)
        else:
            return False

    def find_neighbors(self, coords):
        '''
        Given coords (row, col):
            check the neighbors to the N, S, E, W
            if they contain coords, return them
        '''
        row, col = coords

        visited = (
            self.discover_cell((row-1, col)),  # North
            self.discover_cell((row+1, col)),  # South
            self.discover_cell((row, col-1)),  # East
            self.discover_cell((row, col+1)),  # West
        )
        return [v for v in visited if isinstance(v, tuple)]

    def to_adjlist(self):
        ''' 
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
        '''
        cells = OrderedDict()

        for row_idx, row in enumerate(self.matrix):
            for col_idx, c in enumerate(row):
                coords = (row_idx, col_idx)
                if self.discover_cell(coords):
                    new_cell = Cell(
                        coords, 
                        self.find_neighbors(coords)
                    )
                    cells.update({coords : new_cell})

        return cells

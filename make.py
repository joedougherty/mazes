from random import randint


BLOCKED = '#' 
PASSAGE = ' '


class M:
    # https://stackoverflow.com/questions/29739751/implementing-a-randomly-generated-maze-using-prims-algorithm
    def __init__(self, height=10, width=10):

        r = [str(c) for c in BLOCKED*width]
        grid = []
        for _ in range(0, height):
            grid.append(r)
        self.grid = grid

        self.frontier_list = list()

    def random_cell(self):
        rand_row = randint(0, len(self.grid)-1)
        rand_col = randint(0, len(self.grid[0])-1)
        return {
            'coords': (rand_row, rand_col),
            'value': self.grid[rand_row][rand_col],
        }

    def set_to_passage(self, coords):
        row, col = coords
        self.grid[row][col] = PASSAGE

    def explore(self, coords, state):
        row, col = coords
        if any((
            row < 0,
            col < 0,
            row > len(self.grid),
            col > len(self.grid[0]),
        )):
            return False
        elif self.grid[row][col] == state:
            return (row, col)
        return False

    def _survey(self, coords, state):
        row, col = coords
        n = self.explore((row-2, col), state)
        s = self.explore((row+2, col), state)
        e = self.explore((row, col-2), state) 
        w = self.explore((row, col+2), state)
        return [d for d in (n,s,e,w) if d]
    
    def frontier_cells(self, coords):
        # All cells in distance 2 in state BLOCKED. 
        return self._survey(coords, BLOCKED)

    def neighbor_cells(self, coords):
        # All cells in distance 2 in state PASSAGE. 
        return self._survey(coords, PASSAGE)

    def random_frontier(self):
        return self.frontier_list[randint(0, len(self.frontier_list)-1)]

    def extract_middle_cell(self, start_coords, end_coords):
        in_order = sorted([start_coords, end_coords])
        start_row, start_col = in_order[0]
        end_row, end_col = in_order[1]

        if end_row > start_row:
            return (end_row-1, start_col)
        elif end_col > start_col:
            return (start_row, end_col-1)

    def go(self):
        rando = self.random_cell()
        self.set_to_passage(rando.get('coords'))
        self.frontier_list = self.frontier_cells(rando.get('coords'))

        while self.frontier_list:
            chosen = self.random_frontier()
            print(f'chosen: {chosen}')

            neighbors = self.neighbor_cells(chosen)
            print(f'neighbors: {neighbors}')

            random_neighbor = neighbors[randint(0, len(neighbors)-1)]
            print(f'random neighbor: {random_neighbor}')

            in_between = self.extract_middle_cell(chosen, random_neighbor)
            print(f'in_between: {in_between}')

            self.set_to_passage(in_between)

            new_frontier_cells = self.frontier_cells(chosen)
            print(f'new_frontier_cells: {new_frontier_cells}')
        
            for f in new_frontier_cells:
                self.frontier_list.append(f)

            self.frontier_list.remove(chosen)
            print(f'removed: {chosen}')
            print('---------------------------------------\n')

        return self.grid

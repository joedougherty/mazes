from collections import deque
from string import ascii_uppercase


matrix = [
    [0, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 0, 0],
    [1, 0, 0, 0, 1, 1, 1],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
]


class Node:
    def __init__(self, num_id, parent=None):
        self.num_id = num_id
        self.parent = parent
        # 0=A, 1=B, 2=C, ...
        self.letter = ascii_uppercase[self.num_id] 

    def __repr__(self):
        if self.parent:
            return f'''{self.parent} -> {self.letter}'''
        return f'''{self.letter}'''


def bfs(adj_matrix, start_node_id, goal_node_id):
    to_visit = deque()
    visited = set()

    to_visit.append(Node(start_node_id, parent=None))

    while to_visit:
        node = to_visit.popleft()
        visited.add(node)

        if node.num_id == goal_node_id:
            return node 

        # Find adjacent edges that haven't been visited
        for idx, val in enumerate(adj_matrix[node.num_id]):
            if val == 1 and idx not in visited:
                to_visit.append(Node(idx, parent=node))

    return "No path found!"

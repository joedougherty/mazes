-----------------
A Review of BFS
-----------------

`Wikipedia Pseudocode <https://en.wikipedia.org/wiki/Breadth-first_search#Pseudocode>`_:


.. code-block:: text 


	1  procedure BFS(G, root) is
	2      let Q be a queue
	3      label root as discovered	
	4      Q.enqueue(root)			                              
	5      while Q is not empty do
	6          v := Q.dequeue()
	7          if v is the goal then
	8              return v
	9          for all edges from v to w in G.adjacentEdges(v) do
	10             if w is not labeled as discovered then
	11                 label w as discovered
	12                 w.parent := v
	13                 Q.enqueue(w)


Breadth-first Search:


**A**. starts at the root node (lines 3,4)

**B**. discovers neighboring nodes (lines 9-13)

**C**. proceeds by visiting them and continuing this process until there are no new nodes left to discover and visit (line 5)



----------------------------
Looking at an Implementation
----------------------------


Here's some sample code to compare it to the pseudocode above!


.. code-block:: python

    # Source: $ROOT/functionalish.py
    def bfs(adjlist, start_coords, goal_coords):
        to_visit = deque()
        visited = set()

        root = adjlist[start_coords]
        root.traversal_mode = True

        to_visit.append(root)

        while to_visit:
            room = to_visit.popleft()
            visited.add(room)

            if room.coords == goal_coords:
                return room

            # Find adjacent edges that haven't been visited
            for coords in room.neighbors:
                next_room = adjlist[coords]
                if next_room not in visited:
                    next_room.prev = room
                    next_room.traversal_mode = True
                    to_visit.append(next_room)
        return False



---------
Resources
---------


https://www.dcode.fr/maze-generator


https://www.khanacademy.org/computing/computer-science/algorithms/graph-representation/a/describing-graphs


https://py.checkio.org/en/mission/open-labyrinth/share/574bd1ded68c9705c5d6f07c6206be12/


http://bryukh.com/labyrinth-algorithms/


Breadth-first search. (2020). Retrieved September 19, from https://en.wikipedia.org/wiki/Breadth-first_search. 


Skiena, S. (2008) *The Algorithm Design Manual* IBSN: 9781848000698


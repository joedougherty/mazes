---------------------------------------------------------
From an ASCII Maze to an Adjacency List
---------------------------------------------------------


.. code-block:: text

	######
	#    #
	# # ##
	######
    


How can we transform this string into an Adjacency List?


+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Step 1: Use an intermediate form: Maze as Nested List
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


.. code-block:: python
    
    tiny = '''
    ######
    #    #
    # # ##
    ######
    '''.strip()



Let's convert this ASCII maze, ``tiny``,  into a list of lists.  


.. code-block:: python

    def str2nested_list(s, delim='\n'):
        return [list(e) for e in s.split(delim)]


    tiny_nested_list = str2nested_list(tiny)
    

That was easy enough!

``tiny_nested_list``'s value now is:

.. code-block:: text

    [['#', '#', '#', '#', '#', '#'],
     ['#', ' ', ' ', ' ', ' ', '#'],
     ['#', ' ', '#', ' ', '#', '#'],
     ['#', '#', '#', '#', '#', '#']]


+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Step 2: Convert Maze as Nested List to an Adjacency List
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++


Taking a cue from `this article <http://bryukh.com/labyrinth-algorithms/>`_, the Adjacency List will be expressed as a dictionary. 

Here's the spec:

+ **key** -> coordinates of the room in the maze, expressed as a tuple ``(row, col)``.
+ **value** -> the ``Room`` instance of the current room. Each ``Room`` instance has a ``.neighbors`` attribute: a list of coordinates of neighboring cells that can be reached from this room.


.. code-block:: python


    # Source: src/functionalish.py
    PATH, WALL = ' ', '#'


    def find_neighbors(coords, nested_list):
        row, col = coords

        visited = (
            discover_room((row - 1, col), nested_list),  # North
            discover_room((row + 1, col), nested_list),  # South
            discover_room((row, col - 1), nested_list),  # East
            discover_room((row, col + 1), nested_list),  # West
        )
        return [v for v in visited if isinstance(v, tuple)]


    def discover_room(coords, nested_list):
        width, height = len(nested_list[0]), len(nested_list)
        row, col = coords

        if any((row < 0, row > height - 1, col < 0, col > width - 1)):
            return False
        elif nested_list[row][col] == PATH:
            return (row, col)
        else:
            return False


    def nested_list2adjlist(nested_list):
        adjlist = OrderedDict()

        for row_idx, row in enumerate(nested_list):
            for col_idx, c in enumerate(row):
                coords = (row_idx, col_idx)
                if discover_room(coords, nested_list):
                    new_room = Room(coords, find_neighbors(coords, nested_list))
                    adjlist.update({coords: new_room})
        return adjlist


Use the coords of the Room in question as the key. 

If that space has a room, it will provide the ``Room`` object, which will contain ``.neighbors``. 

Here is the resulting Adjacency List for the ``tiny`` labyrinth (with some additonal formatting for readability):

.. code-block:: python

    OrderedDict([
        ((1, 1), Neighbors=[(2, 1), (1, 2)], Intersection=False, Dead End=False),        # A 
        ((1, 2), Neighbors=[(1, 1), (1, 3)], Intersection=False, Dead End=False),        # B
        ((1, 3), Neighbors=[(2, 3), (1, 2), (1, 4)], Intersection=True, Dead End=False), # C
        ((1, 4), Neighbors=[(1, 3)], Intersection=False, Dead End=True),                 # D
        ((2, 1), Neighbors=[(1, 1)], Intersection=False, Dead End=True),                 # E
        ((2, 3), Neighbors=[(1, 3)], Intersection=False, Dead End=True)                  # F
    ])



Are you starting to see how we can traverse this data structure?


.. _bfs-review:

---------------------------------
A Review of Breadth-first Search
---------------------------------

`Wikipedia Pseudocode <https://en.wikipedia.org/wiki/Breadth-first_search#Pseudocode>`_:


.. code-block:: text 
  :linenos:

    procedure BFS(G, root) is
        let Q be a queue
        label root as discovered	
        Q.enqueue(root)			                              
        while Q is not empty do
            v := Q.dequeue()
            if v is the goal then
                return v
            for all edges from v to w in G.adjacentEdges(v) do
                if w is not labeled as discovered then
                    label w as discovered
                    w.parent := v
                    Q.enqueue(w)


Breadth-first Search:


**A**. starts at the root node (lines 3,4)

**B**. discovers neighboring nodes (lines 9-13)

**C**. proceeds by visiting them and continuing this process until there are no new nodes left to discover and visit (line 5)


.. _implementation:

---------------------------------------------------------------
Looking at an Implementation of BFS against an Adjacency List
---------------------------------------------------------------


Here's some sample code to compare it to the pseudocode above!


.. code-block:: python
   :linenos:

    # Source: src/functionalish.py
    def bfs(adjlist, start_coords, goal_coords):
        to_visit = deque()
        visited = set()

        root = adjlist[start_coords]

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
                    to_visit.append(next_room)
        return False


---------------------------------------------------
Side-by-Side comparison of Pseudocode to ``bfs()``
---------------------------------------------------

Some minor reformatting of the ``bfs()`` function helps to reveal significant similarity.


.. code-block:: text

    procedure BFS(G, root) is                                   |  def bfs(adjlist, start_coords, goal_coords):
        let Q be a queue                                        |      to_visit, visited = deque(), set()
        label root as discovered                                |      root = adjlist[start_coords]
        Q.enqueue(root)                                         |      to_visit.append(root)
                                                                |      
                                                                |      
        while Q is not empty do                                 |      while to_visit:
            v := Q.dequeue()                                    |          room = to_visit.popleft()
                                                                |          visited.add(room)
                                                                |
            if v is the goal then                               |          if room.coords == goal.coords:
                return v                                        |              return room 
                                                                | 
            for all edges from v to w in G.adjacentEdges(v) do  |          for coords in room.neighbors: 
                                                                |              next_room = adjlist[coords]
                if w is not labeled as discovered then          |              if next_room not in visited:  
                    label w as discovered                       |                  next_room.prev = room
                    w.parent := v                               |                  to_visit.append(next_room) 
                    Q.enqueue(w)                                |

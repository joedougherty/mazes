---------------------------------------------------------
From ASCII Maze to Adjacency List: A Series of Transforms
---------------------------------------------------------


.. code-block:: text

	######
	#    #
	# # ##
	######
    


How can transform this string into an Adjacency List?


+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Step 1: Use an intermediate form: Maze as Nested List
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


Let's convert the ASCII maze into a list of lists. Much nicer to work with.


.. code-block:: python

    def str2nested_list(s, delim='\n'):
        return [list(e) for e in s.split('\n')]


That was easy enough!


+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Step 2: Convert Maze as Nested List to an Adjacency List
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++


Taking a cue from `this article <http://bryukh.com/labyrinth-algorithms/>`_, the Adjacency List will be expressed as a dictionary. 

Here's the spec:

+ ``key`` -> coordinates of the room in the maze, expressed as a tuple (``row``, ``col``).
+ ``value`` -> the ``Room`` instance of the current room. Each ``Room`` instance has a ``.neighbors`` attribute: a list of coordinates of neighboring cells that can be reached from this room.


.. code-block:: python

    def nested_list2adjlist(nested_list):
        adjlist = OrderedDict()

        for row_idx, row in enumerate(nested_list):
            for col_idx, c in enumerate(row):
                coords = (row_idx, col_idx)
                if discover_room(coords, nested_list):
                    new_room = Room(coords, find_neighbors(coords, nested_list))
                    adjlist.update({coords: new_room})
        return adjlist

    # Helpers
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

        if any((row < 0, row > height - 1, col < 0, col > width - 1)): # bounds check
            return False
        elif nested_list[row][col] == PATH:
            return (row, col)
        else:
            return False


Use the coords of the Room in question as the key. If that space has a room, it will provide the ``Room`` object, which will contain ``.neighbors``. 

Are you starting to see how we can traverse this data structure?

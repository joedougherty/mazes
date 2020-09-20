.. _bfs-review:

-----------------
A Review of BFS
-----------------

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

    # Source: $ROOT/functionalish.py
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


-----------------------
Anatomy of a ``Room``
-----------------------

What's in an instance of a ``Room`` object, anyway?

+ ``.coords``: Its address as a tuple (``row``, ``col``).
+ ``.neighbors``: A list of the *coordinates* of neighbors to the immediate North, East, West, or South. (No diagonal travel).


Setting ``.prev`` during traversal lets us back-track top find the shortest path from the Room we are seeking back to the start.

+ ``.prev``: Reference to prev ``Room``
+ ``.traversal_mode``: This flag controls the string representation of a ``Room`` instance. 

This may sounds strange. Why would we want tha? It can be helpful to know different aspects of the ``Room`` at different times, in different contexts. This somewhat unorthodox approach lets us change how a ``Room`` is ``print()``-ed. This will be of use later.

When a ``Maze`` is instantiated, the ``Rooms`` that it is composed of have ``.traversal_mode`` set to ``False``. It is only when we start looking for paths that this flag is set to ``True``.

There are also some derived attributes. The existence of a derived attribute on this class does *not* imply its usage or existence outside the scope of the object in its lifetime. That's right, there may be attributes that simply don't have a purpose yet.

+ ``.row``: The row part of the coord.
+ ``.col``: The col part of the coord.
+ ``.is_intersection``: Does this room have more than 2 neighbors?
+ ``.is_dead_end``: Is there only one way in / out of this room?

-------------------
Pathfinding
-------------------


This ``bfs()`` function returns a reference to the found room (if, you know, it's found). 


How can we use this to find a path back to the start?


+++++++++++++++++
``Room.prev``
+++++++++++++++++



Take notice of line 12 of the code sample in :ref:`bfs-review`. The same functionality appears on line 21 of :ref:`implementation`. 

Prior to adding new room to the ``to_visit`` queue, we note down that ``Room`` coordinates we're in now. This way, we can walk back up the ``Room.prev`` recursively until we get to a ``Room`` where ``.prev is None``.



+++++++++++++++++++
``shortest_path()``
+++++++++++++++++++


Passing the final ``Room`` to shortest path will the shortest way back to the start. It traverses the implicit linked list, pushing a reference to each item onto the return list. 


.. code-block:: python

    def shortest_path(adjlist, start_coords, goal_coords, root_to_leaf=True):
        path = []

        found = bfs(adjlist, start_coords, goal_coords)

        if not found:
            print("No path found!")
            return False

        path.append(found.coords)

        while found.prev:
            found = found.prev
            path.append(found.coords)

        if root_to_leaf:
            path.reverse()

        return path



+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
A Brief Diversion: printing a linked list with recursive ``__repr__`` 
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Here is a simplified example to demonstrate the principle. 

.. code-block:: python
 :linenos:

    class Node:
        def __init__(self, val, parent=None):
            self.val = val 
            self.parent = parent

        def __repr__(self):
            if self.parent:
                # Here's the (implict) recursive call!
                return f'''{self.parent} <- {self.val}'''
            else:
                return f'''{self.val}'''



.. code-block:: python
 :linenos:

    zero = Node(0, parent=None)
    one  = Node(1, parent=zero)
    two  = node(2, parent=one)

    print(two) # '''0 <- 1 <- 2'''


-------------------
Visualization
-------------------

++++++++++++++++
``.as_ascii()``
++++++++++++++++


.. code-block:: text

    >>> tiny.as_ascii()

    ######
    #    #
    # # ##
    ######




+++++++++++++++++++++
``.show_vertices()``
+++++++++++++++++++++

.. code-block:: text

    >>> tiny.show_vertices()

    (01, 01)(01, 02)(01, 03)(01, 04)
    (02, 01)        (02, 03)


Shows the relationships between the rooms, using coords as an identifier.

---------
Resources
---------


https://www.dcode.fr/maze-generator


https://www.khanacademy.org/computing/computer-science/algorithms/graph-representation/a/describing-graphs


https://py.checkio.org/en/mission/open-labyrinth/share/574bd1ded68c9705c5d6f07c6206be12/


http://bryukh.com/labyrinth-algorithms/


https://stackoverflow.com/questions/1984162/purpose-of-pythons-repro


Breadth-first search. (2020). Retrieved September 19, from https://en.wikipedia.org/wiki/Breadth-first_search. 


Skiena, S. (2008) *The Algorithm Design Manual* IBSN: 9781848000698


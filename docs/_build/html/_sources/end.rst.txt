-----------------------
Anatomy of a ``Room``
-----------------------

What's in an instance of a ``Room`` object, anyway?

+ ``.coords``: Its address as a tuple ``(row, col)``.
+ ``.neighbors``: A list of the *coordinates* of neighbors to the immediate North, East, West, or South. (No diagonal travel).


There are also some derived attributes. The existence of a derived attribute on this class does *not* imply its usage or existence outside the scope of the object in its lifetime. That's right, there may be attributes that simply don't have a purpose yet.


+ ``.row``: The row part of the coord.
+ ``.col``: The col part of the coord.
+ ``.is_intersection``: Does this room have more than 2 neighbors?
+ ``.is_dead_end``: Is there only one way in / out of this room?

Last, but not least, are attributes that are used during the traversal (pathfinding) stage.

+ ``.prev``: Reference to prev ``Room``
+ ``.traversal_mode``: This flag controls the string representation of a ``Room`` instance. 


"*This flag controls the string representation of a Room instance."* 

This may sound strange. Why would we want that? 

It can be helpful to know different aspects of the ``Room`` at different times, in different contexts. This somewhat unorthodox approach lets us change how a ``Room`` is ``print()``-ed based on the context we are in.

When a ``Maze`` is instantiated, the ``Room`` instances that it is composed of will have ``.traversal_mode`` set to ``False``. It is only when we start looking for paths that this flag is set to ``True``.

Here's the implementation:


.. code-block:: python

    class Room:
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



-------------------
The ``Maze`` class
-------------------

We have primarily looked at how we can approach this problem with a few functions.

There is also a full ``Maze`` class that encapsulates this functionality.

Let's look at a few select methods:



.. NOTE::
    The implementation of the ``Maze`` class can be found in ``src/classymaze.py``.


++++++++++++++
Visualization
++++++++++++++


``.as_ascii()``
----------------


.. code-block:: text

    >>> tiny.as_ascii()
    ######
    #    #
    # # ##
    ######




``.show_vertices()``
-----------------------

.. code-block:: text

    >>> tiny.show_vertices()
    (01, 01)(01, 02)(01, 03)(01, 04)
    (02, 01)        (02, 03)


(This method helps show the position of rooms using coords as an identifier.)


+++++++++++++++++++++++++
Searching and Pathfinding
+++++++++++++++++++++++++

.. _rec-print-example:

``.bfs()``
------------

Uses breadth-first search to determine whether or not there is a path between a given start room ``(start_row, start_col)`` and a given goal room ``(goal_row, goal_col)``.

If a path exists, it returns a reference to the ``Room`` instance at ``(goal_row, goal_col)``. 

Otherwise, this returns ``False``.


.. code-block:: text
    
    tiny = '''
    ######
    #    #
    # # ##
    ######
    '''.strip()


    tinymaze = Maze(tiny)

    '''
    Try to keep something like this in mind...

    ######
    #ABCD#
    #E#F##
    ######
    ''''

    # Look for a path from "A" to "F"
    goal = tinymaze.bfs((1,1),(2,3))

    if goal:
        print(goal)
        
    # ``goal`` now has this nice str rep which shows us the path back...

    """(1, 1) -> (1, 2) -> (1, 3) -> (2, 3)"""


Yes, we can get there from here!



``.shortest_path()``
----------------------

A list of ``Room`` coordinates that describe the path from ``(start_row, start_col)`` to ``(goal_row, goal_col)`` (including both).

If no path is found, returns ``False``.

This method makes concrete what is implicit above in ``.bfs()``.


+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
An Aside: printing a linked list with recursive ``__repr__`` 
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

You may have noticed in :ref:`rec-print-example` that we were able to print the full path back to the start room using only a reference to the end ``Room``. What's going on here?

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



The `__repr__ magic method <https://docs.python.org/3/reference/datamodel.html#object.__repr__>`_ controls the "official" string representation of an object. 

We can use implicit recursive calls to ``__repr__`` to print the whole path.


When we ``print()``  a ``Node`` who has a ``parent``, we print the parent instance as well. 

This pushes onto the stack until we get to the root ``Node``, at which point the stack unwinds and prints the path back.

---------
Resources
---------


https://www.dcode.fr/maze-generator


https://www.khanacademy.org/computing/computer-science/algorithms/graph-representation/a/describing-graphs


https://py.checkio.org/en/mission/open-labyrinth/share/574bd1ded68c9705c5d6f07c6206be12/


http://bryukh.com/labyrinth-algorithms/


https://stackoverflow.com/questions/1984162/purpose-of-pythons-repro


https://docs.python.org/3/reference/datamodel.html#object.__repr__

Breadth-first search. (2020). Retrieved September 19, from https://en.wikipedia.org/wiki/Breadth-first_search. 


Skiena, S. (2008) *The Algorithm Design Manual* IBSN: 9781848000698


-----------------------
Defining Our Terms
-----------------------

Before we dive in, let's get some definitions squared away.


++++++++
**Maze**
++++++++

In this context, a **Maze** is an two-dimensional area containing *at least two* connected **Rooms** that one must find a path through.

++++++++
**Room**
++++++++


+ A **Room** can have neighbors to the North, West, East, and South. 

+ Each **Room** has a max of four immediately adjacent neighbors.

+ A **Room** must have at least one neighbor (at least, if you ever hope to get to it). 

++++++++++
**Path**
++++++++++

A list containing the coordinates of **Rooms** from the start to the end (ordering by convention).

As a consequence, we don't worry about diagonal movement on the grid. 


----------------------------------------------
Lil' Labyrinth: Methods of Maze Representation 
----------------------------------------------


Here is a small ASCII representation of a 2D labyrinth. 

.. code-block:: text

	######
	#    #
	# # ##
	######
    


+ The octothorpe character (``#``) represents a wall
+ The space character (``' '``) represents a room

The wall blocks define our boundaries and thus determine which direction(s) we may travel.

.. NOTE::
    We will not concern ourselves with diagonal travel. The only directions one can travel from a Room are North, East, West, and South.  


Assigning each room a unique identifier helps to clarify the relationships.


.. code-block:: text

	######
	#ABCD#
	#E#F##
	######


++++++++++++++++++++++++++++++++++++++++++++++
Network Diagram
++++++++++++++++++++++++++++++++++++++++++++++


Drawing this particular example as a network diagram does not reveal much we could not have seen in its previous form.


Definition
----------

An *N* node diagram that describes the maze in terms of network connections. 


Example
-------

.. code-block:: text 

    A---B---C---D
    |       |
    E       F


+ ``A``'s neighbor(s): ``B``, ``E``
+ ``B``'s neighbor(s): ``A``, ``C``
+ ``C``'s neighbor(s): ``B``, ``F``, ``D``
+ ``D``'s neighbor(s): ``C``
+ ``E``'s neighbor(s): ``A``
+ ``F``'s neighbor(s): ``C``


This is largely a conceptual representation. There is no example object as it does not require implementation.


++++++++++++++++++++++++++++++++++++++++++++++++
Adjacency Matrix
++++++++++++++++++++++++++++++++++++++++++++++++

Definition
----------


An *N* x *N* matrix where each cell contains either ``0`` or ``1``. *N* = the number of nodes in the graph.


+ ``0``: There is no connection between the two nodes given by ``row``, ``col``.
+ ``1``: There is a connection between the two nodes given by ``row``, ``col``.

Example
-------

As in the network diagram example above, we can see there's a connection between ``A`` and ``E``.

To check the Adjacency Matrix, we look in one of the two cells that represent that connection.

.. code-block:: python
    
    adjmatrix = [
        #A, B, C, D, E, F
        [0, 1, 0, 0, 1, 0], # A
        [1, 0, 1, 0, 0, 0], # B
        [0, 1, 0, 1, 0, 1], # C
        [0, 0, 1, 0, 0, 0], # D
        [1, 0, 0, 0, 0, 0], # E
        [0, 0, 1, 0, 0, 0], # F
    ]


The cells ``adj_matrix[0][4]`` and ``adj_matrix[4][0]`` both contain ``1`` -- the cells are connected!

.. ATTENTION::

    Note that this representation repeats information. Each (possible) node connection is specified twice.


Ajdacency Matrices make it fast and easy to determine if nodes are *self-referential*. Look down the diagonal from the upper-left corner of the matrix down the lower-right corner. Notice that all the values are ``0``. This means that no nodes intersect with themselves. In other words, each node only connects to other nodes.



++++++++++++++++++++++++++++++++++++++++++++++
Adjacency List
++++++++++++++++++++++++++++++++++++++++++++++

Definition
----------

A list of length *N* where *N* = the number of nodes in the graph.

Each member of the list is a list containing references to its neighbors.


Example
-------


.. code-block:: python
    
    adjlist = [
        [1,4],      # A :: Neighbors: [B, E]
        [0,2],      # B :: Neighbors: [A, C]
        [1,3,5],    # C :: Neighbors: [B, D, F]
        [2]         # D :: Neighbors: [C]
        [0],        # E :: Neighbors: [A]
        [2],        # F :: Neighbors: [C]
    ]


.. ATTENTION::

    Note that this representation potentially makes it less efficient to check if two *arbitrary* nodes are connected.



++++++++++++++++++
Choosing a Method
++++++++++++++++++

Skiena compares adjacency lists and adjacency matrices on p. 152 of *The Algorithm Design Manual* (2008).

While adjacency matrices make it faster to test if two nodes are immediate neighbors and also support fast edge insertion and deletion, adjacency lists offer better traversal speed and less memory usage on average.

"*Take-Home Lesson:* Adjacency lists are the right data structure for most applications of graphs." (Skiena) 




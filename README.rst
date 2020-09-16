-----------------
Let's Review BFS
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

-------------------------------
Some Possible Representations
-------------------------------


Representation of a graph as a Tree
-----------------------------------

.. code-block:: text 

        A
       / \
      B   C
     / \ 
    D   E 
    

Representation of a graph as an Adjacency Matrix
------------------------------------------------

An *N* x *N* matrix where each cell contains either ``0`` or ``1``. *N* = the number of nodes in the graph.


+ ``0``: There is no connection between the two nodes given by ``row``, ``col``.
+ ``1``: There is a connection between the two nodes given by ``row``, ``col``.

+++++++++++++++++++++++++
Adjacency Matrix Example
+++++++++++++++++++++++++

As in the tree above, we can see there's a connection between ``A`` and ``C``.

To check the Adjancency Matrix, we look in one of the two cells that represent that connection.

.. code-block:: python
    
    adj_matrix = [
        #A, B, C, D, E
        [0, 1, 1, 0, 0], # A
        [1, 0, 0, 1, 1], # B
        [1, 0, 0, 0, 0], # C
        [0, 1, 0, 0, 0], # D
        [0, 1, 0, 0, 0], # E
    ]


The cells ``adj_matrix[0][2]`` and ``adj_matrix[2][0]`` both contain ``1`` -- the cells are connected!

.. ATTENTION::

    Note that this representation repeats information. Each (possible) node connection is specified twice.


Representation of a graph as an Adjacency List
----------------------------------------------

A list of length *N* where *N* = the number of nodes in the graph.

Each member of the list is a list containing references to its neighbors.

+++++++++++++++++++++++++
Adjacency Matrix Example
+++++++++++++++++++++++++


.. code-block:: python
    
    adj_list = [
        [1,2],   # A :: Neighbors: [B,C]
        [3,4],   # B :: Neighbors: [D,E]
        [0],     # C :: Neighbors: [A]
        [1],     # D :: Neighbors: [B]
        [1],     # E :: Neighbors: [B]
    ]


All three of these representations describe the same object.

---------
Resources
---------


https://www.dcode.fr/maze-generator


https://www.khanacademy.org/computing/computer-science/algorithms/graph-representation/a/describing-graphs


https://py.checkio.org/en/mission/open-labyrinth/share/574bd1ded68c9705c5d6f07c6206be12/

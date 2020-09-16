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

.. code-block:: python
    
    adj_matrix = [
        #A, B, C, D, E
        [0, 1, 1, 0, 0], # A
        [1, 0, 0, 1, 1], # B
        [1, 0, 0, 0, 0], # C
        [0, 1, 0, 0, 0], # D
        [0, 1, 0, 0, 0], # E
    ]


Representation of a graph as an Adjacency List
----------------------------------------------

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

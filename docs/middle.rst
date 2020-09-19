---------------------------------------------------------
From ASCII Maze to Adjacency List: A Series of Transforms
---------------------------------------------------------


.. code-block:: text

	######
	#    #
	# # ##
	######
    


How can transform what we have into a form that allows easy querying?


++++++++++++++++++++++++++++++++++++++++++++++++
An intermediate form: The *Maze as Nested List*
++++++++++++++++++++++++++++++++++++++++++++++++


Let's convert the ASCII maze to a list of lists.


.. code-block:: python

    def str2nested_list(s, delim='\n'):
        return [list(e) for e in maze_str.split('\n')]



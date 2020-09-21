class Node:
    def __init__(self, val, parent=None):
        self.val = val
        self.parent = parent

    def __repr__(self):
        # dig the recursion
        if self.parent and not isinstance(self.parent, Node):
            raise TypeError("parent= must be of type Node!")

        if self.parent:
            return f"""{self.parent} <- {self.val}"""
        else:
            return f"""{self.val}"""


# Oh boy! A linked list!
zero = Node(0, parent=None)
one = Node(1, parent=zero)
two = Node(2, parent=one)
three = Node(3, parent=two)
four = Node(4, parent=three)


print(zero)  # '0'
print(one)  # '0 <- 1'
print(two)  # '0 <- 1 <- 2'
print(three)  # '0 <- 1 <- 2 <- 3'
print(four)  # '0 <- 1 <- 2 <- 3 <- 4'

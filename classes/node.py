"""
PURPOSE
Node with no limit on number of children. Used to make a non binary tree.
"""

class Node:
    """
    PURPOSE
    A node in a tree. To be used in a non binary tree.
    """

    def __init__(self, split_criterion):
        self.name = split_criterion
        self.children = []

    def new_child(self, new_node):
        """
        PURPOSE
        Insert a new child node to this node.

        INPUT
        new_node: Node detailing the child

        OUTPUT
        None
        """
        self.children.append(new_node)

    def print_children(self):
        """
        PURPOSE
        Print names of children.

        INPUT
        None

        OUTPUT
        None
        """
        for child in self.children:
            print(child.name)
    
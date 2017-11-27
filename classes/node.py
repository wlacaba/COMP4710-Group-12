"""
PURPOSE
Node with no limit on number of children. Used to make a non binary tree.
"""

class Node:
    """
    PURPOSE
    A node in a tree. To be used in a non binary tree.

    INPUT
    label: name of the attribute we want to split by on this node, or label
           of leaf node
    """

    def __init__(self, label):
        self.label = label
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

    def print_label(self):
        """
        PURPOSE
        Print label of this node

        INPUT
        None

        OUTPUT
        None
        """
        print (self.label)

    def update_node_label(self, new_label):
        """
        PURPOSE
        Update the name of the label

        INPUT
        new_label: new name of label

        OUTPUT
        None
        """
        self.label = new_label

    
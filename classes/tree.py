"""
PURPOSE
Hold the tree root and the list of rules

AUTHOR
Warren Lacaba
"""

class Tree:

    def __init__(self, tree_root):
        self.root = tree_root
        self.rules = []

    def insert_rules(self):
        self.read_in_rules(self.root, '')

    def read_in_rules(self, node, parent):
        branch_length = len(node.branches)
        curr = parent + "," + node.label + ","
        
        if branch_length != 0:
            for i in range(0, branch_length):
                rule_part = curr + node.branches[i]
                self.read_in_rules(node.children[i], rule_part)
        else:
            #There's ',' on each side of the string
            #so it's giving spaces on either end of the list
            curr = curr[1:-1]
            self.rules.append(curr.split(','))


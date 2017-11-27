"""
Build the ID3 decision tree here.
"""
import os
import sys
from collections import Counter

#Gotta add the name of your current directory's parent directory to path
#Imports weren't working before I added this
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes.dataset import Dataset
from classes.node import Node

#HELPERS----------------------------------------------------------------------

def init_dataset(database_name):
    """
    Blah
    """
    newdata = Dataset()
    newdata.get_data(database_name)

    return newdata

#MAIN-------------------------------------------------------------------------

def id3_tree(learn_set, attribute_set):
    """
    PURPOSE
    Implementation of decision tree algorithm.

    INPUT
    learn_set: subset of data to train the algorithm and build tree
    attribute_set: set of all possible attributes to judge by

    OUTPUT
    current_node: root node of the decision tree
    """
    #Create a node, label and attach to tree later
    curr_node = Node('Empty')

    #If attribute set is empty
    attribute_set_length = len(attribute_set)

    #Check if all revenue values are the same by comparing all of them
    #with the first one. If all the same, algorithm terminates.
    revenue_class = learn_set[0]['revenue']
    revenue_all_same = True
    list_revenues = []
    
    for movie in learn_set:
        curr_revenue = movie['revenue']
        list_revenues.append(curr_revenue)

        if revenue_class != curr_revenue:
            revenue_all_same = False

    if revenue_all_same:
        #Label node with the attribute
        curr_node.update_node_label(revenue_class)
    elif attribute_set_length == 0:
        #Majority vote on the class
        #Label node with the class
        revenue_counter = Counter(list_revenues)
        revenue_majority = revenue_counter.most_common(1)
        curr_node.update_node_label(revenue_majority[0][0])
    else:
        #Continue algorithm
        print('Algorithm continues')

def run_id3(database_name):
    """
    Run
    """
    mydata = init_dataset(database_name)
    id3_tree(mydata.learn_set, mydata.attribute_set)

run_id3('../data/new_database2.csv')

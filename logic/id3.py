"""
Build the ID3 decision tree here.
"""
import os
import sys
import math
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

def find_information_gain(learn_set, attribute_set):
    """
    Let D be the learning set.
    Let m be the number of distinct values for attribute. 
    Let Cid be the set of tuples of class Ci in D. 
    Let |D| and |Cid| be the size of each. 

    apply Attribute selection method(D, attribute list) to find the “best” splitting criterion;
(7) label node N with splitting criterion;
(8) if splitting attribute is discrete-valued and multiway splits allowed then // not restricted to binary trees
(9) attribute list = attribute list - splitting attribute; // remove splitting attribute
(10) for each outcome j of splitting criterion // partition the tuples and grow subtrees for each partition
(11)    let Dj be the set of data tuples in D satisfying outcome j; // a partition
(12)        if Dj is empty then
(13)            attach a leaf labeled with the majority class in D to node N;
(14)        else attach the node returned by Generate decision tree(Dj , attribute list) to node N;
    endfor
(15) return N;
    """

    info_gain = 0
    best_attribute = 'Empty'
    info_of_class = calculate_entropy(learn_set, 'revenue')

    for attribute in attribute_set:
        info_of_attribute = 0 #Amount needed to store info based on attribute, calculate info(attribute)
        new_info_gain = info_of_class - info_of_attribute

        if new_info_gain > info_gain:
            info_gain = new_info_gain
            best_attribute = attribute

    return best_attribute

def calculate_entropy(learn_set, target_attribute):
    """
    PURPOSE
    Calculate entropy for target_attribute. 

    INPUT
    learn_set: list of movies used to train the tree
    target_attribute: what we're trying to classify by, in this case, revenue

    OUTPUT
    entropy: the total value of entropy

    NOTES
    Entropy is calculated by the formula:

    Let C be the count of revenue class in learn set.
    Let D be the total size of learn set.

    -Sum((C/D) * log2(C/D))
    """
    total_size = len(learn_set)
    list_target = []

    for movie in learn_set:
        list_target.append(movie[target_attribute])

    counter = Counter(list_target)
    common = counter.most_common()
    entropy = 0

    for label in common:
        count_label = label[1]
        portion = count_label/total_size
        entropy += -((portion)*math.log2(portion))

    print(str(entropy))
    return entropy



def run_id3(database_name):
    """
    Run
    """
    mydata = init_dataset(database_name)
    calculate_entropy(mydata.learn_set, 'revenue')
    #id3_tree(mydata.learn_set, mydata.attribute_set)

run_id3('../data/new_database2.csv') #just testing stuff

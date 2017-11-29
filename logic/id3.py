"""
Build the ID3 decision tree here.
"""
import os
import sys
import math
from operator import itemgetter
from itertools import groupby
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
    PURPOSE
    Calculate the information gain of each attribute. A higher gain in
    information will give us the best attribute to split a node by. 

    INPUT
    learn_set: a list of movies to train the algorithm
    attribute_set: a set of the attributes we want to split by

    OUTPUT
    best_attribute: the name of the best attribute to split by
    """

    info_gain = 0
    best_attribute = 'Empty'
    info_of_class = calculate_entropy(learn_set, 'revenue')

    for attribute in attribute_set:
        info_of_attribute = calculate_info(learn_set, attribute, 'revenue')
        new_info_gain = info_of_class - info_of_attribute
        print(attribute + " " + str(new_info_gain))
        if new_info_gain > info_gain:
            info_gain = new_info_gain
            best_attribute = attribute

    print(best_attribute)
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
        entropy -= ((portion)*math.log2(portion))

    return entropy

def calculate_info(learn_set, attribute, target_attribute):
    """
    PURPOSE
    Calculate how much more info needed to get a classification. 

    INPUT
    learn_set: the list of movies used to train the algorithm
    attribute: possible attribute we want to split on
    target_attribute: attribute we want to classify on, revenue

    OUTPUT
    info: amount of info needed to get a classification

    NOTES

    Given by formula:

    Sum((count of attribute's value/total size) * entropy(partition of just that attribute value))
    """
    info = 0
    keys = []
    groups = []
    total_size = len(learn_set)

    #Sort so we can use groupby to find partitions on attribute
    learn_set = sorted(learn_set, key=itemgetter(attribute))

    for group in groupby(learn_set, itemgetter(attribute)):
        keys.append(group[0])
        groups.append(list(group[1]))

    for g in groups:
        count = len(g)
        portion = count/total_size
        info += portion * calculate_entropy(g, target_attribute)

    return info

def run_id3(database_name):
    """
    Run
    """
    mydata = init_dataset(database_name)
    gain = find_information_gain(mydata.learn_set, mydata.attribute_set)
    #calculate_info(mydata.learn_set, 'prod_budget', 'revenue')
    #calculate_entropy(mydata.learn_set, 'revenue')
    #id3_tree(mydata.learn_set, mydata.attribute_set)

run_id3('../data/new_database2.csv') #just testing stuff

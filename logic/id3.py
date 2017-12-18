"""
PURPOSE
Build the ID3 decision tree here.

AUTHOR
Warren Lacaba
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
from classes.tree import Tree

TARGET = 'revenue'
#HELPERS----------------------------------------------------------------------

def init_dataset(database_name):
    """
    PURPOSE
    Read in dataset. Set up the test and learn sets. 

    INPUT
    database_name: name (and path) of database

    OUTPUT
    newdata: dataset object
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

    #Need shallow copy of attribute_set, or else we won't actually
    #find all possible rules
    attributes = attribute_set.copy()
    attribute_set_length = len(attributes)

    #Check if all revenue values are the same by comparing all of them
    #with the first one. If all the same, algorithm terminates.
    revenue_class = learn_set[0][TARGET]
    revenue_all_same = True
    list_revenues = []
    
    for movie in learn_set:
        curr_revenue = movie[TARGET]
        list_revenues.append(curr_revenue)

        if revenue_class != curr_revenue:
            revenue_all_same = False

    if revenue_all_same:
        #Label node with the revenue class
        curr_node.update_node_label(revenue_class)
    elif attribute_set_length == 0:
        #Majority vote on the class, label node with that class
        revenue_counter = Counter(list_revenues)
        revenue_majority = revenue_counter.most_common(1)
        curr_node.update_node_label(revenue_majority[0][0])
    else:
        attribute_name = find_information_gain(learn_set, attributes)
        attributes.discard(attribute_name)

        #Group everything by attribute class
        groups = []
        keys = []
        learn_set = sorted(learn_set, key=itemgetter(attribute_name))

        for group in groupby(learn_set, itemgetter(attribute_name)):
            keys.append(group[0])
            groups.append(list(group[1]))

        curr_node.update_node_label(attribute_name)

        #For each possible attribute class
        for i in range(0, len(keys)):
            partition_size = len(groups[i])

            if partition_size == 0:
                #Attach a leaf labeled with majority class in D to curr_node
                majority_counter = Counter(list_revenues)
                common_rev = majority_counter.most_common(1)
                curr_node.update_node_label(common_rev[0][0])
            else:
                #Recursively call on partitioned learn_set
                curr_node.new_branch(keys[i])
                curr_node.new_child(id3_tree(groups[i], attributes))
    
    return curr_node

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
    best_attribute = ''
    info_of_class = calculate_entropy(learn_set, TARGET)

    for attribute in attribute_set:
        info_of_attribute = calculate_info(learn_set, attribute, TARGET)
        new_info_gain = info_of_class - info_of_attribute
        
        if new_info_gain >= info_gain:
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

def run_id3(database_name, num_trials):
    """
    Loop num_trials times, building a new tree and testing it against the
    test set of movies.
    """
    total = 0

    for x in range(0, num_trials):
        mydata = init_dataset(database_name)
        decision_tree = Tree(id3_tree(mydata.learn_set, mydata.attribute_set))
        decision_tree.insert_rules()

        num_correct = 0

        for movie in mydata.test_set:
            for rule in decision_tree.rules:

                conditions_met = True
                key = ''
                value = ''
                for i in range(0, len(rule) - 1, 2):
                    #Even index = attribute, odd index = class label
                    key = rule[i]
                    value = rule[i + 1]

                    #Check if value is correct
                    if movie[key] != value:
                        conditions_met = False
                        break;
                
                if conditions_met:
                    if rule[-1] == movie[TARGET]:
                        num_correct += 1
                        #End for if we find a rule that correctly classifies movie
                        break;

        total += (num_correct/len(mydata.test_set)) * 100
        
        print("Test #" + str(x) + ", accuracy = " + 
              str((num_correct/len(mydata.test_set)*100)))

    total /= num_trials
    print("Average over " + str(num_trials) + " trials: " + str(total) + "%")

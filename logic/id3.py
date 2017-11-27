"""
Build the ID3 decision tree here.
"""
import os
import sys

#Gotta add the name of your current directory's parent directory to path
#Imports weren't working before I added this
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes import dataset
from classes import node

def init_dataset(database_name):
    """
    Blah
    """
    newdata = dataset.Dataset()
    newdata.get_data(database_name)

    return newdata

def id3_tree(learn_set, attribute_list):
    """
    ID3 Decision Tree Algorithm
    """
    attribute_list_length = len(attribute_list)
    revenue_class = learn_set[0][3]
    compare_revenue = revenue_class
    all_same = True
    
    for movie in learn_set:
        compare_revenue = movie[3]

        if int(revenue_class) != int(compare_revenue):
            all_same = False

    if all_same:
        #Label node with the attribute
        print('All same')
    elif attribute_list_length == 0:
        #Majority vote on the class
        #Label node with the class
        print('Attribute list empty')
    else:
        #Continue algorithm
        print('Algorithm continues')

def run_id3(database_name):
    """
    Run
    """
    mydata = init_dataset(database_name)
    id3_tree(mydata.learn_set, mydata.attribute_list)

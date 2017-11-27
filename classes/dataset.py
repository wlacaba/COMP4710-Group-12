"""
PURPOSE
Used to store all tuples of (label: value) from the database.
"""

import csv
import random

class Dataset:
    """
    PURPOSE
    See above.
    """

    def __init__(self):
        self.name = "MOVIES"
        self.learn_set = []
        self.test_set = []
        self.attribute_list = []

    def get_data(self, database_name):
        """
        PURPOSE
        Read in the whole database file, split into a learn set and
        test set, add labels for attribute list.

        INPUT
        database_name: name of database, path and everything

        OUTPUT
        None
        """

        read = open(database_name, 'r', encoding='utf-8')
        reader = csv.DictReader(read)

        self.attribute_list = reader.fieldnames

        for row in reader:
            movie_tuple = (row['title'],
                           row['revenue'],
                           row['release'],
                           row['prod_budget'],
                           row['genre'],
                           row['company'])

            coin_toss = random.randint(0, 1)

            if coin_toss == 0:
                self.learn_set.append(movie_tuple)
            elif coin_toss == 1:
                self.test_set.append(movie_tuple)

        

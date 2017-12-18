"""
PURPOSE
Used to store all tuples of (label: value) from the database.

AUTHOR
Warren Lacaba
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
        self.attribute_set = set()

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

        """
        Remove these because you don't want them as splitting attributes.
        I only included title in the database just in case we need it for
        the written report (or for printing), and revenue is the class we 
        want to classify by.
        """
        self.attribute_set = set(reader.fieldnames)
        self.attribute_set.discard('title')
        self.attribute_set.discard('revenue')

        for row in reader:
            movie_dict = { 'revenue': 'rv' + row['revenue'],
                           'release': 're' + row['release'],
                           'prod_budget': 'b' + row['prod_budget'],
                           'genre': row['genre'],
                           'company': row['company']}

            coin_toss = random.randint(0, 1)

            if coin_toss == 0:
                self.learn_set.append(movie_dict)
            elif coin_toss == 1:
                self.test_set.append(movie_dict)

        

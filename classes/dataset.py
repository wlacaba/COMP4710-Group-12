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

        self.attribute_set = set(reader.fieldnames)

        for row in reader:
            movie_dict = { 'title': row['title'],
                           'revenue': row['revenue'],
                           'release': row['release'],
                           'prod_budget': row['prod_budget'],
                           'genre': row['genre'],
                           'company': row['company']}

            coin_toss = random.randint(0, 1)

            if coin_toss == 0:
                self.learn_set.append(movie_dict)
            elif coin_toss == 1:
                self.test_set.append(movie_dict)

        

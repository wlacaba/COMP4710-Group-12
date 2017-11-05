"""
Purpose: To clean the csv database.
"""

import csv

def correct_inflation():
    """
    Used to convert to current 2017 values for US dollar.
    """

def clean_data():
    """
    Read the original database to get only the info we need.
    Info needed: Budget, Genre, Title, Company, Release Date, Revenue
    """
    #Note: encoding='utf-8' necessary to be able to read all chars properly.
    #One of the movie titles has a "1/3" symbol that's messing everything up.
    read_csv = open('tmdb_5000_movies.csv', 'r', encoding='utf-8')
    write_csv = open('new_database.csv', 'w', newline='', encoding='utf-8')

    reader = csv.DictReader(read_csv)
    writer = csv.DictWriter(write_csv, {'title',
                                        'genre',
                                        'prod_budget',
                                        'company',
                                        'release',
                                        'revenue'})
    writer.writeheader()

    for row in reader:
        #if 'United States of America' in row['production_countries']:
        #\ufeff is a "byte order mark" ahead of the first column name.
        #Changing encoding above to utf-8-sig would have eliminated this,
        #but broken the "1/3" symbol again.
        writer.writerow({'title': row['title'],
                         'genre': 'TEST',
                         'prod_budget': row['\ufeffbudget'],
                         'company': 'TEST',
                         'release': row['release_date'],
                         'revenue': row['revenue']})

clean_data()

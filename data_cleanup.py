"""
PURPOSE
To parse the original database for useful information that we need.
Data involving money will be corrected for inflation and put into categories.
Release dates will be categorized simply by month.
Genres and Production companies will be parsed, and the first one in each
list will be used as the category for that movie.

INFO ABOUT DATA
20 Genres
21 Production Companies (20 + Other)
12 Release Dates (Months)
6 Budget Brackets (0, and increments of 125 million, up to > 500 million)
6 Revenue Brackets (0, and increments of 250 million, up to > 1 billion)

AUTHOR
Warren Lacaba
"""
import csv
import json
import re
from collections import Counter

#Consumer Price Index values from 1913-2017
CPI_FROM_1913 = [9.9, 10.0, 10.1, 10.9, 12.8, 15.1, 17.3, 20.0, 17.9, 16.8,
                 17.1, 17.1, 17.5, 17.7, 17.4, 17.1, 17.1, 16.7, 15.2, 13.7,
                 13.0, 13.4, 13.7, 13.9, 14.4, 14.1, 13.9, 14.0, 14.7, 16.3,
                 17.3, 17.6, 18.0, 19.5, 22.3, 24.1, 23.8, 24.1, 26.0, 26.5,
                 26.7, 26.9, 26.8, 27.2, 28.1, 28.9, 29.1, 29.6, 29.9, 30.2,
                 30.6, 31.0, 31.5, 32.4, 33.4, 34.8, 36.7, 38.8, 40.5, 41.8,
                 44.4, 49.3, 53.8, 56.9, 60.6, 65.2, 72.6, 82.4, 90.9, 96.5,
                 99.6, 103.9, 107.6, 109.6, 113.6, 118.3, 124.0, 130.7,
                 136.2, 140.3, 144.5, 148.2, 152.4, 156.9, 160.5, 163.0,
                 166.6, 172.2, 177.1, 179.9, 184.0, 188.9, 195.3, 201.6,
                 207.3, 215.303, 214.537, 218.056, 224.939, 229.594,
                 232.957, 236.736, 237.017, 240.007, 244.620]
REVENUE_LIMIT = 1000000000        #Upper limit of rev for calculating brackets
BUDGET_LIMIT = 500000000          #Upper limit of budget for brackets
REVENUE_INCREMENT = 250000000     #Amount to increment revenue bracket
BUDGET_INCREMENT = 125000000      #Amount to increment budget bracket
CURR_YEAR = 2017                  #Current year for calculating inflation
MAX_COMMON_MOVIES = 21            #Need 21 because you want 20 movies, also a
                                  #majority are labelled 'empty' which
                                  #obviously doesn't count
#DATA VALIDATION FUNCTIONS----------------------------------------------------

def valid_list_of_genre(data_entry):
    """
    PURPOSE
    To ensure that input string is in the valid form of
    [{"id": 0000, "name": "NAME"}, {etc.}, {etc}]

    INPUT
    data_entry: string taken from 'genres' column in the database

    OUTPUT
    is_valid: boolean representing valid or not valid
    """
    regex = re.compile(r'\[({"id": \d+, "name": ".+"},*\s*)+]')
    is_valid = False

    if regex.match(data_entry):
        is_valid = True

    return is_valid

def valid_list_of_company(data_entry):
    """
    PURPOSE
    To ensure that input string is in the valid form of
    [{"name": "NAME", "id": 0000}, {etc.}, {etc}]

    INPUT
    data_entry: string taken from 'production_companies'
                column in the database

    OUTPUT
    is_valid: boolean representing valid or not valid
    """
    regex = re.compile(r'\[({"name": ".+", "id": \d+},*\s*)+]')
    is_valid = False

    if regex.match(data_entry):
        is_valid = True

    return is_valid

def valid_date(date_string):
    """
    PURPOSE
    To ensure that input string is in the valid form of
    YYYY-MM-DD

    INPUT
    date_string: string taken from 'release_date' column in the database

    OUTPUT
    is_valid: boolean representing valid or not valid
    """
    regex = re.compile(r'\d{4}-\d{2}-\d{2}')
    is_valid = False

    if regex.match(date_string):
        is_valid = True

    return is_valid

def valid_data(genre, company, release):
    """
    PURPOSE
    Checks data from the database if anything is blank. Zeroes in budget and
    revenue are okay. A blank title is also ok. A blank genre, company,
    and release date however, would make it impossible to categorize.

    INPUT
    genre: string in the form [{"id": 0, "name": NAME}, {etc.}]
    company: string in the form [{"id": 0, "name": NAME}, {etc.}]
    release: string in the form YYYY-MM-DD

    OUTPUT
    is_valid: boolean, representing valid or not valid
    """
    is_valid = True

    if valid_list_of_genre(genre) is False:
        is_valid = False
    if valid_list_of_company(company) is False:
        is_valid = False
    if valid_date(release) is False:
        is_valid = False

    return is_valid

#HELPER-----------------------------------------------------------------------

def most_common_companies():
    """
    PURPOSE
    Find most common companies in database, before, we had 1300 companies
    which we decided was too many classes for a database that only had
    5000 movies to begin with. 

    INPUT
    None

    OUTPUT
    set_companies: set of 20 most common movies

    NOTES
    The constant, MAX_COMMON_MOVIES is 21 rather than 20 because the most
    common movie company was actually labelled 'Empty' so I needed to
    account for this. 

    Columbia Pictures Corporation is the same company as Columbia
    Pictures. They both appear in the most common when they should be
    the same thing, so I needed to correct for this as well. 
    """
    read = open('data/tmdb_5000_movies.csv', 'r', encoding='utf-8')
    readin = csv.DictReader(read)
    comp_list = []

    for row in readin:

        company = get_company(row['production_companies']) 

        if company == 'Columbia Pictures Corporation':
            comp_list.append('Columbia Pictures')
        else:
            comp_list.append(company)

    count = Counter(comp_list)
    common = count.most_common(MAX_COMMON_MOVIES)

    set_companies = set()

    #Again, 'Empty' is the most common, so start with 1 instead of 0
    for i in range(1, len(common)):
        set_companies.add(common[i][0])

    read.close()
    return set_companies

#DATA PARSING FUNCTIONS-------------------------------------------------------

def get_date(date_string, mode):
    """
    PURPOSE
    To parse a part of a date from a string.

    INPUT
    date_string: string in the form 'YYYY-MM-DD'
    mode: 0, 1, 2 representing year, month, day

    OUTPUT
    date: int describing year, month, or day, 0 if invalid
    """
    date = 0

    if valid_date(date_string):
        if mode == 0:
            date = int(date_string[:4])
        elif mode == 1:
            date = int(date_string[5:7])
        elif mode == 2:
            date = int(date_string[8:10])
        else:
            print('Invalid mode input')
    else:
        print('Invalid date input')
      
    return date

def get_category_name(list_of_json):
    """
    PURPOSE
    Parse a category name from a string consisting of a list of json.
    
    INPUT
    list_of_json: stirng in form of
    '[{"id": 0000, "name": "NAME"}, {etc.}]'

    OUTPUT
    category: string name of category
    """
    categories = list_of_json

    #Take away the [] from the string
    categories = categories[1:len(list_of_json)-1]

    #Get the first json string by splitting by '}]
    string_array = categories.split('}')

    #Add the '}' back in for proper json format
    first_json = string_array[0] + '}'

    #Load the json so you can get the category name
    json_string = json.loads(first_json)
    category = json_string['name']

    return category

def get_genre(list_of_genre_json):
    """
    PURPOSE
    A non empty entry in "genres" will be a json of all genres associated
    with the movie. Since we should only have one category for each aspect
    of a movie, we arbitrarily choose the first entry.

    INPUT
    list_of_genre_json: string of a list of json in the form of
    [{"id": 1, "name": "Genre"}, {"id": 2, "name": "Genre"}]

    OUTPUT
    return_genre: string name of the genre, 'Empty' if input not valid
    """
    return_genre = 'Empty'

    if valid_list_of_genre(list_of_genre_json):
        return_genre = get_category_name(list_of_genre_json)

    return return_genre

def get_company(list_of_company_json):
    """
    PURPOSE
    A non empty entry will be a json of all genres associated
    with the movie. Since we should only have one category for each aspect
    of a movie, we arbitrarily choose the first entry.

    INPUT
    list_of_company_json: string of a list of json in the form of
    [{"id": 1, "name": "Company1"}, {"id": 2, "name": "Company2"}]

    OUTPUT
    return_company: string name of the company, 'Empty' if input not valid
    """
    return_company = 'Other'

    if valid_list_of_company(list_of_company_json):
        return_company = get_category_name(list_of_company_json)
        
    return return_company

def correct_inflation(old_year, curr_year, dollar):
    """
    PURPOSE
    Used to convert to current values for US dollar.

    INPUT
    old_year: year of movie release
    curr_year: current year
    dollar: original dollar value

    OUTPUT
    new_value: dollar value adjusted for inflation
    """
    new_value = 0
    old_cpi = CPI_FROM_1913[old_year - 1913]
    curr_cpi = CPI_FROM_1913[curr_year - 1913]

    if curr_cpi != 0:
        new_value = ((curr_cpi * int(dollar))/old_cpi)

    return new_value

def calculate_bracket(old_year, curr_year, dollar, abs_limit, increment):
    """
    PURPOSE
    Correct money value for inflation and then assign it a bracket.

    INPUT
    old_year: year of movie release
    curr_year: current year
    dollar: original dollar value, prior to inflation correction
    abs_limit: upper limit of money value to count
    increment: increment value of money, to determine number of brackets

    OUTPUT
    bracket: integer representing bracket, higher = more money
    """
    dollar_value = correct_inflation(old_year, curr_year, dollar)
    bracket = 0
    upper_limit = 0

    while upper_limit < dollar_value and upper_limit <= abs_limit:
        upper_limit += increment
        bracket += 1

    return bracket

#MAIN-------------------------------------------------------------------------

def clean_data():
    """
    PURPOSE
    Read the original database to get only the info we need.
    Make sure data is valid, all relevant categories are not blank.
    Write relevant data into new_database.csv. That database will be
    used during the actual data mining and classification.

    Info needed: Budget, Genre, Title, Company, Release Date, Revenue

    INPUT
    None

    OUTPUT
    None

    NOTES
    DictWriter will write a random order of headers everytime, not a problem
    considering this is only gonna be run once. Just something to remember.
    """

    common_companies = most_common_companies()

    #Note: encoding='utf-8' necessary to be able to read all chars properly.
    #One of the movie titles has a "1/3" symbol that's messing everything up.
    read_csv = open('data/tmdb_5000_movies.csv', 'r', encoding='utf-8')
    write_csv = open('data/new_database2.csv', 'w', newline='', encoding='utf-8')

    reader = csv.DictReader(read_csv)
    writer = csv.DictWriter(write_csv, {'title',
                                        'genre',
                                        'prod_budget',
                                        'company',
                                        'release',
                                        'revenue'})
    writer.writeheader()

    for row in reader:
        genre = row['genres']
        companies = row['production_companies']
        release = row['release_date']

        if valid_data(genre, companies, release):
            new_genre = get_genre(genre)
            year = get_date(release, 0)

            new_company = get_company(companies)

            """
            Columbia Pictures is a bit of an anomaly
            Columbia Pictures Corporation and Columbia Pictures are the
            same company, so you gotta correct for this
            """
            if new_company == 'Columbia Pictures Corporation':
                new_company = 'Columbia Pictures'
            
            #Only insert 20 most common companies, and 'Other'
            if new_company not in common_companies:
                new_company = 'Other'

            """
            \ufeff is a "byte order mark" ahead of the first column name.
            Changing encoding above to utf-8-sig would have apparently taken
            care of this but would have broken the "1/3" symbol again.
            """
            new_budget = calculate_bracket(year, 2017, row['\ufeffbudget'],
                                           BUDGET_LIMIT, BUDGET_INCREMENT)
            new_revenue = calculate_bracket(year, 2017, row['revenue'],
                                            REVENUE_LIMIT, REVENUE_INCREMENT)

            writer.writerow({'title': row['title'],
                             'genre': new_genre,
                             'prod_budget': new_budget,
                             'company': new_company,
                             'release': get_date(release, 1),
                             'revenue': new_revenue})
                             
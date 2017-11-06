"""
Purpose: To parse the original database for useful information that we need.
Data involving money will be corrected for inflation and put into categories.
Release dates will be categorized simply by month.
Genres and Production companies will be parsed, and the first one in each
list will be used as the category for that movie.

Info about data:
20 Genres
21 Budget Brackets (increments of 50 million, up to > 1 billion)
12 Release Dates (going by months)
1310 Production Companies
11 Revenue Brackets (increments of 100 million, up to > 1 billion)
"""
import csv
import json
"""
CPI values in the USA from 1913-2017
2017 is not finished, so its CPI is just an average of all months so far
"""
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

def valid_data(genre, company, release):
    """
    Checks data from the database if anything is blank. Zeroes in budget and
    revenue are okay. A blank title is also ok. A blank genre, company,
    and release date however, would make it impossible to categorize.
    """
    is_valid = True

    if genre == '[]':
        is_valid = False
    if company == '[]':
        is_valid = False
    if release == '':
        is_valid = False

    return is_valid

def get_year(date):
    """
    Parse the year from a YYYY-MM-DD string. Used to correct money
    values for inflation.
    """
    year = 0

    if date != '':
        year = int(date[:4])

    return year

def get_month(date):
    """
    Parse the month from a YYYY-MM-DD string. Used as one of the categories
    for classification.
    """
    month = 0

    if date != '':
        date_parts = date.split('-')
        month = date_parts[1]

    return month

def get_genre(genre_json):
    """
    A non empty entry in "genres" will be a json of all genres associated
    with the movie. Since we should only have one category for each aspect
    of a movie, we arbitrarily choose the first entry.

    Format of input string:
    [{"id": 1, "name": "Genre"}, {"id": 2, "name": "Genre"}]
    """
    return_genre = 'Empty'

    if (genre_json != '[]'):
        #Take away the [] from the string
        genre_json = genre_json[1:len(genre_json)-1]

        #Get the content inside the first {id, name}
        genre_array = genre_json.split('}')
        first = genre_array[0] + '}'

        #Now that we have the first {id, name}, we can use the json library
        json_string = json.loads(first)
        return_genre = json_string['name']

    return return_genre

def get_company(company_json):
    """
    A non empty entry will be a json of all genres associated
    with the movie. Since we should only have one category for each aspect
    of a movie, we arbitrarily choose the first entry.

    Format of input string:
    [{"id": 1, "name": "Company1"}, {"id": 2, "name": "Company2"}]
    """
    return_company = 'Empty'

    if (company_json != '[]'):
        #Take away the [] from the string
        company_json = company_json[1:len(company_json)-1]

        #Get the content inside the first {id, name}
        company_array = company_json.split('}')
        first = company_array[0] + '}'

        #Now that we have the first {id, name}, we can use the json library
        json_string = json.loads(first)
        return_company = json_string['name']
        
    return return_company

def correct_inflation(old_year, curr_year, dollar):
    """
    Used to convert to current 2017 values for US dollar.
    """
    new_value = 0
    old_cpi = CPI_FROM_1913[old_year - 1913]
    curr_cpi = CPI_FROM_1913[curr_year - 1913]

    if curr_cpi != 0:
        new_value = ((curr_cpi * int(dollar))/old_cpi)

    return new_value

def get_budget_bracket(old_year, curr_year, dollar):
    """
    Correct budget for inflation and then sort it into a bracket.
    Goes by categories of 50,000,000 up to > 1,000,000,000.
    """
    dollar_value = correct_inflation(old_year, curr_year, dollar)
    bracket = 0
    upper_limit = 0

    while upper_limit < dollar_value and upper_limit <= 1000000000:
        upper_limit += 50000000
        bracket += 1

    return bracket

def get_revenue_bracket(old_year, curr_year, dollar):
    """
    Correct revenue for inflation and then sort it into a bracket.
    Goes by categories of 100,000,000 up to > 1,000,000,000.
    """
    dollar_value = correct_inflation(old_year, curr_year, dollar)
    bracket = 0
    upper_limit = 0

    while upper_limit < dollar_value and upper_limit <= 1000000000:
        upper_limit += 100000000
        bracket += 1

    return bracket


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
        """
        \ufeff is a "byte order mark" ahead of the first column name.
        Changing encoding above to utf-8-sig would have eliminated this, but
        broken the "1/3" symbol again.
        """
        genre = row['genres']
        companies = row['production_companies']
        release = row['release_date']

        if valid_data(genre, companies, release):
            year = get_year(release)

            new_budget = get_budget_bracket(year, 2017, row['\ufeffbudget'])
            new_revenue = get_revenue_bracket(year, 2017, row['revenue'])
            new_genre = get_genre(genre)

            writer.writerow({'title': row['title'],
                             'genre': new_genre,
                             'prod_budget': new_budget,
                             'company': 'TEST',
                             'release': get_month(release),
                             'revenue': new_revenue})

clean_data()

__author__ = 'Rohit Ravikant Rane'

import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# Section 1: Start - Get data from website and organize

url = 'https://www.florida-demographics.com/cities_by_population'

# To get the data from the web page we will use requests API's get() method
response = requests.get(url)

# Beautiful Soup is a Python package for parsing HTML and XML documents
soup = BeautifulSoup(response.content, 'html.parser')

# It is always good to check the http response status code
# This should print 200

# print(response.status_code)

# Now we have collected the data from the web page
# Display the http response body
# print(response.content)

# The above data can be view in a pretty format by using beautifulsoup's prettify()
# print(soup.prettify())

# Extract data from table tag's class ranklist span8 using find method
data = soup.find('table', class_='ranklist span8')

# We create a list data_record for collect tr tag data
data_record = []

# find all tr tags by using find_all method
for record in data.find_all('tr'):
    a = record.get_text()                            # The text extracted from all tr tags using the method get_text().
    data_record.append(a)                            # Append list

# We create a list full_data
full_data = []
for new in data_record:
    d = new.replace('\n', ' ')                       # Removing all \n
    f = d.split()                                    # Create lists of relevant items
    full_data.append(f)                              # Append list
data_clean = full_data[1:-1]                         # Removing unwanted 1st and last nested lists

rank = []                                            # Create rank list
cities = []                                          # Create cities list
population = []                                      # Create population list


for j in range(0, len(data_clean)):
    rank_list = data_clean[j][0]
    cities_list = ' '.join(data_clean[j][1:-1])      # Join method use for joining cities name
    population_list = data_clean[j][-1]

    rank.append(rank_list)                           #
    cities.append(cities_list)                       # Append lists
    population.append(population_list)               #

# Update the lists for their titles
rank.insert(0, 'Florida Cities by Population Rank')  #
population.insert(0, 'Population')                   # Update lists using insert method
cities.insert(0, "City")                             #

# Section 1: End

# Section 2: Start - Creating a CSV file in data directory of collected data

fields = [rank[0], cities[0], population[0]]         # Define fields

# We create a rows list
rows = []

# The zip() function take iterables and returns an iterator of tuples.
for combine_rel in zip(rank[1::], cities[1::], population[1::]):
    # Convert a tuples into lists using list method
    rows.append(list(combine_rel))


filename = "data/florida_cities_data.csv"
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)                  # We use csv.writer module to write in a csv file

    csvwriter.writerow(fields)                       # Write fields
    csvwriter.writerows(rows)                        # Write rows

# Section 2: End

# Section 3: Start - Using pandas library to organize csv

# pd.read_csv function will take in a csv file and return a DataFrame
df = pd.read_csv('data/florida_cities_data.csv')

# Section 3: End

# Section 4: Start - Finding Data

user_input = int(input("Enter a Rank of Florida's City: "))

# The iloc method allows us to retrieve rows and columns by position.
cities_rank_list = []
for cities_rank in df.iloc[:, 0]:
    cities_rank_list.append(cities_rank)
if user_input in cities_rank_list:
    print(df.iloc[user_input-1, 1], "has rank", user_input, "and population is", df.iloc[user_input-1, 2], end=".")
else:
    print("Please enter a valid Rank between 1 and", int(rank[-1]))

# Section 4: End

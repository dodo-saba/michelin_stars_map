'''
scrapeJapanRestaurants.py
This file scrapes the restaurants with stars from a Wikipedia page.

In order:
File 01: scrapeRestaurants.py
File 01.1: scrapeJapan.py
File 02: geocodeRestaurants.py
File 03: mapRestaurants.py
'''

# %% IMPORT MODULES
from bs4 import BeautifulSoup
import requests
import pandas as pd

# %% WEBSITE TO SCRAPE:
url = 'https://en.wikipedia.org/wiki/List_of_Michelin_3-star_restaurants#Japan'

# %% SCRAPE WANTED INFO
# Initialise soup
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

# Find table
tables = soup.find_all('table', class_='wikitable')
table_japan = tables[9]  # japan is ninth on the page
rows = table_japan.find_all('tr')[1:]  # exclude header row

# Scrape name and city:
name = []
city = []

for row in rows:
    city.append(row.find_all('td')[0].text.strip())
    name.append(row.find_all('td')[1].text.strip())

# %% CREATE DATAFRAME
df_japan = pd.DataFrame()
df_japan['name'] = name
df_japan['city'] = city
df_japan['stars_num'] = pd.Series([3]*len(name))
df_japan['country'] = pd.Series(['Japan']*len(name))

# %% Export
df_japan.to_csv('.\csv\michelin_star_japan.csv', index=False, encoding = 'utf-16')

'''
scrapeRestaurants.py
This file scrapes the restaurants with stars from the Michelin guide website. Japanese restaurants not on website

In order:
File 01: scrapeRestaurants.py
File 02: geocodeRestaurants.py
File 03: mapRestaurants.py
'''

# %% IMPORT MODULES
from bs4 import BeautifulSoup
import requests
import pandas as pd

# %% SCRAPE METHODS
def create_soup(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")
    return soup

def scrape_panels(soup, restaurants):
    # Get all panels:
    panels = soup.find_all('div', class_ = 'col-md-6 col-lg-6 col-xl-3')

    # Scrape relevant info from each panel:
    # (faster to have one for loop than three list comprehensions)
    for panel in panels:
        restaurant_name = panel.find('h5').find('a').text
        restaurant_link = 'https://guide.michelin.com' + panel.find('h5').find('a')["href"]
        restaurant_stars = panel.find('i').text  # stars are coded with three letters: m (1star), n(2star), o (3star)

        # Add to dataframe:
        restaurants.loc[len(restaurants)] = [restaurant_name.strip(), restaurant_stars.strip(), restaurant_link.strip()]

def scrape_restaurant(soup):
    # Scrape address:
    # (note some restaurants have offers on, so you must choose the correct line with the address)
    # (must use the grandchild 'i' tag of 'ul' to identify the correct part)
    # (then identify correct 'li' of correct grandchild)
    description = soup.find('ul', class_='restaurant-details__heading--list')
    address = description.find('i', class_ = 'fal fa-map-marker-alt').find_parent().text

    # Separate country
    country = address.split(',')[-1].strip()

    return address, country


# %% WEBSITE TO SCRAPE:
base_url = 'https://guide.michelin.com/en/restaurants/3-stars-michelin/2-stars-michelin/1-star-michelin'
# as you can notice in the url, the filters for restaurants with michelin stars are already applied

# %% INITIALISE DATA BASE
df_restaurants = pd.DataFrame(columns = ['name', 'stars_code', 'link'])

# %% SCRAPE WANTED INFO
# Initialise soup
soup = create_soup(base_url)
next_page_button_link = ' '  # initialise so that : is not None

# Iterate the scrape until the 'next page' button doesnt exist
for i in range(1, 1000):
    # Scrape page
    scrape_panels(soup, df_restaurants)

    # Is there a next page button? :
    next_page_button = soup.find('span', class_='icon fal fa-angle-right')  # finds first next page button
    # (there are previous and next page buttons, only way to differentiate is with the icon type)
    if next_page_button is None:
        break

    # Next_page link:
    next_page = base_url + '/page/' + str(i)
    print(next_page)

    # Create new soup using link from button:
    soup = create_soup(next_page)

# %% Convert star codes to numbers
# use for loop below
df_restaurants['stars_num'] = ['']*len(df_restaurants.stars_code)

# %% Scrape address from each restaurant:
restaurant_addresses = []
restaurant_countries = []
for i in range(0, len(df_restaurants.name)):
    print(i)
    # Create soup:
    soup_restaurant = create_soup(df_restaurants.link.iloc[i])
    # Scrape page:
    res_address, res_country = scrape_restaurant(soup_restaurant)
    # Append:
    restaurant_addresses.append(res_address)
    restaurant_countries.append(res_country)

    # Convert stars code to number
    code = df_restaurants['stars_code'].iloc[i]
    if code == 'm':
        df_restaurants['stars_num'].iloc[i] = 1
    elif code == 'n':
        df_restaurants['stars_num'].iloc[i] = 2
    elif code == 'o':
        df_restaurants['stars_num'].iloc[i] = 3

# Add columns:
df_restaurants["country"] = restaurant_countries
df_restaurants["address"] = restaurant_addresses

# Re-arrange:
df_restaurants = df_restaurants[['name', 'stars_code', 'stars_num', 'country', 'address', 'link']]
# %% Export
df_restaurants.to_csv('.\csv\michelin_star_restaurants.csv', index=False, encoding = 'utf-16')


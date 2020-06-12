'''
geocodeRestaurants.py
This file uses googlemaps and geopandas to geocode adresses obtained from web scraping the restaurants
Uses output from scrapeRestaurants.py

In order:
File 01: scrapeRestaurants.py
File 02: geocodeRestaurants.py
File 03: mapRestaurants.py
'''

# Using Google API services:
# https://towardsdatascience.com/how-to-generate-lat-and-long-coordinates-from-an-address-column-using-pandas-and-googlemaps-api-d66b2720248d
# https://developers.google.com/maps/documentation/geocoding/start
# Note that when calling gmaps.geocode a json parsed answer is return
# navigating json: https://onlinejournalismblog.com/2011/04/14/data-for-journalists-json-for-beginners/

# %% IMPORT MODULES
import pandas as pd
import googlemaps
gmaps = googlemaps.Client(key='ENTER_KEY')
# Api key:
# https://console.cloud.google.com/apis/dashboard?project=avian-pact-280019

# %% IMPORT FILES
df = pd.read_csv('.\csv\michelin_stars_restaurants.csv', encoding ='utf-16')

# Initialise columns
df['geocoded_address'] = ['']*len(df)
df['lat'] = df['geocoded_address']
df['long'] = df['geocoded_address']
df['approx_loc'] = df['geocoded_address']

# %% Geocode data:
for i in range(0, len(df.name)):
    print(i)
    # Find location
    location = gmaps.geocode(df.loc[i, 'address'])

    # If location cannot be found, try again using the restaurant name:
    if location == []:

        short_address = df.loc[i, 'address'].split(',')
        # Retry with just name and city
        location = gmaps.geocode(df.name[i] + ' ' + short_address[-1])

        if location == []:
            # Log approximate location:
            df.loc[i, 'approx_loc'] = 'Y'

            # Approx using post code:
            location = gmaps.geocode(short_address[-3:])

            # If failed assign None:
            if location == []:
                df.loc[i, 'geocoded_address'] = None
                df.loc[i, 'lat'] = None
                df.loc[i, 'long'] = None
                continue
    # Assign:
    df.loc[i, 'geocoded_address'] = location[0]['formatted_address']
    df.loc[i, 'lat'] = location[0]['geometry']['location']['lat']
    df.loc[i, 'long'] = location[0]['geometry']['location']['lng']

# %% Export
df.to_csv('.\csv\michelin_star_restaurants_geocoded.csv', encoding = 'utf-16')

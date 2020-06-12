'''
mapRestaurants.py
This file uses folium to create an interactive map using the geocoded restaurant results
Uses output from scrapeRestaurants.py

In order:
File 01: scrapeRestaurants.py
File 02: geocodeRestaurants.py
File 03: mapRestaurants.py
'''

# %% DOCS
# Popups:
# https://nbviewer.jupyter.org/github/python-visualization/folium/blob/master/examples/Popups.ipynb
# Icon list:
# https://stackoverflow.com/questions/53721079/python-folium-icon-list
# Markers:
# https://python-visualization.github.io/folium/plugins.html
# Marker custom options:
# https://github.com/Leaflet/Leaflet.markercluster#options
# %% IMPORT MODULES
import pandas as pd
import folium
from folium.plugins import MarkerCluster

# %% IMPORT FILES
# World
df_res = pd.read_csv('.\csv\michelin_star_restaurants_geocoded.csv', encoding = 'utf-16')
df_res.drop(columns='Unnamed: 0', inplace = True)

# Japan:
df_jap = pd.read_csv('.\csv\michelin_star_japan_geocoded.csv', encoding = 'utf-16')

# Join dataframes:
df = df_res.append(df_jap)

# Resort to have one star first and three stars last (so that three stars are plotted last and thus on top)
df.sort_values(ascending=True, by=['stars_num'], inplace=True)
df.reset_index(drop=True, inplace=True)  # reset index after sorting
# %% BASE MAP
m = folium.Map(location=[45, 0], zoom_start=2,
              tiles = 'cartodbpositron')

# Marker color list:
colors = ['#cd7f32', '#c0c0c0', '#FFD700']

# %% CREATE MARKER CLUSTERS
# Create marker clusters, for each star (same code different names):
marker_cluster_1star = MarkerCluster(
    name='1 star  ( * )',
    overlay=True,
    control=True,
    icon_create_function=None,
    options = {'disableClusteringAtZoom': 7})  # this disables marker clustering at specified zoom level
marker_cluster_2star = MarkerCluster(
    name='2 stars (** )',
    overlay=True,
    control=True,
    icon_create_function=None,
    options = {'disableClusteringAtZoom': 7})
marker_cluster_3star = MarkerCluster(
    name='3 stars (***)',
    overlay=True,
    control=True,
    icon_create_function=None,
    options = {'disableClusteringAtZoom': 7})

# %% ADD RESTAURANT MARKERS TO CLUSTERS
for i in range(0, len(df.name)):
    print(i)
    if df.country[i] != 'Japan':
        # Location
        lat = df.loc[i, 'lat']
        long = df.loc[i, 'long']
        google_link = "https://maps.google.com/?q="+str(lat)+","+str(long)+"&ll="+str(lat)+","+str(long)+"&z=15"

        # html:
        html = """
            <h4>{name}</h4>
            <h3>{stars}</h3>
            <a href = {link} target="_blank">View on Michelin</a><br>
            <a href = {google_search} target="_blank">View on Google</a>
            """.format(name=df.loc[i, "name"],
                       stars = '*'*df.loc[i, 'stars_num'],
                       link = df.loc[i, 'link'],
                       google_search = google_link)

        # Create marker:
        m_color = colors[df.loc[i,'stars_num']-1]
        marker = folium.Marker(location = [lat, long],
                      popup=html,
                      tooltip = df.loc[i, 'name'],
                      icon = folium.Icon(icon = 'glyphicon-star', color = 'gray', icon_color=m_color))

        # Add marker to relevant cluster:
        if df.loc[i, 'stars_num'] == 1:
            marker_cluster_1star.add_child(marker)
        elif df.loc[i, 'stars_num'] == 2:
            marker_cluster_2star.add_child(marker)
        elif df.loc[i, 'stars_num'] == 3:
            marker_cluster_3star.add_child(marker)

    elif df.country[i] == 'Japan':
        # Location
        lat = df.loc[i, 'lat']
        long = df.loc[i, 'long']
        google_link = "https://maps.google.com/?q=" + str(lat) + "," + str(long) + "&ll=" + str(lat) + "," + str(long) + "&z=15"

        # html:
        html = """
            <h4>{name}</h4>
            <h3>{stars}</h3>
            <a href = {google_search} target="_blank">View on Google</a>
            """.format(name=df.loc[i, "name"],
                       stars='*' * df.loc[i, 'stars_num'],
                       google_search=google_link)

        # Create marker:
        m_color = colors[df.loc[i, 'stars_num'] - 1]
        marker = folium.Marker(location=[lat, long],
                               popup=html,
                               tooltip=df.loc[i, 'name'],
                               icon=folium.Icon(icon='glyphicon-star', color='gray', icon_color=m_color))

        # Add marker to relevant cluster (all Japan restaurants three stars):
        marker_cluster_3star.add_child(marker)
# %% SAVE MAP AS HTML
# Add clusters to map:
marker_cluster_1star.add_to(m)
marker_cluster_2star.add_to(m)
marker_cluster_3star.add_to(m)
# Add layer control
folium.LayerControl().add_to(m)
m.save('interactive_map.html')

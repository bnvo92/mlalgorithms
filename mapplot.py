import folium
import geocoder
import pandas as pd
import csv


location = 'New York City'
g = geocoder.google(location)
g.latlng


outfile = 'nyu_data.csv'
cols = ['user', 'created_at', 'latitude', 'longitude', 'text']
df = pd.read_csv(outfile, header=0, names = cols)


df = df.dropna()

#create dataframe with latitudes and longitudes

df['coord'] = tuple(zip(df['latitude'],df['longitude']))

map_osm = folium.Map(location = g.latlng, zoom_start = 11)

folium.circle_Marker(location = g.latlng, radius = 500, num_sides = 10,
                      line_color = '#3186cc',
                      fill_color = '#3186cc').add_to(map_osm)

for row in df.itertuples():
    popup = '@'+ str(row[1])+': ' + str(str(row[5]).encode('utf-8', errors = 'ignore'))[2:-1]
    folium.Marker(location = row[6], popup=popup).add_to(map_osm)
    
map_osm.save('nyu_map2.html')

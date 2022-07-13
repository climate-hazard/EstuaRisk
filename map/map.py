import os
import math
import folium
import random
import logging
import pandas as pd

# Read geodata
df = pd.read_csv(os.path.join("..", "estuary.csv"))
mean_lat = df["Lat"].mean()
mean_lon = df["Lon"].mean()

# Create map object
m = folium.Map(location=[mean_lat, mean_lon], zoom_start=6)

# Global tooltip
tooltip = 'Click For More Info'

# colors = ['red', 'darkred', 'lightred', 'darkpurple', 'pink']
# colors = ['#feb5a5', '#ff9079', '#ff6a4a', '#ff4b24', '#fe3004']  # pinkish to reddish
colors = ['#ffc300', '#ff5733', '#c70039', '#581845']  # orange to dark red (lime ''#daf7a6' is not good on maps)
random_colors = random.choices(colors, k=len(df))

areas = [139.2, 12.86, 251.8, 344.5, 417.3, 600.9, 1029,
        6000,209, 150, 50, 4325, 9948, 2175.6]

img_filenames = [
    '../img/Flood-Feb2020-Essex-EssexLive.jpg',
    '../img/Flood-Dec2012-Camel-River-AdrianLangdon-blog.jpg',
    '../img/Flood-Feb2022-Glasgow-Eyes.jpg',
    '../img/Flood-Feb2021-Llanrwst-BBC.jpg',
    '../img/Flood-Jan2011-Machynlleth-BBC.jpg',
    '../img/Flood-Nov2012-Exeter-BBC.jpg',
    '../img/Flood-Feb2021-Llanrwst-BBC.jpg',
    '../img/Flood-2020-Edinburgh-OBrien_SWNS.jpg',
    '../img/Flood-2019-York-Humber-Yorkshire-Post.jpg',
    '../img/Flood-Dec2019-KentOnline.jpg',
    '../img/Flood-Nov2018-Milford-Haven-Pembrokeshire-Herald.jpg',
    '../img/Flood-Dec2021-Portsmouth-The-News.jpg',
    '../img/Flood-2022-Severn-Ironbridge-Times.jpg',
    '../img/Flood-2014-Thames-Mirror-UK.jpg',
    '../img/Flood-Dec2013-Newcastle-ChronicleLive.jpg',
]

# Create markers
for i in range(len(df)):
    name = df.iloc[i]['Estuary']    # df['Estuary'][i]
    lat = df.iloc[i]['Lat']
    lon = df.iloc[i]['Lon']
    risk_color = random_colors[i]

    # folium.Marker(...).add_to(m)

    folium.CircleMarker(
        location=[lat, lon],
        radius=math.sqrt(areas[i]),
        popup=f'''<h3>{name}</h3><p>Catchment area: {areas[i]} km²</p>
                <img src="{img_filenames[i]}" width="200%">''',
        color=risk_color,
        fill=True,
        fill_color=risk_color,
    ).add_to(m)

    try:
        overlay = os.path.join('..', 'data', 'downloaded',
                f'EA_RecordedFloodOutlines_{name}', 'data', 
                'Recorded_Flood_Outlines.json')
        if os.path.getsize(overlay) > 1_000_000:
            logging.warning(f'Omit big file recorded flooding in {name}')
            continue

        print(f'Added recorded flooding in {name}')
        folium.GeoJson(overlay, name=f'Recorded flooding in {name}').add_to(m)
    except:
        logging.error(f'Error loading recorded flooding in {name}')
    

# folium.Marker([42.374150, -71.122410],
#               popup='<strong>Location Four</strong>',
#               tooltip=tooltip,
#               icon=folium.Icon(color='green', icon='leaf')).add_to(m), # 'cloud'


# Geojson overlay
overlay = os.path.join('..', 'data', 'downloaded',
                'EA_RecordedFloodOutlines_Kent', 'data', 
                'overlay_epsg.json')
folium.GeoJson(overlay, name='recorded flooding in Kent').add_to(m)  # Simplified


# Create a layer control object and add it to our map instance
folium.LayerControl().add_to(m)

# Create custom marker icon
# logoIcon = folium.features.CustomIcon('logo.png', icon_size=(50, 50))

# Show map
# m

# Generate map
m.save('map.html')

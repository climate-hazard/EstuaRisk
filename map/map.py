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
    'img/Flood-Feb2020-Essex-EssexLive.jpg',
    'img/Flood-Dec2012-Camel-River-AdrianLangdon-blog.jpg',
    'img/Flood-Feb2022-Glasgow-Eyes.jpg',
    'img/Flood-Feb2021-Llanrwst-BBC.jpg',
    'img/Flood-Jan2011-Machynlleth-BBC.jpg',
    'img/Flood-Nov2012-Exeter-BBC.jpg',
    'img/Flood-Feb2021-Llanrwst-BBC.jpg',
    'img/Flood-2020-Edinburgh-OBrien_SWNS.jpg',
    'img/Flood-2019-York-Humber-Yorkshire-Post.jpg',
    'img/Flood-Dec2019-KentOnline.jpg',
    'img/Flood-Nov2018-Milford-Haven-Pembrokeshire-Herald.jpg',
    'img/Flood-Dec2021-Portsmouth-The-News.jpg',
    'img/Flood-2022-Severn-Ironbridge-Times.jpg',
    'img/Flood-2014-Thames-Mirror-UK.jpg',
    'img/Flood-Dec2013-Newcastle-ChronicleLive.jpg',
]

# Create markers
for i in range(len(df)):
    name = df.iloc[i]['Estuary']    # df['Estuary'][i]
    lat = df.iloc[i]['Lat']
    lon = df.iloc[i]['Lon']
    risk_color = random_colors[i]
    
    # ▷ folium.Marker(...icon=folium.Icon(color='green', icon='leaf')).add_to(m)  # icon can be 'leaf', 'cloud', etc.

    folium.CircleMarker(
        location=[lat, lon],
        radius=math.sqrt(areas[i]),
        popup=f'''<h3>{name.replace(' ', '⠀') + '⠀'*12}</h3>
                <p>Catchment area: {areas[i]} km²</p>
                <iframe src="./plot_Conwy.html" />
                <a href="./plot_Conwy.html"><img alt="Chart" src="./plot_Conwy.png" width="300" target="_blank" /></a>
                <img src="{img_filenames[i]}" width="100%">''',
        color=risk_color,
        fill=True,
        fill_color=risk_color,
    ).add_to(m)

    try:
        # overlay = os.path.join('..', 'data', 'downloaded',
        #         f'EA_RecordedFloodOutlines_{name}', 'data', 
        #         'Recorded_Flood_Outlines.json')
        overlay = os.path.join('..', 'data', 'flood_outline',
                f'Converted_Flood_Outlines_{name}.json')
        if os.path.getsize(overlay) > 1_000_000:   # 1 MB
            logging.warning(f'Omit big file recorded flooding in {name}')
            continue

        # Converting coordinates:
        # https://gis.stackexchange.com/questions/166934/python-library-for-converting-geojson-multi-polygon-to-polygon
        # https://pyproj4.github.io/pyproj/stable/api/transformer.html#pyproj-transform
        # https://all-geo.org/volcan01010/2012/11/change-coordinates-with-pyproj/
        # >>> from pyproj import Transformer
        # >>> transformer = Transformer.from_crs("epsg:27700", "epsg:4326")
        # >>> transformer.transform(581882.70000000019,214267.03999999911)
        # (51.7974703631485, 0.6362507110039868)

        print(f'Added recorded flooding in {name}')
        folium.GeoJson(overlay, name=f'Recorded flooding in {name}').add_to(m)
    except:
        logging.error(f'Error loading recorded flooding in {name}')
    

# Geojson overlay: need to convert from EPSG:27700 to EPSG:4326 (long/lat)
overlay_flood_geojson = os.path.join('..', 'data', 'downloaded',
                'EA_RecordedFloodOutlines_Kent', 'data', 
                'overlay_epsg.json')
folium.GeoJson(overlay_flood_geojson, 
            name='recorded flooding in Kent').add_to(m)  # Simplified

# Image overlay (population density)
img = folium.raster_layers.ImageOverlay(
    name='UK population',
    image='UK_population_overlay.png',
    bounds=[[-8.4, 1.8], [50, 61]],
    opacity=0.4,
    zindex=1,
    )
img.add_to(m)

folium.LayerControl().add_to(m)

m.save('map.html')

# Create custom marker icon
# logoIcon = folium.features.CustomIcon('logo.png', icon_size=(50, 50))

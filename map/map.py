import os
import math
import folium
import random
import logging
import pandas as pd


# Read geodata
df = pd.read_csv(os.path.join("estuary.csv"))
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
        6000, 209, 150, 50, 4325, 9948, 2175.6]

img_filenames = [
    'map/img/Flood-Feb2020-Essex-EssexLive.jpg',
    'map/img/Flood-Dec2012-Camel-River-AdrianLangdon-blog.jpg',
    'map/img/Flood-Feb2022-Glasgow-Eyes-cropped.jpg',
    'map/img/Flood-Feb2021-Llanrwst-BBC.jpg',
    'map/img/Flood-Jan2011-Machynlleth-BBC.jpg',
    'map/img/Flood-Nov2012-Exeter-BBC.jpg',
    'map/img/Flood-Feb2021-Llanrwst-BBC.jpg',
    'map/img/Flood-2020-Edinburgh-OBrien_SWNS.jpg',
    'map/img/Flood-2019-York-Humber-Yorkshire-Post.jpg',
    'map/img/Flood-Dec2019-KentOnline.jpg',
    'map/img/Flood-Nov2018-Milford-Haven-Pembrokeshire-Herald.jpg',
    'map/img/Flood-Dec2021-Portsmouth-The-News.jpg',
    'map/img/Flood-2022-Severn-Ironbridge-Times.jpg',
    'map/img/Flood-2014-Thames-Mirror-UK.jpg',
    'map/img/Flood-Dec2013-Newcastle-ChronicleLive.jpg',
]


def create_map(show_dens=False, outfile=True):
    ''' Creates a Folium map with optional overlay and HTML file output. '''
    # Create markers
    for i in range(len(df)):
        name = df.iloc[i]['Estuary']    # df['Estuary'][i]
        lat = df.iloc[i]['Lat']
        lon = df.iloc[i]['Lon']
        risk_color = random_colors[i]
        risk_color = 'darkred'
        
        # ▷ folium.Marker(...icon=folium.Icon(color='green', icon='leaf')).add_to(m)  # icon can be 'leaf', 'cloud', etc.
        # <a href="./plot_Conwy.html"><img alt="Chart" src="./plot_Conwy.png" width="300" target="_blank" /></a>
        folium.CircleMarker(
            location=[lat, lon],
            radius=math.sqrt(300), # math.sqrt(areas[i]),
            popup=f'''<h3>{name.replace(' ', '⠀') + '⠀'*12}</h3>
                    <p>Catchment area: {areas[i]} km²</p>
                    <iframe src="./map/plot_{name}.html" width="400" height="250" />
                    <img src="{img_filenames[i]}" width="100%" />''',
            color=risk_color,
            fill=True,
            fill_color=risk_color,
        ).add_to(m)

        # try:
        #     overlay = os.path.join('map', 'data', 'flood_outline',
        #             f'Converted_Flood_Outlines_{name}.json')
        #     if os.path.getsize(overlay) > 1_000_000:   # 1 MB
        #         logging.warning(f'Omit big file recorded flooding in {name}')
        #         continue

        #     # Converting coordinates from EPSG:27700 to EPSG:4326 (done in trans_proj.py)

        #     print(f'Added recorded flooding in {name}')
        #     folium.GeoJson(overlay, name=f'Recorded flooding in {name}').add_to(m)
        # except:
        #     logging.error(f'Error loading recorded flooding in {name}')
        
        overlay_flood_geojson = os.path.join('data', 'flood_outline',
                            f'Flood_Outlines_{name}.json')
        if not os.path.isfile(overlay_flood_geojson):
            print('File Flood extent not exist for:', name)
            continue
        
        folium.GeoJson(overlay_flood_geojson, 
                    name=f'Recorded flooding in {name}').add_to(m)
        print('Flood extent', name)

    img = folium.raster_layers.ImageOverlay(
        name='Flood Conwy',
        image='map/Conwy_flood.png',
        bounds=[[53.095, -3.895], [53.325, -3.735]],
        opacity=0.5,
        zindex=1,
        )
    img.add_to(m)

    if show_dens:
        # Image overlay (population density)
        img = folium.raster_layers.ImageOverlay(
            name='UK population',
            image='map/UK_population_overlay.png',
            bounds=[[49.9, -8.0], [60.5, 1.8]],
            opacity=0.4,
            zindex=1,
            )
        img.add_to(m)

    folium.LayerControl().add_to(m)

    if outfile:
        m.save('map.html')

    # Create custom marker icon
    # logoIcon = folium.features.CustomIcon('logo.png', icon_size=(50, 50))


if __name__ == '__main__':
    create_map(show_dens=False, outfile=True)

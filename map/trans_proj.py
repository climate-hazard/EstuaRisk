# Transform projections from UK Ordnance Survey, 1936 datum to WGS84 (lat/long).
# The EPSG:4326 LatLon system with WGS84 datum is required for geojson maps
# to be overlaid on Folium maps.
import os
import json
from shapely.geometry import shape, mapping

json_file = os.path.join('data', 'flood_outline',
        f'Recorded_Flood_Outlines_Blackwater.json')
json_file_out = os.path.join('data', 'flood_outline',
        f'Converted_Flood_Outlines_Blackwater.json')

# Converting coordinates:
# https://gis.stackexchange.com/questions/166934/python-library-for-converting-geojson-multi-polygon-to-polygon
# https://pyproj4.github.io/pyproj/stable/api/transformer.html#pyproj-transform
# https://all-geo.org/volcan01010/2012/11/change-coordinates-with-pyproj/
# >>> from pyproj import Transformer
# >>> transformer = Transformer.from_crs("epsg:27700", "epsg:4326")
# >>> transformer.transform(581882.70000000019,214267.03999999911)
# (51.7974703631485, 0.6362507110039868)

from pyproj import Transformer
transformer = Transformer.from_crs("epsg:27700", "epsg:4326")
transformer.transform(581882.70000000019,214267.03999999911)

json_data = json.load(open(json_file))

for i, feature in enumerate(json_data['features']):
    coords = feature['geometry']['coordinates']
    for ii in range(len(coords)):
        if isinstance(coords[ii][0][0], float):
            # print('>>>', coords[ii][0][0])
            (lat, lon) = transformer.transform(coords[ii][0][0], coords[ii][0][1])
            json_data['features'][i]['geometry']['coordinates'][0][0] = [lat, lon]
    
    if not isinstance(coords[0][0][0], float):   # Check is it ok with deeper nests? (Converted_Flood_Outlines_Blackwater.json)
        print(type(coords[0][0][0]), len(coords[0][0][0]), end='.')
        # print('>>>>', coords[0][0][0])
        for j, (easting, northing) in enumerate(coords[0][0]):
            print('>', j, '>', easting)
            (lat, lon) = transformer.transform(easting, northing)
            json_data['features'][i]['geometry']['coordinates'][0][0][j] = [lat, lon]

with open(json_file_out, 'w') as outfile:
    json.dump(json_data, outfile)

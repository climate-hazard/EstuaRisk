# Transform projections from UK Ordnance Survey, 1936 datum to WGS84 (lat/long).
# The EPSG:4326 LatLon system with WGS84 datum is required for geojson maps
# to be overlaid on Folium maps.
import os
import json
from pyproj import Transformer
transformer = Transformer.from_crs("epsg:27700", "epsg:4326")

# Converting coordinates:
# https://gis.stackexchange.com/questions/166934/python-library-for-converting-geojson-multi-polygon-to-polygon
# https://pyproj4.github.io/pyproj/stable/api/transformer.html#pyproj-transform
# https://all-geo.org/volcan01010/2012/11/change-coordinates-with-pyproj/


json_file = os.path.join('data', 'flood_outline',
        f'Recorded_Flood_Outlines_Blackwater.json')
json_file_out = os.path.join('data', 'flood_outline',
        f'draft_Blackwater.json')
        # f'Converted_Flood_Outlines_Blackwater.json')

# template for geoJSON files as example for `overlay.json` (Cambridge MA)
json_template = """{
  "type": "FeatureCollection",
  "features": %s
}
"""

feature_template = """{
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "LineString",
        "coordinates": %s
      }
    }
"""


features = []
json_data = json.load(open(json_file))

for i, feature in enumerate(json_data['features']):
    coords = feature['geometry']['coordinates']
    feature_coords = []
    for ii in range(len(coords)):
        if isinstance(coords[ii][0][0], float):
            # print('>>>', coords[ii][0][0])
            (lat, lon) = transformer.transform(coords[ii][0][0], coords[ii][0][1])
            json_data['features'][i]['geometry']['coordinates'][0][0] = [lon, lat]
            feature_coords.append([lon, lat])
    if feature_coords:
        # features.append(feature_coords)
        feature_json = feature_template % feature_coords
        features.append(json.loads(feature_json))  # TODO: json.loads converts all " " to ' '. Needs to manually replace in the output file.
    
    feature_coords = []
    if not isinstance(coords[0][0][0], float):   # Check is it ok with deeper nests? (Converted_Flood_Outlines_Blackwater.json)
        print(type(coords[0][0][0]), len(coords[0][0][0]), end='.')
        # print('>>>>', coords[0][0][0])
        for j, (easting, northing) in enumerate(coords[0][0]):
            print('>', j, '>', easting)
            (lat, lon) = transformer.transform(easting, northing)
            json_data['features'][i]['geometry']['coordinates'][0][0][j] = [lon, lat]
            feature_coords.append([lon, lat])
    if feature_coords:
        # features.append(feature_coords)
        feature_json = feature_template % feature_coords
        features.append(json.loads(feature_json))


with open(json_file_out, 'w') as outfile:
    outfile.write(json_template % features )
    # json.dump(json_data, outfile)

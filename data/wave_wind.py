import time
import cdsapi
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def template(up, left, down, right, year_start, year_end):
    ''' Create a template for the request.
        Parameter: `up` - `float`, the upper (north-bound) latitude
        Parameter: `left` - `float`, the left (west-bound) longitude
        Parameter: `down` - `float`, the lower (south-bound) latitude
        Parameter: `right` - `float`, the right (east-bound) longitude
        Parameter: `year_start` - `int`, the start year
        Parameter: `year_end` - `int`, the end year
    '''
    return {
        'product_type': 'reanalysis',
        'format': 'grib',
        'month': [
            '01', '02', '11',
            '12',
        ],
        'year': [str(year) for year in range(year_start, year_end + 1)],
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
            '31',
        ],
        'time': [
            '00:00', '01:00', '02:00',
            '03:00', '04:00', '05:00',
            '06:00', '07:00', '08:00',
            '09:00', '10:00', '11:00',
            '12:00', '13:00', '14:00',
            '15:00', '16:00', '17:00',
            '18:00', '19:00', '20:00',
            '21:00', '22:00', '23:00',
        ],
        'area': [
            up, left, down,
            right,
        ],
        'variable': [
            'significant_height_of_combined_wind_waves_and_swell',
            '10m_u_component_of_wind', '10m_v_component_of_wind', 'mean_sea_level_pressure',
        ],
    }


def get_data(name, up, left, down, right, year_start, year_end):
    ''' Query data from CDS for a given gauge.

        Parameter: `name` - `str`, the name of the gauge
        Parameter: `up` - `float`, the upper (north-bound) latitude
        Parameter: `left` - `float`, the left (west-bound) longitude
        Parameter: `down` - `float`, the lower (south-bound) latitude
        Parameter: `right` - `float`, the right (east-bound) longitude
        Parameter: `year_start` - `int`, the start year
        Parameter: `year_end` - `int`, the end year

        Return: None
        Side effect: The request is sent and the data is saved in a grib file.
    '''
    print('Retrieving data for', name)
    template_dict = template(up, left, down, right, year_start, year_end)
    c.retrieve(
        'reanalysis-era5-single-levels',
        template_dict,
        f'data/{name}_wind_wave.grib',
    )
    print('Suspending for 60 seconds to avoid rate limiting')
    time.sleep(60)


def plot_location(my_map, lat, lon):
    x,y = my_map(lon, lat)
    point = my_map.plot(x, y, 'bo', markersize=5)  # [0]
    plt.show()


def background_map():
    my_map = Basemap(projection='lcc', resolution = 'l', area_thresh = 1000.0,
            lat_0=52, lon_0=0, llcrnrlon=-10,llcrnrlat=46,urcrnrlon=8,urcrnrlat=62)
    my_map.drawcoastlines()
    my_map.drawcountries()
    my_map.fillcontinents(color = 'coral')
    my_map.drawmapboundary()
    my_map.drawmeridians(np.arange(-14, 10, 2))
    my_map.drawparallels(np.arange(46, 64, 2))
    return my_map


c = cdsapi.Client()

df = pd.read_csv('data/sea.csv')

map = background_map()
coords = [(52.00,1.50), (50.75,-4.75), (55.50,-5.00), (53.50,-3.50), (52.50,-4.25), (50.50,-3.25), (56.25,-2.50),
        (53.5,0.25), (54.00,-3.25), (51.75,-5.25), (50.75,-1.00), (51.25,-3.50), (51.50,1.00), (55.00,-1.25),]

for index in range(len(df)):
    site = df.iloc[index]['Estuary']
    lat = df.iloc[index]['WaveLat']
    lon = df.iloc[index]['WaveLon']
    plot_location(map, lat, lon)

    # Request to CDS typically takes about 30 minutes to process.
    # Due to latency in data downloading, parts of the following code
    # are commented out and executed in turn.

    # get_data(site, lat+0.1, lon-0.1, lat-0.1, lon+0.1, 1959, 1968)
    # get_data(site, lat+0.1, lon-0.1, lat-0.1, lon+0.1, 1969, 1978)
    # get_data(site, lat+0.1, lon-0.1, lat-0.1, lon+0.1, 1979, 1988)
    # get_data(site, lat+0.1, lon-0.1, lat-0.1, lon+0.1, 1989, 1998)
    # get_data(site, lat+0.1, lon-0.1, lat-0.1, lon+0.1, 1999, 2008)
    # get_data(site, lat+0.1, lon-0.1, lat-0.1, lon+0.1, 2009, 2018)
    if site != 'Severn' and site  > 'Kent':
        get_data(site, lat+0.1, lon-0.1, lat-0.1, lon+0.1, 2019, 2021)



import zipfile
import urllib.request
import pandas as pd


def download_data():
    ''' Download the peak flow data from the NRFA website, then
        extract the `amax.csv` file containing peak values.

        Side effect: Creating file `amax.csv`.
    '''
    url = 'https://nrfa.ceh.ac.uk/sites/default/files/NRFAPeakFlow_v10.zip'
    urllib.request.urlretrieve(url, 'NRFAPeakFlow_v10.zip')
    with zipfile.ZipFile('NRFAPeakFlow_v10.zip', 'r') as zip_ref:
        zip_ref.extract('amax.csv', path='./downloaded_NRFA')


def extract(datafile_name):
    ''' Extract the peak flow data from the downloaded file (`datafile_name`),
        then create data files for each river.

        Side effect: `"./data/{river}.csv"` files created, 
                    each contains a series of peak flow rates sorted descending.
    '''
    df = pd.read_csv('./downloaded_NRFA/amax.csv')
    river_ids = pd.read_csv('rivers.csv')['StationNo'].to_list()
    for river in river_ids:
        if not river.startswith('?'):
            river = '0' + river
        df = df[df['StationNo'] == river]
        df.to_csv(f'./data/{river}.csv', index=False)

if __name__ == '__main__':
    download_data()
    print('Done')

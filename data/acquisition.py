# !pip install pandas requests BeautifulSoup4 
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


base_url = "https://www.bodc.ac.uk/data/hosted_data_systems/sea_level/uk_tide_gauge_network/processed/"


def get_gauge_names():
    df = pd.read_csv("estuary.csv")
    return list(df["Tide"])


def scrape(list_gauges):
    response = requests.get(base_url)
    soup = bs(response.content, 'html.parser')
    print('Webpage:', soup.title.string)

    list_years = []
    get_years = False

    table_data = soup.find_all('td')
    for entry in table_data:
        text = entry.text.strip()
        if text in list_gauges: 
            get_years = True
        elif text.split(",")[0] in list_gauges:
            get_years = True
        elif get_years:
            list_years.append(text.split(','))
            get_years = False
    
    return list_years


def fill_form():
    driver = webdriver.Chrome('D:\\Users\\Public\\Downloads\\chocoportable\\bin\\chromedriver.exe')
    driver.get('https://www.bodc.ac.uk/data/hosted_data_systems/sea_level/uk_tide_gauge_network/processed_customise_time_selection/')
    time.sleep(2)

    btn_date = driver.find_element(By.ID, 'btndate')
    btn_date.click()
    time.sleep(1)
    date_range_from = driver.find_element(By.ID, 'sdatepicker')
    date_range_from.send_keys('1981-01-01')
    date_range_to = driver.find_element(By.ID, 'edatepicker')
    date_range_to.send_keys('2022-05-31')
    btn_update = driver.find_element(By.ID, 'btndateUpdate')
    btn_update.click()

    time.sleep(1)
    btn_site = driver.find_element(By.ID, 'btnsite')
    btn_site.click()
    time.sleep(1)
    item_leith = driver.find_element(By.XPATH, '//*[@id="site"]/option[18]')
    item_leith.click()
    btn_site_update = driver.find_element(By.ID, 'btnsiteUpdate')
    btn_site_update.click()

    dataset_format = driver.find_element(By.ID, 'datasetFormat')
    # dataset_format.select_by_index(1)   # CSV - obsolete
    _ = Select(dataset_format).select_by_index(1)  # CSV

    btn_add_basket = driver.find_element(By.ID, 'btnAddBasket')
    btn_add_basket.click()


    time.sleep(5)
    # ans3.send_keys(Keys.ENTER)
    driver.quit()   # close: 1 tab


list_gauges = get_gauge_names()
data_available = scrape(list_gauges)
# print(data_available)

assert len(list_gauges) == len(data_available)  # 14

df = pd.DataFrame({'gauges': list_gauges, 'years': data_available})
# df.to_csv('data_available.txt', sep='\t')   # already

fill_form()

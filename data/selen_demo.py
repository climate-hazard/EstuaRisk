import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def fill_form():
    driver = webdriver.Chrome('D:\\Users\\Public\\Downloads\\chocoportable\\bin\\chromedriver.exe')
    driver.get('https://docs.google.com/forms/d/1AetRu2JMsjKl5CFv9gMZr4Sn4MYKDyaI6IR6bOKjE14/')
    # print('Filling google form')
    time.sleep(2)

    ans1 = driver.find_element(by=By.XPATH, value='//*[@id="i8"]/div[3]/div')
    ans1.click()

    ans2a = driver.find_element(by=By.XPATH, value='//*[@id="i19"]/div[2]')
    ans2a.click()
    ans2b = driver.find_element(by=By.XPATH, value='//*[@id="i25"]/div[2]')
    ans2b.click()

    ans3 = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    ans3.send_keys('Monaco')
    time.sleep(5)
    ans3.send_keys(Keys.ENTER)
    driver.quit()   # close: 1 tab


fill_form()

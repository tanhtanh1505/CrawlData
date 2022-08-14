# install chromium, its driver, and selenium
!apt-get update
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
!pip install selenium
# set options to be headless, ..
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--lang=es')
# open it, go to a website, and get results
driver = webdriver.Chrome('chromedriver',options=options)

from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from selenium import webdriver
import time

from google.colab import drive
drive.mount('/content/drive')

cd /content/drive/MyDrive/Data Analyst/Spiderum

from selenium.common.exceptions import NoSuchElementException        
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

from numpy.ma.core import append
spiderum = pd.DataFrame(columns = ['Url', 'Title','Content'])
link_page = 'https://baotainguyenmoitruong.vn/'

try:
    req = requests.get(link_page)
    page_obj = BeautifulSoup(req.text, 'html.parser')

    count = 0
    while True:
        driver.find_element_by_xpath('//a[contains(text(), "Xem thêm")]').click()
        time.sleep(1000)
        count += 1
        if count == 10:
            break
except:
    print('Page not found')

list_url = []
list_title = []
list_content = []

# Extract urls, titles
try:
    for link in page_obj.find_all('h3', {'class': 'b-grid__title'}):
        # link = _link.find_all('h3', {'class': 'b-grid__title'})
        # link = _link.div
        url = link.a.attrs['href']
        print(url)
        list_url.append(url)
        req = requests.get(url)
        page_content = BeautifulSoup(req.text, 'html.parser')
        title = page_content.find('h1', {'class': 'c-detail-head__title'})
        list_title.append(title.text)
        content = page_content.find('div', {'class': 'b-maincontent'})
        res_content = ''
        for p in content.find_all('p'):
          res_content += str(p.text + '\n')
        list_content.append(res_content)

    twenty_info =  list(zip(list_url, list_title, list_content))

    for info in twenty_info:
        spiderum.loc[len(spiderum)] = info
except:
    print('There is error in num page {} about urls and titles')

spiderum.to_excel('./environment.xlsx', index=False)
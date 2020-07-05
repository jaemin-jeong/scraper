import json
from selenium import webdriver
from bs4 import BeautifulSoup

with open('config.json', 'r') as conf_f:
  config = json.load(conf_f)

chromedriver = config['DEFAULT']['CHROME_DRIVER_PATH']

URL = 'https://www.wanted.co.kr/wdlist/518/872?country=all&job_sort=job.latest_order&years=0'

driver = webdriver.Chrome(chromedriver)
driver.get(URL)
page = driver.page_source

# ul.clearfix contents
contents = driver.find_element_by_css_selector('#__next > div > div._1yHloYOs_bDD0E-s121Oaa > div._2y4sIVmvSrf6Iy63okz9Qh > div > ul')

# li tags count
positions = contents.find_elements_by_tag_name('li')

for i in range(len(positions)):
  print(f'=================== {i}번째 포지션입니다 ===================')
  position_div = contents.find_element_by_css_selector(f'#__next > div > div._1yHloYOs_bDD0E-s121Oaa > div._2y4sIVmvSrf6Iy63okz9Qh > div > ul > li:nth-child({i}) > div')
  # position_a = position_div.find_elements_by_tag_name('a')
  print(position_div)

# for i in positions:
#   position_div = i.find_element_by_css_selector(f'#__next > div > div._1yHloYOs_bDD0E-s121Oaa > div._2y4sIVmvSrf6Iy63okz9Qh > div > ul > li:nth-child({i}) > div')
#   position_a = position_div.find_elements_by_tag_name('a')
#   print(position_a)



driver.quit()


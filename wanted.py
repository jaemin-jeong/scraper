import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# # load config.json file
# with open('config.json', 'r') as conf_f:
#   config = json.load(conf_f)

def driver_init(URL):
  # chromedriver = config['DEFAULT']['CHROME_DRIVER_PATH']
  chromedriver = '/opt/WebDriver/bin/chromedriver'
  driver = webdriver.Chrome(chromedriver)
  driver.get(URL)

  try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'clearfix')))
    page = driver.page_source
  finally:
    driver.quit() # headlesshtml 적용시키면 삭제하기

  # page = driver.page_source
  soup = BeautifulSoup(page, 'lxml')
  main = soup.find('div', {'class':'_325-VFHw4I8HVltNqdJ89t'})
  entire = main.find('ul', {'class':'clearfix'})
  positions = entire.find_all('li')
  print(positions)
  return positions


def get_info(position):
    title = position.find('div', {'class': 'job-card-position'}).string
    company = position.find('div', {'class': 'job-card-company-name'}).string
    location = position.find('div', {'class': 'job-card-company-location'}).text
    link_id = position.find('a')['href']
    return {'title':title, 'company':company, 'location':location, 'link':f'https://www.wanted.co.kr{link_id}?referer_id=805818'}


def extract_jobs(positions):
  jobs_list = []
  for position in positions:
    job = get_info(position)
    jobs_list.append(job)
  return jobs_list


def get_jobs(word):
  URL = f'https://www.wanted.co.kr/search?query={word}'
  positions = driver_init(URL)
  jobs = extract_jobs(positions)
  return jobs
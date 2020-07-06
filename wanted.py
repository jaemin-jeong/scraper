import json
from selenium import webdriver
from bs4 import BeautifulSoup

# load config.json file
with open('config.json', 'r') as conf_f:
  config = json.load(conf_f)

chromedriver = config['DEFAULT']['CHROME_DRIVER_PATH']
URL = 'https://www.wanted.co.kr/wdlist/518/872?country=all&job_sort=job.latest_order&years=0'

driver = webdriver.Chrome(chromedriver)
driver.get(URL)
page = driver.page_source
driver.quit() # headlesshtml 적용시키면 삭제하기

# lxml module is faster than html.parser
soup = BeautifulSoup(page, 'lxml')
dummy = soup.find('ul', {'class': 'clearfix'})
positions = dummy.find_all('li')

def get_info(position):
    title = position.find('div', {'class': 'job-card-position'}).string
    company = position.find('div', {'class': 'job-card-company-name'}).string
    location = position.find('div', {'class': 'job-card-company-location'}).text
    link_id = position.find('a')['href']
    return {'title':title, 'company':company, 'location':location, 'link':f'https://www.wanted.co.kr{link_id}?referer_id=805818'}

def extract_jobs():
  jobs_list = []
  for position in positions:
    job = get_info(position)
    jobs_list.append(job)
  return jobs_list



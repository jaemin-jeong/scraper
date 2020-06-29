import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f'https://kr.indeed.com/jobs?q=node.js&limit={LIMIT}&radius=25'

def extract_indeed_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, 'html.parser')
  pagination = soup.find('div', {'class': 'pagination'})
  # print(pagination.prettify())

  links = pagination.find_all('a')

  pages = []
  for link in links[:-1]:
    pages.append(int(link.string))

  max_page = pages[-1]
  return max_page


def extract_indeed_jobs(last_page):
  jobs = []
  for n in range(last_page):
    result = requests.get(f'{URL}&start={n * LIMIT}')
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all('div', { 'class':'jobsearch-SerpJobCard' })

    for result in results:
      title = result.find('h2', { 'class': 'title' }).find('a')['title']
      company = result.find('span', { 'class':'company' })
      company_anchor = company.find('a')
      if company_anchor is not None:
        company = str(company_anchor.string)
      else:
        company = str(company.string)
      company = company.strip()
      print(title, company)
  return jobs
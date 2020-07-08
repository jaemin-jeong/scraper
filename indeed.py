import requests
from bs4 import BeautifulSoup

LIMIT = 50

def get_URL(str):
  return f'https://kr.indeed.com/jobs?q={str}&limit={LIMIT}&radius=25'

def get_last_page(str):
    URL = get_URL(str)
    # print(URL)
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


def extract_job(html):
    title = html.find('h2', {'class': 'title'}).find('a')['title']
    company = html.find('span', {'class': 'company'})
    company_anchor = company.find('a')
    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)
    company = company.strip()
    location = html.find('div', {'class': 'recJobLoc'})['data-rc-loc']
    job_id = html['data-jk']
    return {'title': title, 'company': company, 'location': location,
           'link': f'https://kr.indeed.com/viewjob?jk={job_id}'}


def extract_jobs(last_page, str):
    jobs = []
    URL = get_URL(str)
    for n in range(last_page):
        print(f'{n + 1}번째 페이지 출력')
        result = requests.get(URL)
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', {'class': 'jobsearch-SerpJobCard'})
        print(URL)
        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


def get_jobs(word):
  last_page = get_last_page(word)
  jobs = extract_jobs(last_page, word)
  return jobs
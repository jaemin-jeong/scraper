import requests
from bs4 import BeautifulSoup

# 한페이지에 50개씩 출력하도록 설정할 수 있기 때문에 변수에 할당
LIMIT = 50

# 검색 결과에 맞는 URL을 만들기 위해 검색어(str), 한 페이지에 몇개 출력될지(LIMIT) 변수로 작성
def get_URL(str):
  return f'https://kr.indeed.com/jobs?q={str}&limit={LIMIT}&radius=25'

# 몇 개의 페이지가 나오는지 알아내기 위한 함수
def get_last_page(str):
    URL = get_URL(str)
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find('div', {'class': 'pagination'})

    # pagination의 모든 a 태그를 불러온다
    links = pagination.find_all('a')

    pages = []

    # links 배열의 마지막까지 반복하면서
    for link in links[:-1]:
      # 요소의 내용을 뽑아낸 뒤 int형으로 변환시킨 뒤 pages 배열에 추가
        pages.append(int(link.string))

    # 마지막 페이지 출력
    print(pages)
    max_page = pages[-1]
    return max_page

# job card에서 타이틀, 회사명, 지역, 지원링크를 뽑아내는 함수
def extract_job(html):
    # 조건을 충족하는 a태그를 찾아 그 태그의 title 속성을 저장
    title = html.find('h2', {'class': 'title'}).find('a')['title']
    company = html.find('span', {'class': 'company'})
    company_anchor = company.find('a')
    # a태그가 있는 회사인 경우
    if company_anchor is not None:
        # a 태그의 문자열을 str형으로 변환시켜 저장
        company = str(company_anchor.string)
    # a태그가 없는 경우
    else:
        # company의 문자열을 str형으로 변환시켜 저장
        company = str(company.string)
    # strip()에 인자를 전달하지 않으므로 company에서 맨앞과 맨 뒤의 공백 제거
    company = company.strip()
    # 위치 저장
    location = html.find('div', {'class': 'recJobLoc'})['data-rc-loc']
    # data-jk를 붙이면 각 포지션의 지원 페이지로 넘어가기에 이를 알아내서 변수로 적용시킨다
    job_id = html['data-jk']
    return {'title': title, 'company': company, 'location': location,
           'link': f'https://kr.indeed.com/viewjob?jk={job_id}'}


def extract_jobs(last_page, str):
    jobs = []
    URL = get_URL(str)
    START = 0
    # 전체 페이지 개수만큼 반복
    for n in range(last_page):
        print(f'{URL}&start={START}')
        result = requests.get(f'{URL}&start={START}')
        START += LIMIT
        soup = BeautifulSoup(result.text, 'html.parser')
        # 페이지 내에서 class가 jobsearch-SerpJobCard인 div를 모두 찾아냄
        results = soup.find_all('div', {'class': 'jobsearch-SerpJobCard'})
        # results의 각 요소들을 extract_job의 파라미터로 넘겨서 실행
        for result in results:
            # 타이틀, 회사명, 지역, 지원링크 정보를 담은 객체를 job에 저장
            job = extract_job(result)
            # jobs 리스트에 job 객체 저장
            jobs.append(job)

    return jobs


def get_jobs(word):
  last_page = get_last_page(word)
  # 마지막 페이지와 검색어를 파라미터로 넣어 실행
  jobs = extract_jobs(last_page, word)
  return jobs
from flask import Flask, render_template, request, redirect, send_file
import logging

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        print(path.dirname( path.dirname( path.abspath(__file__) ) ))
        sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
        from indeed import get_jobs as id_get_jobs
        from wanted import get_jobs as wt_get_jobs
        from exporter import save_to_file
    else:
        from ..indeed import get_jobs as id_get_jobs
        from ..wanted import get_jobs as wt_get_jobs
        from ..exporter import save_to_file

app = Flask('index')

db = {}

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/report')
def report():
  word = request.args.get('word')
  if word:
    # 대소문자 통일하기 위해 입력받은 단어를 소문자로 변환시킴
    word = word.lower()
    # db에 word와 동일한 게 있는지 확인하기 위해 변수 선언 및 할당
    existingJobs = db.get(word)
    # existingJobs이 true면 jobs에 해당 값을 할당
    if existingJobs:
      jobs = existingJobs
    # existingJobs이 false면 id_get_jobs(), wt_get_jobs()를 통해 jobs에 값을 할당
    else:
      jobs = id_get_jobs(word)
      jobs.append(wt_get_jobs(word))
      db[word] = jobs
  else:
    return redirect('/')
  return render_template('report.html', 
    searching_by=word,
    resultsNumber=len(jobs),
    jobs=jobs,
  )

@app.route('/export')
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file('job.csv')
  except Exception as e:
    logger = logging.getLogger('GET LOGGER')
    logger.error('Failed to do something: ' + str(e))
    return redirect('/')

# @app.route('/contact')
# def contact():
#   return 'contact me!'

# @app.route('/<username>')
# def username(username):
#   return f'Hello your name is {username}!'

app.run(host='localhost')
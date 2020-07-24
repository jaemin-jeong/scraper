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
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = id_get_jobs(word)
      if wt_get_jobs(word):
        jobs = jobs + wt_get_jobs(word)
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

app.run(host='localhost')
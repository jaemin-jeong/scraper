from flask import Flask, render_template, request

app = Flask('scrapper')

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/contact')
def contact():
  return 'contact me!'

@app.route('/<username>')
def username(username):
  return f'Hello your name is {username}!'

@app.route('/report')
def report():
  word = request.args.get('word')
  return render_template('report.html', searching_by=word)
  

app.run(host='localhost')
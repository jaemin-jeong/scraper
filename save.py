import csv

def save_to_file(jobs):
  file = open('jobs.csv', mode='w')
  writer = csv.writer(file)
  for job in jobs:
    writer.writerow(list(job.values()))

def append_to_file(jobs):
  file = open('jobs.csv', 'a', newline='')
  writer = csv.writer(file)
  for job in jobs:
    writer.writerow(list(job.values()))
from indeed import get_jobs as get_indeed_jobs
from wanted import get_jobs as get_wanted_jobs
from save import save_to_file, append_to_file

indeed_jobs = get_indeed_jobs()
wanted_jobs = get_wanted_jobs()

save_to_file(indeed_jobs)
append_to_file(wanted_jobs)
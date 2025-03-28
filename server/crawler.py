from jobsites.jumpit import scrape_jumpit_jobs
from jobsites.zighang import scrape_zighang_frontend_jobs
from jobsites.jobkorea import scrape_jobkorea_frontend_jobs
from jobsites.wanted import scrape_wanted_frontend_jobs

from utils.normalize import normalize_jobs, deduplicate_jobs

def collect_all_jobs():
  jobs = []
  jobs += scrape_jumpit_jobs()
  jobs += scrape_zighang_frontend_jobs()
  jobs += scrape_jobkorea_frontend_jobs()
  jobs += scrape_wanted_frontend_jobs()

  jobs = normalize_jobs(jobs)
  jobs = deduplicate_jobs(jobs)

  return jobs

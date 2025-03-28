from jobsites.jumpit import scrape_jumpit_jobs
from jobsites.zighang import scrape_zighang_frontend_jobs
from jobsites.jobkorea import scrape_jobkorea_frontend_jobs

def collect_all_jobs():
  return scrape_jumpit_jobs() + scrape_zighang_frontend_jobs() +  scrape_jobkorea_frontend_jobs()

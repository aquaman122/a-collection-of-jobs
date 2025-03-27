from jobsites.jumpit import scrape_jumpit_jobs

def collect_all_jobs():
    all_jobs = []
    all_jobs.extend(scrape_jumpit_jobs())
    return all_jobs
from crawler import collect_all_jobs
from supabase_client import save_to_supabase

if __name__ == "__main__":
  jobs = collect_all_jobs()
  save_to_supabase(jobs)
from crawler import collect_all_jobs
from supabase_client import upload_to_supabase_and_filter_new

if __name__ == "__main__":
  jobs = collect_all_jobs()
  new_jobs = upload_to_supabase_and_filter_new(jobs)

  print(f"오늘 새로 추가된 공고 {len(new_jobs)}개:")
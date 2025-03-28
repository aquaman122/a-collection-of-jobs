import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def deduplicate_jobs(jobs: list[dict]) -> list[dict]:
  job_map = {}
  for job in jobs:
    job_map[job["link"]] = job
  return list(job_map.values())

# ✅ Supabase 저장 함수
def save_to_supabase(jobs: list[dict]):
  jobs = deduplicate_jobs(jobs)

  if not jobs:
    print("✅ 저장할 데이터 없음")
    return

  try:
    res = supabase.table("job_posts").upsert(jobs, on_conflict=["link"]).execute()
    print("✅ 저장 완료:", len(res.data))
  except Exception as e:
    print("❌ 저장 실패:", e)
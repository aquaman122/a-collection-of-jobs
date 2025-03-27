import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_TABLE = "job_posts"

def upload_to_supabase_and_filter_new(jobs):
  headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
  }

  # 모든 link 조회 (limit으로 수 제한)
  query = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?select=link&limit=10000"
  existing = requests.get(query, headers=headers)

  if existing.status_code != 200:
    return []

  existing_links = {item["link"] for item in existing.json()}

  new_jobs = [job for job in jobs if job["link"] not in existing_links]
  update_jobs = [job for job in jobs if job["link"] in existing_links]

  if new_jobs:
    res = requests.post(
      f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
      headers=headers,
      json=new_jobs
    )

  for job in update_jobs:
    update_url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?link=eq.{job['link']}"
    res = requests.patch(update_url, headers=headers, json=job)

  return new_jobs
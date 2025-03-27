import os
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

def upload_to_supabase(job_list):
  headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
  }
  res = requests.post(
    f"{SUPABASE_URL}/rest/v1/job_posts",
    headers=headers,
    json=job_list
  )
  print(res.status_code, res.text)
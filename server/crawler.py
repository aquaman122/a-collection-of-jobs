import datetime
from supabase_client import upload_to_supabase

def get_fake_jobs():
  today = datetime.date.today().isoformat()
  return [
    {
      "title": "프론트엔드 개발자 (React)",
      "company": "점핏",
      "link": "httpshttps://jumpit.saramin.co.kr/positions?jobCategory=2&sort=reg_dt",
      "source": "jumpit",
      "posted_date": today,
    },
  ]
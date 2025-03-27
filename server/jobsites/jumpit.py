from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_TABLE = "job_posts"

def scrape_jumpit_jobs():
  jobs = []
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://jumpit.saramin.co.kr/positions?jobCategory=2&sort=reg_dt")
    
    print("스크롤 전체 공고 로드 중..")
    prev_height = 0
    for _ in range(10):
      page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
      page.wait_for_timeout(1500)
      curr_height = page.evaluate("document.body.scrollHeight")
      if curr_height == prev_height:
        break
      prev_height = curr_height

    try:
      print("셀렉터 대기 중.")
      page.wait_for_selector("div.sc-d609d44f-0", timeout=10000) 
    except Exception as e:
      print("셀렉터 대기 실패", e)
      browser.close()
      return []

    job_cards = page.locator("div.sc-d609d44f-0")
    count = job_cards.count()
    print(f"총 {count}개의 공고 감지")

    for i in range(count):
        card = job_cards.nth(i)
        try:
          title = "Unknown"
          if card.locator("h2.position_card_info_title").is_visible():
            title = card.locator("h2.position_card_info_title").inner_text()

          company = "Unknown"
          company_el = card.locator("div.dyMWAC span")
          if company_el.count() > 0:
            company = company_el.first.inner_text(timeout=2000)

          # 기술 스택 리스트
          skill_spans = card.locator("ul.iFMgIl li span")
          skill_list = [skill_spans.nth(j).inner_text(timeout=2000) for j in range(skill_spans.count())]

          # 위치 & 경력 정보
          detail_spans = card.locator("ul.cdeuol li")
          details = [detail_spans.nth(j).inner_text(timeout=2000) for j in range(detail_spans.count())]

          link = card.locator("a").first.get_attribute("href")
          if link and not link.startswith("http"):
              link = f"https://jumpit.saramin.co.kr{link}"

          jobs.append({
            "title": title.strip(),
            "company": company.strip(),
            "skills": skill_list,
            "details": details,
            "link": link,
            "source": "jumpit",
            "posted_date": datetime.today().date().isoformat(),
          })
        except Exception as e:
          print(f"⚠️ 크롤링 오류: [{i+1}/{count}]:", e)
          continue

    browser.close()
  return jobs

def upload_to_supabase_and_filter_new(jobs):
  today = datetime.today().date().isoformat()
  yesterday = (datetime.today() - timedelta(days=1)).date().isoformat()

  headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
  }

  query = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?select=link,posted_date&or=(posted_date.eq.{yesterday},posted_date.eq.{today})"
  existing = requests.get(query, headers=headers)

  if existing.status_code != 200:
    print("조회 실패 supabase", existing.text)
    return []

  existing_links = {item["link"] for item in existing.json()}
  new_jobs = [job for job in jobs if job["link"] not in existing_links]

  if new_jobs:
      res = requests.post(
        f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
        headers=headers,
        json=new_jobs
      )
      if res.status_code not in [200, 201]:
        print("❌ Supabase 저장 실패:", res.text)
      else:
        print(f"✅ Supabase에 {len(new_jobs)}개 저장 완료")
  else:
    print("📭 새로운 공고 없음")

  return new_jobs

if __name__ == "__main__":
  job_list = scrape_jumpit_jobs()
  print(f"총 {len(job_list)}개 크롤링 완료")

  for job in job_list:
    print("📝", job["title"], "|", job["company"], "|", job.get("link"))

  new_jobs = upload_to_supabase_and_filter_new(job_list)
  print(f"🆕 오늘 새로 추가된 공고 {len(new_jobs)}개:")
  for job in new_jobs:
    print("-", job["title"], "|", job["company"])
from playwright.sync_api import sync_playwright
from datetime import datetime
from bs4 import BeautifulSoup

def scrape_wanted_frontend_jobs():
  jobs = []

  with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    page = context.new_page()

    page.goto("https://www.wanted.co.kr/search?query=프론트엔드&tab=position", timeout=60000)
    page.wait_for_timeout(5000)

    for _ in range(5):
      page.mouse.wheel(0, 4000)
      page.wait_for_timeout(1500)

    html = page.content()

  soup = BeautifulSoup(html, 'html.parser')

  job_cards = soup.select('a[data-position-id]')

  seen_links = set()

  for card in job_cards:
    try:
      title_el = card.select_one("strong")
      company_el = card.select_one("span")

      title = title_el.text.strip() if title_el else "unKnown"
      company = company_el.text.strip() if company_el else "unKnown"
      link = "https://www.wanted.co.kr" + card["href"]

      if not title or not company:
        continue

      seen_links.add(link)

      job_data = {
        "title": title,
        "company": company,
        "details": {
          "summary": "unKnown",
          "tech_stack": [],
        },
        "location": "unKnown",
        "career": "unKnown",
        "link": link,
        "source": "wanted",
        "posted_date": datetime.today().date().isoformat()
      }

      jobs.append(job_data)

    except Exception as e:
      print("⚠️ 에러:", e)
      continue

  print(f"원티드 프론트엔드 공고 {len(jobs)}건 크롤링 완료")
  return jobs
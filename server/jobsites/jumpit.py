from playwright.sync_api import sync_playwright
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def scrape_jumpit_jobs():
  jobs = []
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://jumpit.saramin.co.kr/positions?jobCategory=2&sort=reg_dt")
    
    prev_height = 0
    for _ in range(10):
      page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
      page.wait_for_timeout(1500)
      curr_height = page.evaluate("document.body.scrollHeight")
      if curr_height == prev_height:
        break
      prev_height = curr_height

    try:
      page.wait_for_selector("div.sc-d609d44f-0", timeout=10000) 
    except Exception as e:
      browser.close()
      return []

    job_cards = page.locator("div.sc-d609d44f-0")
    count = job_cards.count()
    print(f"점핏 총 {count}개의 공고 감지")

    for i in range(count):
        card = job_cards.nth(i)
        try:
          title = "Unknown"
          if card.locator("h2.position_card_info_title").is_visible():
            title = card.locator("h2.position_card_info_title").inner_text()

          company = "Unknown"
          try:
            company_el = card.locator("div[class^='sc-'][class*='-2'] span").first
            company = company_el.inner_text(timeout=1000).strip()
          except Exception as e:
            print(f"⚠️ 회사 정보 로딩 실패: {e}")

          # 위치 & 경력 정보
          detail_spans = card.locator("ul.cdeuol li")
          details = []
          for j in range(detail_spans.count()):
            try:
              text = detail_spans.nth(j).inner_text(timeout=2000).strip()
              details.append(text)
            except:
              continue

          location = details[0] if len(details) > 0 else None
          career = details[1] if len(details) > 1 else None

          link = card.locator("a").first.get_attribute("href")
          if link and not link.startswith("http"):
              link = f"https://jumpit.saramin.co.kr{link}"

          job_data = {
            "title": title.strip(),
            "company": company.strip(),
            "details": details if details else [],
            "location": location,
            "career": career,
            "link": link,
            "source": "jumpit",
            "posted_date": datetime.today().date().isoformat(),
          }

          jobs.append(job_data)

        except Exception as e:
          print(f"⚠️ 크롤링 오류: [{i+1}/{count}]:", e)
          continue

    print(f"점핏 프론트엔드 공고 {len(jobs)}건 크롤링 완료")
  return jobs
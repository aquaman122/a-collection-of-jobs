import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_jobkorea_frontend_jobs():
  jobs = []

  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
  }

  url = "https://www.jobkorea.co.kr/Search/?stext=프론트엔드&tabType=recruit"
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, "html.parser")

  job_cards = soup.select("article.list-item")

  for card in job_cards:
    try:
      title_el = card.select_one("a.information-title-link")
      company_el = card.select_one("a.corp-name-link")

      if not title_el or not company_el:
        continue

      title = title_el.text.strip()
      company = company_el.text.strip()
      link = title_el["href"]
      if not link.startswith("http"):
        link = "https://www.jobkorea.co.kr" + link

      location = ""
      career = ""
      info_tags = card.select("ul.chip-information-group li.chip-information-item")
      for tag in info_tags:
        text = tag.text.strip()
        if "신입" in text or "경력" in text:
          career = text
        elif (
          "·" not in text and
          "등록일" not in text and
          "마감일" not in text and
          not text.startswith("D-")
        ):
          location = text

      job_data = {
        "title": title,
        "company": company,
        "details": [],
        "location": location,
        "career": career,
        "link": link,
        "source": "jobkorea",
        "posted_date": datetime.today().date().isoformat()
      }

      jobs.append(job_data)

    except Exception as e:
      print(f"크롤링 중 오류 발생: {e}")
      continue

  print(f"잡코리아 프론트엔드 공고 {len(jobs)}건 크롤링 완료")
  return jobs
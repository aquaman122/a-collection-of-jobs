import requests
from datetime import datetime

def scrape_zighang_frontend_jobs():
  jobs = []

  url = "https://api.zighang.com/api/recruitment/filter/v4"
  params = {
    "page": 0,
    "size": 100,
    "isOpen": "true",
    "sortCondition": "UPLOAD",
    "orderBy": "DESC",
    "recJobMajorCategory": "IT개발_데이터",
    "careers": "ZERO,ONE,TWO,THREE,FOUR,FIVE,SIX,SEVEN,EIGHT,NINE,TEN,IRRELEVANCE"
  }

  try:
    res = requests.get(url, params=params)
    res.raise_for_status()
    data = res.json()

    recruitments = data.get("recruitments", {}).get("recruitmentSimpleList", [])

    count = 0
    for item in recruitments:
      jobs_list = item.get("recruitmentJobs", {})
      it_jobs = jobs_list.get("IT개발_데이터", [])

      if "프론트엔드" not in it_jobs:
        continue

      job_data = {
        "title": item.get("title", "Unknown"),
        "company": item.get("companyName", "Unknown"),
        "details": [],
        "location": " / ".join([str(addr) for addr in item.get("recruitmentAddress", [])]),
        "career": ", ".join(item.get("careers", [])) or None,
        "link": item.get("shortenedUrl", f"https://zighang.com/recruitment/{item.get('recruitmentUid')}"),
        "source": "zighang",
        "posted_date": datetime.today().date().isoformat(),
      }

      jobs.append(job_data)
      count += 1

    print(f"직행 프론트엔드 공고 {count}건 크롤링 완료")

  except Exception as e:
    print("API 요청 또는 파싱 중 오류:", e)
    return []

  return jobs
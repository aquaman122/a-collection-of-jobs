def normalize_career(raw: str) -> str:
  if not raw or raw.lower() in ["unknown", "미지정"]:
    return "미지정"

  raw = raw.replace("경력", "").replace("↑", " 이상").strip()

  mapping = {
    "ZERO": "신입",
    "ONE": "1년 이상",
    "TWO": "2년 이상",
    "THREE": "3년 이상",
    "FOUR": "4년 이상",
    "FIVE": "5년 이상",
    "SIX": "6년 이상",
    "SEVEN": "7년 이상",
    "EIGHT": "8년 이상",
    "NINE": "9년 이상",
    "TEN": "10년 이상",
    "IRRELEVANCE": "무관"
  }

  if "," in raw:
    parts = raw.split(",")
    return ", ".join([mapping.get(p.strip(), p.strip()) for p in parts])

  return mapping.get(raw.strip(), raw.strip())


def normalize_location(raw: str) -> str:
  if not raw or raw.lower() in ["unknown", "unKnown"]:
    return "미지정"

  raw = raw.strip().upper()

  mapping = {
    "SEOUL": "서울",
    "GYEONGGI": "경기",
    "INCHEON": "인천",
    "BUSAN": "부산",
    "DAEGU": "대구",
    "GWANGJU": "광주",
    "DAEJEON": "대전",
    "ULSAN": "울산",
    "SEJONG": "세종",
    "GANGWON": "강원",
    "CHUNGBUK": "충북",
    "CHUNGNAM": "충남",
    "JEONBUK": "전북",
    "JEONNAM": "전남",
    "GYEONGBUK": "경북",
    "GYEONGNAM": "경남",
    "JEJU": "제주",
  }

  return mapping.get(raw, raw)

def normalize_details(raw) -> list:
  if not raw:
    return []
  if isinstance(raw, str):
    return [raw.strip()]
  return [str(r).strip() for r in raw if r]

def normalize_job(job: dict) -> dict:
  job["career"] = normalize_career(job.get("career"))
  job["location"] = normalize_location(job.get("location"))
  job["details"] = normalize_details(job.get("details"))
  return job

def normalize_jobs(jobs: list[dict]) -> list[dict]:
  return [normalize_job(job) for job in jobs]

def deduplicate_jobs(jobs: list[dict]) -> list[dict]:
  job_map = {}
  for job in jobs:
    job_map[job["link"]] = job
  return list(job_map.values())
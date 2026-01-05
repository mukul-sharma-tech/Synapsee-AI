# //working
# import os
# import requests
# from ddgs import DDGS
# from dotenv import load_dotenv

# # ================== SETUP ==================
# load_dotenv()

# JINA_API_KEY = os.getenv("JINA_API_KEY")
# if not JINA_API_KEY:
#     raise ValueError("Please set JINA_API_KEY in .env")

# HEADERS = {
#     "Authorization": f"Bearer {JINA_API_KEY}",
#     "Accept": "text/plain"
# }

# # ================== INPUT ==================
# product = input("Enter product name: ")
# region = input("Enter region (optional): ")

# # ================== DUCKDUCKGO SEARCH ==================
# queries = [
#     f"{product} complaints site:reddit.com",
#     f"{product} problems review",
#     f"{product} missing features",
# ]

# urls = []

# print("\n🔍 DuckDuckGo Results:\n")

# with DDGS() as ddgs:
#     for q in queries:
#         print(f"➡️ Query: {q}")
#         for r in ddgs.text(q, max_results=3):
#             url = r.get("href")
#             title = r.get("title")
#             if url:
#                 urls.append(url)
#                 print("   •", title)
#                 print("     ", url)

# # ================== JINA FETCH ==================
# def fetch_with_jina(url):
#     try:
#         jina_url = f"https://r.jina.ai/{url}"
#         res = requests.get(jina_url, headers=HEADERS, timeout=20)
#         if res.status_code == 200:
#             return res.text
#         else:
#             return f"[ERROR {res.status_code}] {res.text[:300]}"
#     except Exception as e:
#         return f"[FETCH FAILED] {e}"

# # ================== OUTPUT RAW DATA ==================
# print("\n📥 RAW CONTENT EXTRACTED VIA JINA\n")
# print("=" * 100)

# for i, u in enumerate(urls, 1):
#     print(f"\n🧾 SOURCE {i}")
#     print("URL:", u)
#     print("-" * 100)
#     content = fetch_with_jina(u)
#     print(content[:6000])   # limit output
#     print("\n" + "=" * 100)



# limit
# jira.py  — TEST PHASE LIMITED EXTRACTION

# import os
# import requests
# from ddgs import DDGS
# from dotenv import load_dotenv

# # ================== SETUP ==================
# load_dotenv()

# JINA_API_KEY = os.getenv("JINA_API_KEY")
# if not JINA_API_KEY:
#     raise ValueError("Please set JINA_API_KEY in .env")

# HEADERS = {
#     "Authorization": f"Bearer {JINA_API_KEY}",
#     "Accept": "text/plain"
# }

# MAX_RESULTS_PER_QUERY = 2
# MAX_TOTAL_URLS = 5
# MAX_CHARS_PER_PAGE = 1500

# # ================== INPUT ==================
# product = input("Enter product name: ").strip()
# region = input("Enter region (optional): ").strip()

# # ================== DUCKDUCKGO SEARCH ==================
# queries = [
#     f"{product} complaints site:reddit.com",
#     f"{product} problems review",
#     f"{product} missing features",
# ]

# urls = []

# print("\n🔍 DuckDuckGo Results:\n")

# with DDGS() as ddgs:
#     for q in queries:
#         if len(urls) >= MAX_TOTAL_URLS:
#             break

#         print(f"➡️ Query: {q}")
#         count = 0

#         for r in ddgs.text(q, max_results=MAX_RESULTS_PER_QUERY):
#             if len(urls) >= MAX_TOTAL_URLS:
#                 break

#             url = r.get("href")
#             title = r.get("title")

#             if url and url not in urls:
#                 urls.append(url)
#                 count += 1
#                 print("   •", title)
#                 print("     ", url)

# # ================== JINA FETCH ==================
# def fetch_with_jina(url):
#     try:
#         jina_url = f"https://r.jina.ai/{url}"
#         res = requests.get(jina_url, headers=HEADERS, timeout=20)

#         if res.status_code == 200:
#             text = res.text.strip()
#             return text[:MAX_CHARS_PER_PAGE]
#         else:
#             return f"[ERROR {res.status_code}] {res.text[:300]}"

#     except Exception as e:
#         return f"[FETCH FAILED] {e}"

# # ================== OUTPUT RAW DATA ==================
# print("\n📥 RAW CONTENT (LIMITED – TEST PHASE)\n")
# print("=" * 100)

# for i, u in enumerate(urls, 1):
#     print(f"\n🧾 SOURCE {i}")
#     print("URL:", u)
#     print("-" * 100)

#     content = fetch_with_jina(u)
#     print(content)

#     print("\n" + "=" * 100)

# print("\n✅ Test-phase extraction complete")



# # json
# import os
# import requests
# import re
# import json
# from ddgs import DDGS
# from dotenv import load_dotenv

# # ================== SETUP ==================
# load_dotenv()

# JINA_API_KEY = os.getenv("JINA_API_KEY")
# if not JINA_API_KEY:
#     raise ValueError("Please set JINA_API_KEY in .env")

# HEADERS = {
#     "Authorization": f"Bearer {JINA_API_KEY}",
#     "Accept": "text/plain"
# }

# MAX_SOURCES = 5   # test phase limit

# PAIN_KEYWORDS = [
#     "problem", "issue", "drain", "fail", "slow",
#     "disconnect", "crash", "poor", "bad", "complaint"
# ]

# # ================== INPUT ==================
# product = input("Enter product name: ").strip()

# # ================== SEARCH ==================
# queries = [
#     f"{product} common problems",
#     f"{product} complaints review",
#     f"{product} missing features"
# ]

# urls = []

# with DDGS() as ddgs:
#     for q in queries:
#         for r in ddgs.text(q, max_results=5):
#             url = r.get("href")
#             if not url:
#                 continue
#             if "reddit.com" in url:      # 🔑 skip Reddit
#                 continue
#             if url not in urls:
#                 urls.append(url)
#             if len(urls) >= MAX_SOURCES:
#                 break
#         if len(urls) >= MAX_SOURCES:
#             break

# # ================== JINA FETCH ==================
# def fetch_with_jina(url):
#     try:
#         jina_url = f"https://r.jina.ai/{url}"
#         res = requests.get(jina_url, headers=HEADERS, timeout=20)
#         if res.status_code == 200:
#             return res.text
#     except:
#         pass
#     return None

# # ================== EXTRACT PAIN POINTS ==================
# def extract_pain_points(text):
#     sentences = re.split(r"[.\n]", text)
#     points = []
#     for s in sentences:
#         s_clean = s.strip()
#         if len(s_clean) < 40:
#             continue
#         for kw in PAIN_KEYWORDS:
#             if kw in s_clean.lower():
#                 points.append(s_clean)
#                 break
#     return list(set(points))[:8]   # limit per source

# # ================== FINAL JSON ==================
# final_data = {
#     "product": product,
#     "sources": []
# }

# for url in urls:
#     content = fetch_with_jina(url)
#     if not content:
#         continue

#     pain_points = extract_pain_points(content)

#     if pain_points:
#         final_data["sources"].append({
#             "url": url,
#             "pain_points": pain_points
#         })

# # ================== OUTPUT ==================
# print(json.dumps(final_data, indent=2))


# json
import os
import requests
import re
import json
from ddgs import DDGS
from dotenv import load_dotenv

# ================== SETUP ==================
load_dotenv()

def clean_text(text: str) -> str:
    # Remove markdown images & links
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\[.*?\]\(.*?\)", "", text)

    # Remove markdown symbols
    text = re.sub(r"[*_`>#\-]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


JINA_API_KEY = os.getenv("JINA_API_KEY")
if not JINA_API_KEY:
    raise ValueError("Please set JINA_API_KEY in .env")

HEADERS = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Accept": "text/plain"
}

MAX_SOURCES = 5   # test phase limit

PAIN_KEYWORDS = [
    "problem", "issue", "drain", "fail", "slow",
    "disconnect", "crash", "poor", "bad", "complaint"
]

# ================== INPUT ==================
product = input("Enter product name: ").strip()

# ================== SEARCH ==================
queries = [
    f"{product} common problems",
    f"{product} complaints review",
    f"{product} missing features"
]

urls = []

with DDGS() as ddgs:
    for q in queries:
        for r in ddgs.text(q, max_results=5):
            url = r.get("href")
            if not url:
                continue
            if "reddit.com" in url:      # 🔑 skip Reddit
                continue
            if url not in urls:
                urls.append(url)
            if len(urls) >= MAX_SOURCES:
                break
        if len(urls) >= MAX_SOURCES:
            break

# ================== JINA FETCH ==================
def fetch_with_jina(url):
    try:
        jina_url = f"https://r.jina.ai/{url}"
        res = requests.get(jina_url, headers=HEADERS, timeout=20)
        if res.status_code == 200:
            return res.text
    except:
        pass
    return None

# ================== EXTRACT PAIN POINTS ==================
def extract_pain_points(text):
    sentences = re.split(r"[.\n]", text)
    points = []
    for s in sentences:
        s_clean = s.strip()
        if len(s_clean) < 40:
            continue
        for kw in PAIN_KEYWORDS:
            if kw in s_clean.lower():
                cleaned = clean_text(s_clean)  # ✅ fixed variable name
                if cleaned:
                    points.append(cleaned)
                break
    return list(set(points))[:8]   # limit per source

# ================== FINAL JSON ==================
final_data = {
    "product": product,
    "sources": []
}

for url in urls:
    content = fetch_with_jina(url)
    if not content:
        continue

    pain_points = extract_pain_points(content)

    if pain_points:
        final_data["sources"].append({
            "url": url,
            "pain_points": pain_points
        })

# ================== OUTPUT ==================
print(json.dumps(final_data, indent=2))

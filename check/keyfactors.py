# ================== FULL MARKET ANALYSIS SCRIPT ==================
import os
import re
import json
import requests
from ddgs import DDGS
from dotenv import load_dotenv
from google import genai

# ================== SETUP ==================
load_dotenv()

# ------------------ Clean text ------------------
def clean_text(text: str) -> str:
    # Remove markdown images & links
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\[.*?\]\(.*?\)", "", text)
    # Remove markdown symbols
    text = re.sub(r"[*_`>#\-]", " ", text)
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ------------------ Environment keys ------------------
JINA_API_KEY = os.getenv("JINA_API_KEY")
if not JINA_API_KEY:
    raise ValueError("Please set JINA_API_KEY in .env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set GEMINI_API_KEY in .env")

HEADERS = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Accept": "text/plain"
}

# ------------------ Config ------------------
MAX_SOURCES = 5  # limit sources for testing
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
            if not url or "reddit.com" in url:  # skip Reddit
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
                cleaned = clean_text(s_clean)
                if cleaned:
                    points.append(cleaned)
                break
    return list(set(points))[:8]  # limit per source

# ================== BUILD RAW DATA ==================
final_data = {"product": product, "sources": []}

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

# ================== GEMINI ANALYSIS PROMPT ==================
prompt = f"""
You are a senior product and market strategy analyst. Here is a JSON object with raw user pain points for the product "{product}":

{json.dumps(final_data, indent=2)}

Your tasks:

1. Top complaints: Identify the main problems users face.
2. Frequently requested features: Extract features users wish the product had.
3. Pain points current products don't solve: Highlight unmet needs.
4. Key feature gaps: Based on user pain points, suggest missing features or improvements.
5. Recommendations: Provide actionable insights for product improvement and unique selling points.

Provide a concise JSON output like this format:

{{
  "product": "{product}",
  "summary": {{
      "top_complaints": [],
      "requested_features": [],
      "unmet_pain_points": [],
      "feature_gaps": [],
      "recommendations": []
  }}
}}

Only include essential, actionable information suitable for a product team.
"""

# ================== SEND TO GEMINI ==================
client = genai.Client(api_key=GEMINI_API_KEY)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)


summary_json = response.text

# ================== OUTPUT ==================
print("===== RAW PAIN POINT DATA =====")
print(json.dumps(final_data, indent=2))
print("\n===== GEMINI MARKET ANALYSIS SUMMARY =====")
print(summary_json)

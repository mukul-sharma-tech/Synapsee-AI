# from google import genai
# import os
# import jsonjson
# from dotenv import load_dotenv 
# load_dotenv()

# # 👇 Set your Gemini API key
# # (Alternatively: export GEMINI_API_KEY in .env or in shell)
# API_KEY = os.getenv("GEMINI_API_KEY")
# if not API_KEY:
#     raise ValueError("Please set GEMINI_API_KEY as an environment variable")

# # Initialize client
# client = genai.Client(api_key=API_KEY)

# # ---------- Scout Output (Sample) ----------
# scout_output = {
#     "product": "Heated Jacket",
#     "region": "Manali, Himachal Pradesh",
#     "competitors": [
#         {"name": "Winter Wear for Manali", "url": "https://woollen-wear.in", "brand_type": "National"},
#         {"name": "Coatsnmore Manali", "url": "https://coatsnmore.com", "brand_type": "National"},
#         {"name": "HimalayanKraft", "url": "https://himalayankraft.in", "brand_type": "National"}
#     ],
#     "features": ["winter", "heated", "thermal"],
#     "market_saturation": "Saturated",
#     "regional_comparison": {
#         "Pune, Maharashtra": 14,
#         "Shimla, Himachal Pradesh": 16,
#         "Leh, Ladakh": 17
#     }
# }

# prompt = f"""
# You are a senior market strategy analyst. Below is raw market data for a product idea.

# Analyze the data and output:
# 1. A feasibility score (0-100)
# 2. Key product feature recommendations
# 3. A prioritized expansion plan
# 4. Suggested safe batch size for initial manufacturing
# 5. Suggested launch timing and price positioning

# Here is the data:
# {json.dumps(scout_output, indent=2)}

# Provide a clear, human‑readable strategic summary.
# """

# # 📩 Send request to Gemini‑2.5‑Flash
# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents=prompt,
#     # Optional: add temperature/other config settings
# )

# # 🖨️ Print result
# print("=== Gemini Strategic Analysis ===\n")
# print(response.text)




# ================= FULL MARKET ANALYSIS WITH GEMINI =================
import os
import re
import json
from ddgs import DDGS
from urllib.parse import urlparse
from collections import Counter
from dotenv import load_dotenv
from google import genai

# ---------------- SETUP ----------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set GEMINI_API_KEY in .env")

client = genai.Client(api_key=GEMINI_API_KEY)

# ---------------- CONFIG ----------------
BLOCKED_DOMAINS = [
    "amazon", "flipkart", "myntra", "meesho",
    "indiamart", "justdial", "alibaba",
]

FEATURE_KEYWORDS = [
    "waterproof", "usb", "battery", "heated",
    "thermal", "lightweight", "fast charging",
    "type-c", "winter", "snow"
]

PRICE_PATTERNS = [
    r"₹\s?\d+",
    r"rs\.?\s?\d+",
    r"under\s?₹?\d+",
    r"below\s?₹?\d+"
]

# ---------------- HELPERS ----------------
def extract_domain(url):
    return urlparse(url).netloc.lower()

def is_valid_competitor(url):
    domain = extract_domain(url)
    return not any(bad in domain for bad in BLOCKED_DOMAINS)

def infer_brand_type(domain, region):
    if region.lower().split()[0] in domain:
        return "Local Brand"
    elif "shop" in domain or "store" in domain:
        return "D2C Brand"
    else:
        return "National Brand"

# ---------------- SCOUT ----------------
def duckduckgo_scout(product, region, limit=6):
    queries = [
        f"buy {product} in {region}",
        f"\"{product}\" \"{region}\" price",
        f"{product} near me",
        f"{product} shop {region}",
        f"{product} winter wear {region}",
        f"{product} trekking {region}"
    ]

    competitors = []
    seen_domains = set()
    feature_hits = []
    price_signals = []

    with DDGS() as ddgs:
        for query in queries:
            results = ddgs.text(query, max_results=20)
            for r in results:
                title = r.get("title", "")
                snippet = r.get("body", "")
                url = r.get("href")
                if not title or not url:
                    continue

                domain = extract_domain(url)
                if domain in seen_domains or not is_valid_competitor(url):
                    continue

                # Feature extraction
                for f in FEATURE_KEYWORDS:
                    if f in (title + snippet).lower():
                        feature_hits.append(f)

                # Price signal extraction
                for pattern in PRICE_PATTERNS:
                    match = re.search(pattern, snippet.lower())
                    if match:
                        price_signals.append(match.group())

                competitors.append({
                    "name": title,
                    "url": url,
                    "domain": domain,
                    "brand_type": infer_brand_type(domain, region)
                })

                seen_domains.add(domain)
                if len(competitors) >= limit:
                    break
            if len(competitors) >= limit:
                break

    return competitors, feature_hits, price_signals

# ---------------- GEMINI PROMPT ----------------
def generate_gemini_prompt(product, region, competitors, features, prices):
    scout_data = {
        "product": product,
        "region": region,
        "competitors": competitors,
        "features": features,
        "market_saturation": "Saturated" if competitors else "White Space",
        "price_signals": prices
    }

    prompt = f"""
You are a senior market strategy analyst. Below is raw market data for a product idea.

Analyze the data and output:
1. A feasibility score (0-100)
2. Key product feature recommendations
3. A prioritized expansion plan
4. Suggested safe batch size for initial manufacturing
5. Suggested launch timing and price positioning

Here is the data:
{json.dumps(scout_data, indent=2)}

Provide a clear, human‑readable strategic summary.
"""
    return prompt

# ---------------- MAIN ----------------
if __name__ == "__main__":
    PRODUCT = input("Enter product name: ").strip()
    REGION = input("Enter primary region: ").strip()
    
    # Scout competitors, features, prices
    competitors, features, prices = duckduckgo_scout(PRODUCT, REGION)
    
    print("\n✅ Competitors Found:", len(competitors))
    print("✅ Features Signals:", features)
    print("✅ Price Signals:", prices)

    # Generate prompt for Gemini
    prompt = generate_gemini_prompt(PRODUCT, REGION, competitors, features, prices)
    
    # Send request to Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print("\n=== Gemini Strategic Analysis ===\n")
    print(response.text)

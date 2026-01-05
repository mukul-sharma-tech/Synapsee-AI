# from duckduckgo_search import DDGS
# from urllib.parse import urlparse

# BLOCKED_DOMAINS = [
#     "amazon", "flipkart", "myntra", "meesho",
#     "indiamart", "justdial", "alibaba",
#     "shopify", "etsy"
# ]

# def is_valid_competitor(url: str) -> bool:
#     try:
#         domain = urlparse(url).netloc.lower()
#         return not any(blocked in domain for blocked in BLOCKED_DOMAINS)
#     except:
#         return False

# def scout_competitors(product: str, region: str, limit: int = 5):
#     queries = [
#         f"buy {product} in {region}",
#         f"\"{product}\" \"{region}\" price\"",
#         f"{product} near me"
#     ]

#     competitors = []
#     seen_domains = set()

#     print(f"\n🔍 Searching competitors for: {product} in {region}\n")

#     with DDGS() as ddgs:
#         for query in queries:
#             print(f"➡️ Query: {query}")
#             results = ddgs.text(query, max_results=10)

#             for r in results:
#                 title = r.get("title")
#                 url = r.get("href")

#                 if not title or not url:
#                     continue

#                 domain = urlparse(url).netloc
#                 if domain in seen_domains:
#                     continue

#                 if is_valid_competitor(url):
#                     competitors.append({
#                         "title": title,
#                         "url": url
#                     })
#                     seen_domains.add(domain)

#                     print(f"   ✅ Found: {title}")
#                     print(f"      🌐 {url}\n")

#                 if len(competitors) >= limit:
#                     return competitors

#     return competitors


# if __name__ == "__main__":
#     PRODUCT = "Heated Jacket"
#     REGION = "Manali India"

#     competitors = scout_competitors(PRODUCT, REGION)

#     print("\n================ FINAL COMPETITORS ================\n")
#     if not competitors:
#         print("❌ No competitors found.")
#     else:
#         for i, c in enumerate(competitors, 1):
#             print(f"{i}. {c['title']}")
#             print(f"   {c['url']}\n")

# Robust DuckDuckGo Scout for Synapsee AI
# Updated to use ddgs package

from ddgs import DDGS
from urllib.parse import urlparse
import re
from collections import Counter

# ---------------- CONFIG ---------------- #

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

# ---------------- HELPERS ---------------- #

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

# ---------------- SCOUT AGENT ---------------- #

def duckduckgo_scout(product, region, limit=6):
    # Expanded queries for better coverage
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

    print(f"\n🔍 PRODUCT: {product}")
    print(f"📍 REGION: {region}")
    print("\n---------------- SEARCH START ----------------\n")

    with DDGS() as ddgs:
        for query in queries:
            print(f"➡️ Query: {query}")
            results = ddgs.text(query, max_results=20)  # increased max results

            for r in results:
                title = r.get("title", "")
                snippet = r.get("body", "")
                url = r.get("href")

                if not title or not url:
                    continue

                domain = extract_domain(url)
                if domain in seen_domains:
                    continue

                if not is_valid_competitor(url):
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

                competitor = {
                    "name": title,
                    "url": url,
                    "domain": domain,
                    "brand_type": infer_brand_type(domain, region)
                }

                competitors.append(competitor)
                seen_domains.add(domain)

                print(f"   ✅ {title}")
                print(f"      🌐 {url}")
                print(f"      🏷️ {competitor['brand_type']}\n")

                if len(competitors) >= limit:
                    break

    return competitors, feature_hits, price_signals

# ---------------- ANALYSIS ---------------- #

def analyze_market(competitors, features, prices):
    print("\n================ MARKET INTELLIGENCE ================\n")

    print(f"🏭 Competitors Found: {len(competitors)}")

    # Market saturation
    if len(competitors) == 0:
        saturation = "White Space"
    elif len(competitors) <= 2:
        saturation = "Low Competition"
    elif len(competitors) <= 5:
        saturation = "Competitive"
    else:
        saturation = "Saturated"

    print(f"📊 Market Saturation: {saturation}")

    # Feature frequency
    feature_count = Counter(features)
    if feature_count:
        print("\n🧩 Common Feature Signals:")
        for f, c in feature_count.most_common(5):
            print(f"   • {f} ({c})")
    else:
        print("\n🧩 No clear feature signals detected")

    # Pricing signals
    if prices:
        print("\n💰 Pricing Signals Found:")
        for p in set(prices):
            print(f"   • {p}")
    else:
        print("\n💰 No pricing signals detected")

# ---------------- REGION COMPARISON ---------------- #

def compare_regions(product, regions):
    print("\n================ REGION COMPARISON ================\n")

    region_scores = {}

    with DDGS() as ddgs:
        for region in regions:
            query = f"buy {product} in {region}"
            results = ddgs.text(query, max_results=20)
            domains = set()

            for r in results:
                url = r.get("href")
                if url and is_valid_competitor(url):
                    domains.add(extract_domain(url))

            region_scores[region] = len(domains)
            print(f"📍 {region}: {len(domains)} competitors")

    print("\n🚀 Expansion Opportunity Ranking:")
    for r, score in sorted(region_scores.items(), key=lambda x: x[1]):
        print(f"   • {r} (competition score: {score})")

# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    PRODUCT = "Heated Jacket"
    REGION = "Manali, Himachal Pradesh"
    EXPANSION_REGIONS = ["Shimla, Himachal Pradesh", "Leh, Ladakh", "Pune, Maharashtra"]

    competitors, features, prices = duckduckgo_scout(PRODUCT, REGION)
    analyze_market(competitors, features, prices)
    compare_regions(PRODUCT, EXPANSION_REGIONS)

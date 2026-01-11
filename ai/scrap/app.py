from flask import Flask, request, jsonify
import os
import re
import time
import requests
from dotenv import load_dotenv

# ================== SETUP ==================
load_dotenv()

JINA_API_KEY = os.getenv("JINA_API_KEY")
if not JINA_API_KEY:
    raise ValueError("Please set JINA_API_KEY in .env")

HEADERS = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Accept": "text/plain"
}

MAX_PRODUCTS = 10   # competitors per marketplace

BAD_KEYWORDS = [
    "javascript:void", "previous page", "next page", "sponsored", 
    "ad", "offer", "coupon", "kindle", "book", "edition", "author",
    "delivery", "popular", "idea", "fastest"
]

MIN_TITLE_WORDS = 2
MAX_LINE_DISTANCE = 3

# ================== FLASK APP ==================
app = Flask(__name__)

# ================== HELPER FUNCTIONS ==================
def fetch_with_jina(url, retries=2):
    jina_url = f"https://r.jina.ai/{url}"
    for _ in range(retries):
        try:
            res = requests.get(jina_url, headers=HEADERS, timeout=35)
            if res.status_code == 200:
                return res.text
        except:
            time.sleep(2)
    return None

def clean_line(text):
    text = re.sub(r"\[.*?\]\(.*?\)", "", text)  # remove markdown links
    text = re.sub(r"\s+", " ", text)  # normalize spaces
    return text.strip()

def valid_title(text):
    t = text.lower()
    if len(text.split()) < MIN_TITLE_WORDS:
        return False
    if any(bad in t for bad in BAD_KEYWORDS):
        return False
    return True

def filter_price(price_text):
    try:
        price_val = int(re.sub(r"[^\d]", "", price_text))
        return price_val if price_val > 0 else None
    except:
        return None

def extract_products(text):
    lines = [clean_line(l) for l in text.split("\n")]
    results = []

    for i, line in enumerate(lines):
        if valid_title(line):
            for j in range(i, min(i + MAX_LINE_DISTANCE + 1, len(lines))):
                price_match = re.search(r"₹[1-9][0-9,]{0,}", lines[j])
                if price_match:
                    price_val = filter_price(price_match.group())
                    if price_val:
                        results.append({
                            "title": line,
                            "price": price_match.group(),
                            "price_value": price_val
                        })
                    break
        if len(results) >= MAX_PRODUCTS:
            break

    unique = []
    seen = set()
    for r in results:
        key = (r["title"], r["price_value"])
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique

# ================== API ROUTE ==================
@app.route("/scrape", methods=["GET", "POST"])
def scrape_product():
    # Accept product from GET query param or POST JSON
    product = request.args.get("product")
    if not product and request.is_json:
        product = request.json.get("product")
    if not product:
        return jsonify({"error": "Please provide a product name"}), 400

    query = product.replace(" ", "+")
    AMAZON_URL = f"https://www.amazon.in/s?k={query}&s=exact-aware-popularity-rank&ds=v1%3AG9y7mY3p1vNiRmwHvcqLm%2BssXBXV10lC6B0gfEhILME&qid=1768154452&ref=sr_st_exact-aware-popularity-rank"
    FLIPKART_URL = f"https://www.flipkart.com/search?q={query}"

    final_data = {
        "searched_product": product,
        "marketplaces": {}
    }

    amazon_content = fetch_with_jina(AMAZON_URL)
    if amazon_content:
        final_data["marketplaces"]["amazon"] = extract_products(amazon_content)

    flipkart_content = fetch_with_jina(FLIPKART_URL)
    if flipkart_content:
        final_data["marketplaces"]["flipkart"] = extract_products(flipkart_content)

    return jsonify(final_data)

# ================== RUN APP ==================
if __name__ == "__main__":
    app.run(debug=True, port=5000)

# trend_analysis.py
import os
import csv
import json
from dotenv import load_dotenv
from google import genai  # Gemini API

load_dotenv()

# -----------------------------
# 1️⃣ Gemini Client Setup
# -----------------------------
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Please set GEMINI_API_KEY as an environment variable")

client = genai.Client(api_key=API_KEY)

# -----------------------------
# 2️⃣ Read Google Trends CSVs
# -----------------------------
def read_csv(file_path):
    data = []
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def load_trends(folder="data"):
    trends = {}
    csv_files = ["multiTimeline.csv", "geoMap.csv", "relatedEntities.csv", "relatedQueries.csv"]
    for file_name in csv_files:
        path = os.path.join(folder, file_name)
        if os.path.exists(path):
            trends[file_name.replace(".csv","")] = read_csv(path)
        else:
            trends[file_name.replace(".csv","")] = []
    return trends

# -----------------------------
# 3️⃣ Analyze Trends with Gemini
# -----------------------------
def analyze_trends(product, region):
    trends_data = load_trends("data")

    prompt = {
        "product": product,
        "region": region,
        "google_trends": trends_data
    }

    user_prompt = f"""
    You are a senior market strategy analyst.

    Analyze the following Google Trends data for a product launch:

    {json.dumps(prompt, indent=2)}

    Please provide:
    1. Feasibility score (0-100)
    2. Key product feature recommendations
    3. Suggested safe batch size for initial manufacturing
    4. Launch timing & price positioning
    5. Regional expansion plan

    Output in clear, human-readable format.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt
    )

    print("\n=== Gemini Trend Analysis ===\n")
    print(response.text)

# -----------------------------
# 4️⃣ Main Execution
# -----------------------------
if __name__ == "__main__":
    PRODUCT = input("Enter product name: ")
    REGION = input("Enter target region: ")
    analyze_trends(PRODUCT, REGION)

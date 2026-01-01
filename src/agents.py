import os
import requests
from azure.cognitiveservices.search.websearch import WebSearchClient
from azure.cognitiveservices.search.websearch.models import SafeSearch
from msrest.authentication import CognitiveServicesCredentials
import serpapi
import praw
from openai import AzureOpenAI

# API Keys
BING_KEY = os.getenv('BING_SEARCH_KEY')
SERPAPI_KEY = os.getenv('SERPAPI_KEY')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
AZURE_OPENAI_KEY = os.getenv('AZURE_OPENAI_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')

# Clients
bing_client = WebSearchClient(endpoint="https://api.bing.microsoft.com/", credentials=CognitiveServicesCredentials(BING_KEY))
serpapi_client = serpapi.Client(api_key=SERPAPI_KEY)
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET, user_agent="SynapseeAI/1.0")
openai_client = AzureOpenAI(api_key=AZURE_OPENAI_KEY, api_version="2023-12-01-preview", azure_endpoint=AZURE_OPENAI_ENDPOINT)

def agent_scout(product_type, target_region):
    # Bing Search for competitors
    query = f"buy {product_type} in {target_region} -site:amazon.com"
    search_results = bing_client.web.search(query=query, safe_search=SafeSearch.strict)
    competitors = []
    urls = []
    for result in search_results.web_pages.value[:5]:
        competitors.append(result.name)
        urls.append(result.url)
    
    # Jina Reader for features and prices
    features_prices = []
    for url in urls[:3]:
        response = requests.get(f"https://r.jina.ai/{url}")
        if response.status_code == 200:
            content = response.text
            # Extract features and prices (simplified)
            features_prices.append({"url": url, "content": content[:500]})
    
    return {"competitors": competitors, "features_prices": features_prices}

def agent_analyst(product_type):
    # SerpApi for Google Trends
    params = {
        "engine": "google_trends",
        "q": product_type,
        "date": "today 12-m",
        "api_key": SERPAPI_KEY
    }
    results = serpapi_client.search(params)
    # Analyze seasonality
    interest_over_time = results.get("interest_over_time", {})
    # Simplified: find peak
    timeline_data = interest_over_time.get("timeline_data", [])
    if timeline_data:
        peak = max(timeline_data, key=lambda x: x.get("values", [{}])[0].get("value", 0))
        when_to_market = f"Peak in {peak['date']}"
    else:
        when_to_market = "Data not available"
    
    return {"seasonality": when_to_market}

def agent_reporter(product_type):
    # Bing News for supply chain
    query = f"{product_type} supply chain issues OR strikes"
    search_results = bing_client.news.search(query=query, count=5)
    news = [article.name for article in search_results.value]
    return {"supply_chain_risks": news}

def agent_listener(product_type, target_region):
    # Reddit search
    subreddits = ["r/India", "r/technology", "r/gadgets"]  # Example
    complaints = []
    for sub in subreddits:
        subreddit = reddit.subreddit(sub)
        for submission in subreddit.search(f"{product_type} annoying OR hate OR fail", time_filter="year", limit=10):
            complaints.append(submission.title + " " + submission.selftext[:200])
    return {"user_pain_points": complaints[:10]}

def run_agents(product_type, target_region, description, max_price, age_group):
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(agent_scout, product_type, target_region): "scout",
            executor.submit(agent_analyst, product_type): "analyst",
            executor.submit(agent_reporter, product_type): "reporter",
            executor.submit(agent_listener, product_type, target_region): "listener"
        }
        
        results = {}
        for future in as_completed(futures):
            key = futures[future]
            results[key] = future.result()
    
    return results
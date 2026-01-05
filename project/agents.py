import os
import requests
import json
import praw
from serpapi import GoogleSearch
from openai import AzureOpenAI
import pandas as pd
from datetime import datetime
# In agents.py
import streamlit as st
import google.generativeai as genai
import json

class SynapseeAgents:
    def __init__(self, secrets):
        # Initialize API Keys from Streamlit Secrets
        self.bing_key = secrets["BING_SEARCH_KEY"]
        self.serpapi_key = secrets["SERPAPI_KEY"]
        self.openai_client = AzureOpenAI(
            api_key=secrets["AZURE_OPENAI_KEY"],
            api_version="2024-02-15-preview",
            azure_endpoint=secrets["AZURE_OPENAI_ENDPOINT"]
        )
        self.deployment_name = "gpt-4o" # Ensure this matches your Azure Model Name
        
        # Initialize Reddit
        self.reddit = praw.Reddit(
            client_id=secrets["REDDIT_CLIENT_ID"],
            client_secret=secrets["REDDIT_CLIENT_SECRET"],
            user_agent="Synapsee_Hackathon_Bot_v1"
        )

    # # --- AGENT A: THE SCOUT (Competitors) ---
    # def scout_competitors(self, product, region):
    #     """Finds competitors via Bing and reads features via Jina."""
    #     print(f"🕵️ Scout Agent: Searching for {product} in {region}...")
        
    #     headers = {"Ocp-Apim-Subscription-Key": self.bing_key}
    #     # Advanced query to find niche sellers, excluding big generic pages
    #     query = f'buy "{product}" in "{region}" -site:amazon.* -site:flipkart.*'
        
    #     try:
    #         response = requests.get(
    #             "https://api.bing.microsoft.com/v7.0/search",
    #             headers=headers,
    #             params={"q": query, "count": 4}
    #         )
    #         results = response.json().get("webPages", {}).get("value", [])
            
    #         competitors = []
    #         for item in results:
    #             # Use Jina to read the page content
    #             jina_url = f"https://r.jina.ai/{item['url']}"
    #             try:
    #                 # Timeout set to 4s to keep the demo fast
    #                 page_text = requests.get(jina_url, timeout=4).text[:1000] 
    #             except:
    #                 page_text = "Could not read page."
                    
    #             competitors.append({
    #                 "name": item['name'],
    #                 "url": item['url'],
    #                 "content_snippet": page_text
    #             })
    #         return competitors
    #     except Exception as e:
    #         return [{"error": str(e)}]
    
    # In agents.py

    # --- AGENT A: THE SCOUT (Jina + Bing via SerpApi) ---
    # def scout_competitors(self, product, region):
    #     print(f"🕵️ Scout Agent: Searching for {product} in {region} via Bing & Jina...")
        
    #     # 1. SEARCH: Use SerpApi to query the Bing Search Engine
    #     # This is a safe workaround if you can't find the Azure Bing Resource
    #     params = {
    #         "engine": "bing",  # We specifically ask for Bing results
    #         "q": f'buy "{product}" in "{region}" -site:amazon.* -site:flipkart.*',
    #         "api_key": self.serpapi_key,
    #         "count": 4
    #     }
        
    #     try:
    #         search = GoogleSearch(params)
    #         # SerpApi standardizes results, even from Bing
    #         results = search.get_dict().get("organic_results", [])
            
    #         competitors = []
            
    #         # 2. READ: Use Jina AI to scrape the content cleanly
    #         jina_headers = {
    #             "Authorization": f"Bearer {self.jina_key}" # Your "Jeera" API Key
    #         }
            
    #         for item in results:
    #             target_url = item.get("link")
    #             name = item.get("title")
                
    #             if not target_url: continue

    #             # Construct the Jina URL
    #             jina_endpoint = f"https://r.jina.ai/{target_url}"
                
    #             try:
    #                 # Jina turns the website into clean Markdown text
    #                 page_response = requests.get(jina_endpoint, headers=jina_headers, timeout=5)
                    
    #                 if page_response.status_code == 200:
    #                     clean_text = page_response.text[:1000] # Limit to 1000 chars
    #                 else:
    #                     clean_text = "Content protected or inaccessible."
                        
    #             except Exception as e:
    #                 clean_text = f"Read Error: {str(e)}"
                    
    #             competitors.append({
    #                 "name": name,
    #                 "url": target_url,
    #                 "content_snippet": clean_text
    #             })
    #         return competitors
            
    #     except Exception as e:
    #         return [{"error": f"Scout Failed: {str(e)}"}]


    # --- AGENT A: THE SCOUT (Gemini Grounding) ---
    def scout_competitors(self, product, region):
        print(f"🕵️ Gemini Scout: Searching Google for {product} in {region}...")
        
        # Configure Gemini (Add GOOGLE_API_KEY to secrets.toml)
        # Note: You might need to pass the key via __init__ or os.environ
        if "GOOGLE_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        else:
            return [{"error": "Missing GOOGLE_API_KEY"}]
            
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prompt specifically asking for JSON format
        prompt = f"""
        Perform a Google Search to find 4 specific competitors selling '{product}' in '{region}'.
        Ignore big marketplaces like Amazon or Flipkart; look for local dealers or D2C brands.
        
        Return the result as a strictly valid JSON list of objects.
        Do not add Markdown formatting (like ```json). Just the raw JSON string.
        
        Format:
        [
            {{"name": "Competitor Name", "url": "Website URL", "price_range": "e.g. 3000 INR", "key_feature": "Brief feature"}}
        ]
        """
        
        try:
            # Enable the Google Search Tool
            response = model.generate_content(
                prompt,
                tools='google_search_retrieval' 
            )
            
            # Clean the response to ensure it's valid JSON
            clean_json = response.text.strip().replace("```json", "").replace("```", "")
            
            return json.loads(clean_json)
            
        except Exception as e:
            return [{"error": f"Gemini Search Failed: {str(e)}"}]
        
    # --- AGENT B: THE ANALYST (Trends) ---
    def analyze_trends(self, product):
        """Fetches 12-month interest graph from Google Trends."""
        print(f"📈 Analyst Agent: Checking trends for {product}...")
        
        params = {
            "engine": "google_trends",
            "q": product,
            "location": "India", # Defaulting to India for better data density
            "api_key": self.serpapi_key
        }
        
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            timeline = results.get("interest_over_time", {}).get("timeline_data", [])
            
            data = []
            for point in timeline:
                data.append({
                    "date": point["date"],
                    "interest": int(point["values"][0]["extracted_value"])
                })
            return data
        except Exception as e:
            return []

    # --- AGENT C: THE REPORTER (News) ---
    def get_market_news(self, product):
        """Checks for supply chain risks or industry news."""
        print(f"📰 Reporter Agent: Reading news for {product}...")
        
        headers = {"Ocp-Apim-Subscription-Key": self.bing_key}
        params = {
            "q": f"{product} industry supply chain OR price shortage",
            "count": 3,
            "mkt": "en-IN"
        }
        
        try:
            response = requests.get(
                "https://api.bing.microsoft.com/v7.0/news/search",
                headers=headers,
                params=params
            )
            return response.json().get("value", [])
        except:
            return []

    # --- AGENT D: THE LISTENER (Reddit) ---
    def listen_to_users(self, product):
        """Scrapes Reddit for pain points."""
        print(f"👂 Listener Agent: Scanning Reddit for {product} complaints...")
        
        complaints = []
        try:
            # Search for "pain" keywords
            query = f'"{product}" (annoying OR hate OR fail OR expensive)'
            for post in self.reddit.subreddit("all").search(query, limit=5, sort="relevance"):
                complaints.append({
                    "title": post.title,
                    "score": post.score,
                    "url": post.url,
                    "text": post.selftext[:300]
                })
        except Exception as e:
            complaints.append({"error": str(e)})
            
        return complaints

    # --- THE BRAIN: SYNTHESIS (GPT-4o) ---
    def generate_strategy(self, user_input, scout_data, trend_data, news_data, reddit_data):
        """Compiles all data into a JSON strategy."""
        
        # Prepare context for the LLM
        context = f"""
        PRODUCT: {user_input['product']}
        REGION: {user_input['region']}
        TARGET PRICE: {user_input['price']}
        
        1. COMPETITOR DATA (Bing + Jina):
        {str(scout_data)[:2000]}
        
        2. TREND DATA (Google Trends - Peak/Low):
        {str(trend_data)[:500]}
        
        3. MARKET NEWS (Bing News):
        {str(news_data)[:1000]}
        
        4. USER COMPLAINTS (Reddit):
        {str(reddit_data)[:1000]}
        """
        
        system_prompt = """
        You are Synapsee AI, a Startup Consultant. Analyze the provided data and return a strictly valid JSON object with these keys:
        - "marketing_start_date": (String, e.g., "October 1st")
        - "raw_material_buy_date": (String, based on off-peak trends)
        - "safe_batch_size": (Integer, estimate based on demand)
        - "feasibility_score": (Integer 0-100, based on price vs competitors)
        - "key_features_to_add": (List of strings, features competitors lack but users want)
        - "expansion_regions": (List of strings, nearby cities)
        - "executive_summary": (String, a 3-sentence summary of the strategy)
        """

        try:
            response = self.openai_client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": context}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}
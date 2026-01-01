# 🧠 Synapsee AI: The Agentic Market Strategist

"Don't just launch. Launch when the world is ready."

Synapsee AI is an autonomous agentic workflow for startups that validates product ideas, predicts optimal launch windows, and creates a data-driven manufacturing roadmap using live market intelligence and user sentiment.

## 1. 🚨 The Problem

90% of startups fail, not because of bad products, but due to four "Blind Spots":

- **Bad Timing**: Launching seasonal products (e.g., Winter Jackets) in January instead of October.
- **Invisible Competitors**: Google Search often misses niche local dealers or D2C brands that dominate specific regions.
- **Inventory Risk**: Manufacturing without knowing the "Safe Batch Size," leading to dead stock.
- **Ignored Pain Points**: Building features nobody wants because they didn't read real user complaints on forums.

## 2. 💡 The Solution

Synapsee AI is a Multi-Agent Consulting System. It takes a raw product idea and a target region as input, then dispatches autonomous AI agents to scan the web, analyze competitors, listen to user complaints, and calculate unit economics.

**Inputs:**
- Product Type (e.g., "Smart Heated Jacket")
- Target Region (e.g., "Manali, India")
- Description (e.g., "Battery operated, waterproof")
- Max Unit Price (e.g., ₹3,000)

## 3. 📍 API Mapping: Where the Data Comes From

We use a specific, specialized API for each data point to ensure accuracy, speed, and legal compliance.

| Return Output | Primary API / Tool | How it Works (Logic) |
|---------------|---------------------|----------------------|
| 📅 When to Market | SerpApi (Google Trends) | Logic: Fetches 12-month interest graph. Identifies the "slope start" (approx. 45 days before peak).<br><br>Output: "Start Ads: Oct 1st. Peak: Dec 15th." |
| 🏭 Raw Material Buying | SerpApi + Azure OpenAI | Logic: GPT-4o identifies key materials (e.g., "Cotton"). SerpApi checks trends for "Cotton Price" to find the "Off-Season Dip."<br><br>Output: "Buy in June (Lowest Demand)." |
| ⚔️ Competitors | Bing Web Search API | Logic: Uses advanced operators: buy "{Product}" in "{Region}" -site:amazon.*. Finds niche local players.<br><br>Output: List of 3-5 direct rival domains. |
| 📉 Feasibility | Jina Reader + Azure OpenAI | Logic: Jina extracts pricing from competitor sites. GPT-4o compares it to user's Max Price.<br><br>Formula: If User_Price < (Avg_Rival_Price - 15%), Feasibility = High. |
| 😡 User Pain Points | Reddit API (PRAW) | Logic: Searches relevant subreddits for keywords like "annoying", "hate", "fail".<br><br>Output: "Users hate that current jackets take 3 hours to charge." |
| 📦 Safe Batch Size | Bing Search + Azure OpenAI | Logic: GPT-4o estimates TAM (Total Addressable Market) based on Region Population + Search Volume Index.<br><br>Output: "Manufacture 500 units initially." |
| 🔑 Key Factors | Jina Reader + Bing News | Logic: Scans competitor reviews. Identifies missing features.<br><br>Output: "Must include Type-C Charging to win." |
| 🗺️ Regional Expansion | SerpApi (Google Trends) + Azure OpenAI | Logic: GPT-4o analyzes the initial target region's success metrics (Feasibility Score, Search Volume Index). SerpApi is then called to compare interest trends for the product across 3-5 adjacent regions.<br><br>Output: "Top 3 expansion targets: Pune, Hyderabad, and Bangalore (in that order)." |

## 4. 🔄 The Agentic Workflow (Step-by-Step)

### Phase 1: The Request
User submits the form on the Streamlit Frontend.
Payload: {"product": "Heated Jacket", "region": "Manali", "price": 3000}

### Phase 2: Parallel Execution (The Backend)
The Azure Function triggers four agents simultaneously:

- **Agent A (The Scout)**:
  - Calls Bing Web Search to find URLs.
  - Calls Jina Reader to scrape features & prices.

- **Agent B (The Analyst)**:
  - Calls SerpApi to get the "Seasonality Curve" for the last year.

- **Agent C (The Reporter)**:
  - Calls Bing News Search to check for supply chain risks (e.g., "Textile Strike").

- **Agent D (The Listener)**:
  - Calls Reddit API (PRAW) to fetch "Customer Complaints" and "Feature Requests" from real discussions.

### Phase 3: The Synthesis (The Brain)
All JSON data is fed into Azure OpenAI (GPT-4o) with a System Prompt:
"Act as a Supply Chain Expert. Analyze this competitor data, Reddit user sentiment, and trend graph. Calculate the Safe Batch Size and Feasibility Score."

### Phase 4: Delivery
The system generates a PDF Report (using FPDF).
The Frontend displays interactive Charts (Trends) and Cards (Competitors).

## 5. 🛠️ Technical Architecture

- **Frontend**: Streamlit (Python) - User Interface.
- **Backend**: Azure Functions (Python v2 Model) - Serverless Logic.
- **Database**: Azure Cosmos DB - Stores User Reports.
- **AI Engine**: Azure OpenAI (gpt-4o) - Reasoning Core.
- **Search Engine**: Bing Search API (S1 Tier) - Web Discovery.
- **Social Engine**: Reddit API (PRAW) - Sentiment Analysis.

## 6. ⚖️ Legal & Ethical Compliance

We strictly adhere to White-Hat Data Gathering principles suitable for enterprise use:

- **No Unauthorized Scraping**: We do not use botnets or headless browsers (Selenium) to crawl private data.
- **Paid API Access**: We use Bing Search API (Enterprise License) to discover public web data legally.
- **Official Social Data**: We use the Official Reddit API (PRAW) with authentication, respecting rate limits and Terms of Service.
- **Respectful Proxies**: We use Jina Reader, which respects robots.txt.

## 7. 🚀 Installation & Setup

```bash
# 1. Clone Repo
git clone https://github.com/your-username/synapsee-ai.git

# 2. Install Dependencies
pip install -r requirements.txt
# (Ensure 'praw', 'serpapi', 'openai', 'streamlit' are in requirements.txt)

# 3. Set Keys (Env Variables or .streamlit/secrets.toml)
export BING_SEARCH_KEY="your_key"
export SERPAPI_KEY="your_key"
export AZURE_OPENAI_KEY="your_key"
export REDDIT_CLIENT_ID="your_reddit_id"
export REDDIT_CLIENT_SECRET="your_reddit_secret"

# 4. Run Locally
streamlit run app.py
```

## 👨‍💻 Team

**Event**: Microsoft Imagine Cup 2025  
**Goal**: Reducing startup failure rates through AI-driven market intelligence.
# # ================== AGENTIC MARKET ANALYSIS APP ==================
# import streamlit as st
# import os, re, json, csv, requests
# from ddgs import DDGS
# from dotenv import load_dotenv
# from google import genai
# from urllib.parse import urlparse
# from fpdf import FPDF

# # ================== SETUP ==================
# load_dotenv()
# st.set_page_config(page_title="Agentic Market Intelligence", layout="wide")

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# JINA_API_KEY = os.getenv("JINA_API_KEY")

# client = genai.Client(api_key=GEMINI_API_KEY)

# HEADERS = {
#     "Authorization": f"Bearer {JINA_API_KEY}",
#     "Accept": "text/plain"
# }

# # ================== HELPERS ==================
# def clean_text(text):
#     text = re.sub(r"\[.*?\]|\(.*?\)|[*_`>#\-]", " ", text)
#     return re.sub(r"\s+", " ", text).strip()

# def extract_domain(url):
#     return urlparse(url).netloc.lower()

# # ================== PAIN POINT AGENT ==================
# PAIN_KEYWORDS = ["problem","issue","fail","slow","drain","bad","complaint"]

# def fetch_pain_points(product):
#     urls, points = [], []
#     queries = [
#         f"{product} common problems",
#         f"{product} complaints review",
#         f"{product} missing features"
#     ]

#     with DDGS() as ddgs:
#         for q in queries:
#             for r in ddgs.text(q, max_results=5):
#                 if r.get("href") and "reddit.com" not in r["href"]:
#                     urls.append(r["href"])
#                 if len(urls) >= 5:
#                     break

#     for url in urls:
#         try:
#             res = requests.get(f"https://r.jina.ai/{url}", headers=HEADERS, timeout=15)
#             for s in re.split(r"[.\n]", res.text):
#                 if any(k in s.lower() for k in PAIN_KEYWORDS) and len(s) > 40:
#                     points.append(clean_text(s))
#         except:
#             pass

#     return list(set(points))[:10]

# # ================== COMPETITOR AGENT ==================
# BLOCKED = ["amazon","flipkart","myntra","alibaba"]

# def scout_competitors(product, region):
#     competitors = []
#     with DDGS() as ddgs:
#         for r in ddgs.text(f"buy {product} in {region}", max_results=20):
#             url = r.get("href")
#             if not url or any(b in url for b in BLOCKED):
#                 continue
#             competitors.append({
#                 "name": r.get("title"),
#                 "url": url,
#                 "domain": extract_domain(url)
#             })
#             if len(competitors) >= 6:
#                 break
#     return competitors

# # ================== GOOGLE TRENDS AGENT ==================
# def load_trends():
#     trends = {}
#     for f in ["multiTimeline","geoMap","relatedEntities","relatedQueries"]:
#         path = f"data/{f}.csv"
#         if os.path.exists(path):
#             with open(path, encoding="utf-8") as file:
#                 trends[f] = list(csv.DictReader(file))
#         else:
#             trends[f] = []
#     return trends

# # ================== PDF ==================
# def generate_pdf(text):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=10)
#     for line in text.split("\n"):
#         pdf.multi_cell(0, 8, line)
#     path = "market_report.pdf"
#     pdf.output(path)
#     return path

# # ================== UI ==================
# st.title("🧠 Agentic Market Intelligence Platform")
# st.caption("AI-driven market, demand & product feasibility analysis")

# col1, col2 = st.columns(2)

# with col1:
#     product = st.text_input("Product Name")
#     region = st.text_input("Target Region")
#     max_price = st.number_input("Max Unit Price", min_value=1)
# with col2:
#     description = st.text_area("Product Description")
#     age_group = st.selectbox("Target Age Group (Optional)", ["All","18-25","26-35","36-50","50+"])

# if st.button("Run Market Analysis") and product and region:
#     with st.spinner("Running multi-agent analysis..."):
#         pain_points = fetch_pain_points(product)
#         competitors = scout_competitors(product, region)
#         trends = load_trends()

#         agent_input = {
#             "product": product,
#             "region": region,
#             "price_limit": max_price,
#             "description": description,
#             "age_group": age_group,
#             "pain_points": pain_points,
#             "competitors": competitors,
#             "google_trends": trends
#         }

#         prompt = f"""
# You are a senior market strategy analyst.

# Analyze the following agent-generated market intelligence and produce a unified report covering:

# - When to market the product
# - Market timing & seasonality
# - User pain points & feature gaps
# - Competitor landscape
# - Supply-side feasibility
# - Manufacturing risk
# - Safe manufacturing quantity
# - Price feasibility
# - Key product factors
# - Regional expansion opportunities
# - Raw material buying timing

# DATA:
# {json.dumps(agent_input, indent=2)}

# Provide a structured, clear, business-ready report.
# """

#         response = client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=prompt
#         )

#     st.success("Analysis Complete")

#     st.subheader("📊 Market Intelligence Report")
#     st.text(response.text)

#     pdf_path = generate_pdf(response.text)
#     with open(pdf_path, "rb") as f:
#         st.download_button("⬇ Download PDF", f, file_name="market_report.pdf")



# # ================== AGENTIC MARKET ANALYSIS APP ==================
# import streamlit as st
# import os, re, json, csv, requests
# from ddgs import DDGS
# from dotenv import load_dotenv
# from google import genai
# from urllib.parse import urlparse
# from fpdf import FPDF
# from datetime import datetime

# # ================== SETUP ==================
# load_dotenv()
# st.set_page_config(
#     page_title="Agentic Market Intelligence", 
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for better UI
# st.markdown("""
# <style>
#     .main-header {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 2rem;
#         border-radius: 10px;
#         color: white;
#         margin-bottom: 2rem;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#     }
    
#     .metric-card {
#         background: white;
#         padding: 1.5rem;
#         border-radius: 8px;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#         border-left: 4px solid #667eea;
#         margin: 1rem 0;
#     }
    
#     .section-header {
#         color: #667eea;
#         font-size: 1.5rem;
#         font-weight: 600;
#         margin: 2rem 0 1rem 0;
#         padding-bottom: 0.5rem;
#         border-bottom: 2px solid #667eea;
#     }
    
#     .insight-box {
#         background: #f8f9fa;
#         padding: 1rem;
#         border-radius: 6px;
#         border-left: 3px solid #28a745;
#         margin: 0.5rem 0;
#     }
    
#     .competitor-card {
#         padding: 1rem;
#         border-radius: 6px;
#         border: 1px solid #e0e0e0;
#         margin: 0.5rem 0;
#         transition: transform 0.2s;
#     }
    
#     .competitor-card:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 4px 8px rgba(0,0,0,0.1);
#     }
    
#     .pain-point {
#         padding: 0.8rem;
#         border-radius: 6px;
#         border-left: 3px solid #ffc107;
#         margin: 0.5rem 0;
#     }
    
#     .stButton>button {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         border: none;
#         padding: 0.75rem 2rem;
#         font-size: 1.1rem;
#         border-radius: 8px;
#         font-weight: 600;
#         width: 100%;
#         transition: all 0.3s;
#     }
    
#     .stButton>button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
#     }
# </style>
# """, unsafe_allow_html=True)

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# JINA_API_KEY = os.getenv("JINA_API_KEY")

# client = genai.Client(api_key=GEMINI_API_KEY)

# HEADERS = {
#     "Authorization": f"Bearer {JINA_API_KEY}",
#     "Accept": "text/plain"
# }

# # ================== HELPERS ==================
# def clean_text(text):
#     text = re.sub(r"\[.*?\]|\(.*?\)|[*_`>#\-]", " ", text)
#     return re.sub(r"\s+", " ", text).strip()

# def extract_domain(url):
#     return urlparse(url).netloc.lower()

# # ================== PAIN POINT AGENT ==================
# PAIN_KEYWORDS = ["problem","issue","fail","slow","drain","bad","complaint"]

# def fetch_pain_points(product):
#     urls, points = [], []
#     queries = [
#         f"{product} common problems",
#         f"{product} complaints review",
#         f"{product} missing features"
#     ]

#     with DDGS() as ddgs:
#         for q in queries:
#             for r in ddgs.text(q, max_results=5):
#                 if r.get("href") and "reddit.com" not in r["href"]:
#                     urls.append(r["href"])
#                 if len(urls) >= 5:
#                     break

#     for url in urls:
#         try:
#             res = requests.get(f"https://r.jina.ai/{url}", headers=HEADERS, timeout=15)
#             for s in re.split(r"[.\n]", res.text):
#                 if any(k in s.lower() for k in PAIN_KEYWORDS) and len(s) > 40:
#                     points.append(clean_text(s))
#         except:
#             pass

#     return list(set(points))[:10]

# # ================== COMPETITOR AGENT ==================
# BLOCKED = ["amazon","flipkart","myntra","alibaba"]

# def scout_competitors(product, region):
#     competitors = []
#     with DDGS() as ddgs:
#         for r in ddgs.text(f"buy {product} in {region}", max_results=20):
#             url = r.get("href")
#             if not url or any(b in url for b in BLOCKED):
#                 continue
#             competitors.append({
#                 "name": r.get("title"),
#                 "url": url,
#                 "domain": extract_domain(url)
#             })
#             if len(competitors) >= 6:
#                 break
#     return competitors

# # ================== GOOGLE TRENDS AGENT ==================
# def load_trends():
#     trends = {}
#     for f in ["multiTimeline","geoMap","relatedEntities","relatedQueries"]:
#         path = f"data/{f}.csv"
#         if os.path.exists(path):
#             with open(path, encoding="utf-8") as file:
#                 trends[f] = list(csv.DictReader(file))
#         else:
#             trends[f] = []
#     return trends

# # ================== ENHANCED PDF ==================
# class EnhancedPDF(FPDF):
#     def __init__(self, product_name, region):
#         super().__init__()
#         self.product_name = product_name
#         self.region = region
        
#     def header(self):
#         self.set_fill_color(102, 126, 234)
#         self.rect(0, 0, 210, 40, 'F')
#         self.set_text_color(255, 255, 255)
#         self.set_font('Arial', 'B', 20)
#         self.cell(0, 15, 'Market Intelligence Report', 0, 1, 'C')
#         self.set_font('Arial', '', 12)
#         self.cell(0, 10, f'{self.product_name} | {self.region}', 0, 1, 'C')
#         self.ln(10)
        
#     def footer(self):
#         self.set_y(-15)
#         self.set_font('Arial', 'I', 8)
#         self.set_text_color(128, 128, 128)
#         self.cell(0, 10, f'Page {self.page_no()} | Generated on {datetime.now().strftime("%B %d, %Y")}', 0, 0, 'C')
    
#     def section_title(self, title):
#         self.set_font('Arial', 'B', 14)
#         self.set_text_color(102, 126, 234)
#         self.cell(0, 10, title, 0, 1, 'L')
#         self.set_draw_color(102, 126, 234)
#         self.line(10, self.get_y(), 200, self.get_y())
#         self.ln(5)
        
#     def section_content(self, text):
#         self.set_font('Arial', '', 10)
#         self.set_text_color(0, 0, 0)
#         self.multi_cell(0, 6, text)
#         self.ln(3)
    
#     def bullet_point(self, text):
#         self.set_font('Arial', '', 10)
#         self.set_text_color(0, 0, 0)
#         x_start = self.get_x()
#         self.cell(5, 6, chr(149), 0, 0)
#         self.multi_cell(0, 6, text)
#         self.set_x(x_start)

# def generate_enhanced_pdf(report_data, product, region):
#     pdf = EnhancedPDF(product, region)
#     pdf.add_page()
    
#     # Executive Summary
#     pdf.section_title('Executive Summary')
#     pdf.section_content(report_data.get('executive_summary', ''))
    
#     # Market Timing
#     pdf.section_title('Market Timing & Seasonality')
#     pdf.section_content(report_data.get('market_timing', ''))
    
#     # Pain Points
#     pdf.section_title('User Pain Points & Feature Gaps')
#     if 'pain_points' in report_data:
#         for point in report_data['pain_points'][:5]:
#             pdf.bullet_point(point)
#     pdf.ln(5)
    
#     # Competitor Landscape
#     pdf.section_title('Competitor Landscape')
#     pdf.section_content(report_data.get('competitor_analysis', ''))
    
#     # Feasibility Analysis
#     pdf.section_title('Supply-Side Feasibility')
#     pdf.section_content(report_data.get('feasibility', ''))
    
#     # Manufacturing
#     pdf.section_title('Manufacturing Recommendations')
#     pdf.section_content(report_data.get('manufacturing', ''))
    
#     # Pricing
#     pdf.section_title('Price Feasibility')
#     pdf.section_content(report_data.get('pricing', ''))
    
#     # Key Factors
#     pdf.section_title('Key Product Success Factors')
#     pdf.section_content(report_data.get('key_factors', ''))
    
#     # Expansion
#     pdf.section_title('Regional Expansion Opportunities')
#     pdf.section_content(report_data.get('expansion', ''))
    
#     # Raw Materials
#     pdf.section_title('Raw Material Procurement')
#     pdf.section_content(report_data.get('raw_materials', ''))
    
#     path = "market_report.pdf"
#     pdf.output(path)
#     return path

# def parse_ai_response(text):
#     """Parse AI response into structured sections"""
#     sections = {
#         'executive_summary': '',
#         'market_timing': '',
#         'pain_points': [],
#         'competitor_analysis': '',
#         'feasibility': '',
#         'manufacturing': '',
#         'pricing': '',
#         'key_factors': '',
#         'expansion': '',
#         'raw_materials': ''
#     }
    
#     current_section = None
#     lines = text.split('\n')
    
#     for line in lines:
#         line_lower = line.lower()
#         if 'executive summary' in line_lower or 'summary' in line_lower:
#             current_section = 'executive_summary'
#         elif 'market timing' in line_lower or 'seasonality' in line_lower:
#             current_section = 'market_timing'
#         elif 'pain point' in line_lower or 'feature gap' in line_lower:
#             current_section = 'pain_points'
#         elif 'competitor' in line_lower:
#             current_section = 'competitor_analysis'
#         elif 'feasibility' in line_lower or 'supply' in line_lower:
#             current_section = 'feasibility'
#         elif 'manufacturing' in line_lower:
#             current_section = 'manufacturing'
#         elif 'pric' in line_lower:
#             current_section = 'pricing'
#         elif 'key factor' in line_lower or 'success factor' in line_lower:
#             current_section = 'key_factors'
#         elif 'expansion' in line_lower or 'regional' in line_lower:
#             current_section = 'expansion'
#         elif 'raw material' in line_lower:
#             current_section = 'raw_materials'
#         elif current_section and line.strip():
#             if current_section == 'pain_points' and line.strip().startswith(('-', '•', '*')):
#                 sections[current_section].append(line.strip()[1:].strip())
#             elif current_section != 'pain_points':
#                 sections[current_section] += line + '\n'
    
#     return sections

# # ================== UI ==================
# st.markdown('<div class="main-header"><h1>🧠 Agentic Market Intelligence Platform</h1><p>AI-driven market, demand & product feasibility analysis powered by multi-agent systems</p></div>', unsafe_allow_html=True)

# # Sidebar for additional options
# with st.sidebar:
#     st.header("⚙️ Configuration")
#     st.markdown("---")
#     st.info("💡 **Tip**: Provide detailed product descriptions for better analysis")
    
#     analysis_depth = st.select_slider(
#         "Analysis Depth",
#         options=["Quick", "Standard", "Deep"],
#         value="Standard"
#     )
    
#     include_trends = st.checkbox("Include Google Trends Data", value=True)
#     include_competitors = st.checkbox("Competitor Analysis", value=True)
#     include_pain_points = st.checkbox("Pain Point Research", value=True)

# # Main form
# with st.form("analysis_form"):
#     col1, col2 = st.columns(2)

#     with col1:
#         product = st.text_input("📦 Product Name", placeholder="e.g., Wireless Earbuds")
#         region = st.text_input("🌍 Target Region", placeholder="e.g., North America, India")
#         max_price = st.number_input("💰 Max Unit Price (USD)", min_value=1, value=100)
    
#     with col2:
#         description = st.text_area("📝 Product Description", placeholder="Detailed description of your product, its features, and unique selling points...", height=100)
#         age_group = st.selectbox("👥 Target Age Group", ["All","18-25","26-35","36-50","50+"])
#         product_category = st.selectbox("🏷️ Category", ["Electronics", "Fashion", "Home & Living", "Sports", "Beauty", "Food & Beverage", "Other"])
    
#     submit_button = st.form_submit_button("🚀 Run Market Analysis")

# if submit_button and product and region:
#     progress_bar = st.progress(0)
#     status_text = st.empty()
    
#     with st.spinner("🔍 Initializing multi-agent analysis..."):
#         # Pain Points Agent
#         pain_points = []
#         if include_pain_points:
#             status_text.text("🔎 Agent 1: Researching pain points...")
#             progress_bar.progress(25)
#             pain_points = fetch_pain_points(product)
        
#         # Competitor Agent
#         competitors = []
#         if include_competitors:
#             status_text.text("🏢 Agent 2: Scouting competitors...")
#             progress_bar.progress(50)
#             competitors = scout_competitors(product, region)
        
#         # Trends Agent
#         trends = {}
#         if include_trends:
#             status_text.text("📈 Agent 3: Analyzing trends...")
#             progress_bar.progress(75)
#             trends = load_trends()
        
#         # Master Analysis Agent
#         status_text.text("🧠 Master Agent: Synthesizing insights...")
#         progress_bar.progress(90)
        
#         agent_input = {
#             "product": product,
#             "region": region,
#             "price_limit": max_price,
#             "description": description,
#             "age_group": age_group,
#             "category": product_category,
#             "pain_points": pain_points,
#             "competitors": competitors,
#             "google_trends": trends
#         }

#         prompt = f"""
# You are a senior market strategy analyst with expertise in product launches and market feasibility.

# Analyze the following agent-generated market intelligence and produce a comprehensive, structured report.

# FORMAT YOUR RESPONSE WITH CLEAR SECTIONS:

# ## Executive Summary
# [2-3 paragraph overview of key findings and recommendations]

# ## Market Timing & Seasonality
# [When to launch, seasonal factors, market readiness]

# ## User Pain Points & Feature Gaps
# [Key problems in existing solutions, unmet needs]

# ## Competitor Landscape
# [Major players, competitive positioning, market gaps]

# ## Supply-Side Feasibility
# [Manufacturing complexity, supply chain considerations]

# ## Manufacturing Recommendations
# [Safe production quantities, scaling strategy, risk factors]

# ## Price Feasibility
# [Pricing strategy, competitive pricing, profit margins]

# ## Key Product Success Factors
# [Critical elements for success, differentiation opportunities]

# ## Regional Expansion Opportunities
# [Market entry strategy, regional considerations]

# ## Raw Material Procurement
# [Sourcing strategy, timing, cost optimization]

# DATA:
# {json.dumps(agent_input, indent=2)}

# Provide specific, actionable insights with data-driven recommendations.
# """

#         response = client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=prompt
#         )
        
#         progress_bar.progress(100)
#         status_text.text("✅ Analysis Complete!")

#     st.success("🎉 Market Intelligence Report Generated Successfully!")
    
#     # Display results in tabs
#     tab1, tab2, tab3, tab4 = st.tabs(["📊 Full Report", "🔍 Pain Points", "🏢 Competitors", "📈 Trends"])
    
#     with tab1:
#         st.markdown('<div class="section-header">Market Intelligence Report</div>', unsafe_allow_html=True)
#         st.markdown(response.text)
    
#     with tab2:
#         st.markdown('<div class="section-header">Identified Pain Points</div>', unsafe_allow_html=True)
#         if pain_points:
#             for i, point in enumerate(pain_points, 1):
#                 st.markdown(f'<div class="pain-point"><strong>#{i}</strong> {point}</div>', unsafe_allow_html=True)
#         else:
#             st.info("No pain points data available")
    
#     with tab3:
#         st.markdown('<div class="section-header">Competitor Landscape</div>', unsafe_allow_html=True)
#         if competitors:
#             for comp in competitors:
#                 st.markdown(f'''
#                 <div class="competitor-card">
#                     <strong>{comp["name"]}</strong><br>
#                     <small>🌐 {comp["domain"]}</small><br>
#                     <a href="{comp["url"]}" target="_blank">Visit Site →</a>
#                 </div>
#                 ''', unsafe_allow_html=True)
#         else:
#             st.info("No competitor data available")
    
#     with tab4:
#         st.markdown('<div class="section-header">Google Trends Data</div>', unsafe_allow_html=True)
#         if trends and any(trends.values()):
#             for trend_type, data in trends.items():
#                 if data:
#                     st.subheader(trend_type.replace("_", " ").title())
#                     st.dataframe(data[:10])
#         else:
#             st.info("No trends data available. Upload CSV files to data/ folder.")
    
#     # Generate and download PDF
#     st.markdown("---")
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         parsed_data = parse_ai_response(response.text)
#         parsed_data['pain_points'] = pain_points
        
#         pdf_path = generate_enhanced_pdf(parsed_data, product, region)
        
#         with open(pdf_path, "rb") as f:
#             st.download_button(
#                 label="📥 Download Professional PDF Report",
#                 data=f,
#                 file_name=f"market_report_{product.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
#                 mime="application/pdf",
#                 use_container_width=True
#             )

# # Footer
# st.markdown("---")
# st.markdown("""
# <div style='text-align: center; color: #666; padding: 2rem;'>
#     <p>Powered by Multi-Agent AI Systems | Gemini 2.5 Flash | DuckDuckGo | Jina AI</p>
#     <p><small>© 2024 Agentic Market Intelligence Platform</small></p>
# </div>
# """, unsafe_allow_html=True)
# ================== AGENTIC MARKET ANALYSIS APP ==================
import streamlit as st
import os, re, json, csv, requests, io
from ddgs import DDGS
from dotenv import load_dotenv
from google import genai
from urllib.parse import urlparse
from fpdf import FPDF
from datetime import datetime

# ================== SETUP ==================
load_dotenv()
st.set_page_config(
    page_title="Agentic Market Intelligence", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .section-header {
        color: #667eea;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
    
    .insight-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 6px;
        border-left: 3px solid #28a745;
        margin: 0.5rem 0;
    }
    
    .competitor-card {
        padding: 1rem;
        border-radius: 6px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
        transition: transform 0.2s;
    }
    
    .competitor-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .pain-point {
        padding: 0.8rem;
        border-radius: 6px;
        border-left: 3px solid #ffc107;
        margin: 0.5rem 0;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
JINA_API_KEY = os.getenv("JINA_API_KEY")

# Initialize Client safely
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except:
    client = None

HEADERS = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Accept": "text/plain"
}

# ================== HELPERS ==================
def clean_text(text):
    text = re.sub(r"\[.*?\]|\(.*?\)|[*_`>#\-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def extract_domain(url):
    try:
        return urlparse(url).netloc.lower()
    except:
        return url

def sanitize_for_pdf(text):
    """Replace unsupported characters for FPDF (Latin-1)"""
    replacements = {
        '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
        '\u2013': '-', '\u2014': '-', '\u2022': '*', '\u2026': '...'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Remove emojis or other non-latin characters
    return text.encode('latin-1', 'replace').decode('latin-1')

# ================== PAIN POINT AGENT ==================
PAIN_KEYWORDS = ["problem","issue","fail","slow","drain","bad","complaint"]

def fetch_pain_points(product):
    urls, points = [], []
    queries = [
        f"{product} common problems",
        f"{product} complaints review",
        f"{product} missing features"
    ]

    with DDGS() as ddgs:
        for q in queries:
            for r in ddgs.text(q, max_results=5):
                if r.get("href") and "reddit.com" not in r["href"]:
                    urls.append(r["href"])
                if len(urls) >= 5:
                    break

    for url in urls:
        try:
            res = requests.get(f"https://r.jina.ai/{url}", headers=HEADERS, timeout=15)
            for s in re.split(r"[.\n]", res.text):
                if any(k in s.lower() for k in PAIN_KEYWORDS) and len(s) > 40:
                    points.append(clean_text(s))
        except:
            pass

    return list(set(points))[:10]

# ================== COMPETITOR AGENT ==================
BLOCKED = ["amazon","flipkart","myntra","alibaba"]

def scout_competitors(product, region):
    competitors = []
    with DDGS() as ddgs:
        for r in ddgs.text(f"buy {product} in {region}", max_results=20):
            url = r.get("href")
            if not url or any(b in url for b in BLOCKED):
                continue
            competitors.append({
                "name": r.get("title"),
                "url": url,
                "domain": extract_domain(url)
            })
            if len(competitors) >= 6:
                break
    return competitors

# ================== GOOGLE TRENDS AGENT ==================
def process_uploaded_trends(uploaded_files):
    trends = {
        "multiTimeline": [],
        "geoMap": [],
        "relatedEntities": [],
        "relatedQueries": []
    }
    
    # Map input keys to internal keys
    file_mapping = {
        "multiTimeline": "multiTimeline", 
        "geoMap": "geoMap", 
        "relatedEntities": "relatedEntities", 
        "relatedQueries": "relatedQueries"
    }

    for key, uploaded_file in uploaded_files.items():
        if uploaded_file is not None:
            try:
                # Read file as string
                stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
                # Skip first line usually containing category info in Google Trends exports
                content = stringio.read()
                # Simple CSV parsing
                reader = csv.DictReader(io.StringIO(content))
                trends[key] = list(reader)
            except Exception as e:
                st.warning(f"Could not parse {key}: {e}")
                
    return trends

# ================== ENHANCED PDF ==================
class EnhancedPDF(FPDF):
    def __init__(self, product_name, region):
        super().__init__()
        self.product_name = sanitize_for_pdf(product_name)
        self.region = sanitize_for_pdf(region)
        # CRITICAL FIX: Enable Auto Page Break to prevent cutting off text
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        self.set_fill_color(102, 126, 234)
        self.rect(0, 0, 210, 40, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 20)
        self.cell(0, 15, 'Market Intelligence Report', 0, 1, 'C')
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f'{self.product_name} | {self.region}', 0, 1, 'C')
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def section_title(self, title):
        self.ln(5) # Add space before title
        self.set_font('Arial', 'B', 14)
        self.set_text_color(102, 126, 234)
        self.cell(0, 10, sanitize_for_pdf(title), 0, 1, 'L')
        self.set_draw_color(102, 126, 234)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)
        
    def section_content(self, text):
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        # Sanitize text to avoid FPDF errors
        safe_text = sanitize_for_pdf(text)
        self.multi_cell(0, 6, safe_text)
        self.ln(3)
    
    def bullet_point(self, text):
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        safe_text = sanitize_for_pdf(text)
        x_start = self.get_x()
        self.cell(5, 6, chr(149), 0, 0)
        self.multi_cell(0, 6, safe_text)
        self.set_x(x_start)

def generate_enhanced_pdf(report_data, product, region):
    pdf = EnhancedPDF(product, region)
    pdf.add_page()
    
    # Map sections to human readable titles
    sections_map = [
        ('executive_summary', 'Executive Summary'),
        ('market_timing', 'Market Timing & Seasonality'),
        ('pain_points', 'User Pain Points & Feature Gaps'),
        ('competitor_analysis', 'Competitor Landscape'),
        ('feasibility', 'Supply-Side Feasibility'),
        ('manufacturing', 'Manufacturing Recommendations'),
        ('pricing', 'Price Feasibility'),
        ('key_factors', 'Key Product Success Factors'),
        ('expansion', 'Regional Expansion Opportunities'),
        ('raw_materials', 'Raw Material Procurement')
    ]
    
    for key, title in sections_map:
        pdf.section_title(title)
        
        content = report_data.get(key, '')
        if key == 'pain_points' and isinstance(content, list):
            for point in content[:8]: # Limit to fit
                pdf.bullet_point(point)
        elif isinstance(content, str):
            pdf.section_content(content)
            
    # Save to temp path
    path = f"market_report_{datetime.now().strftime('%H%M%S')}.pdf"
    pdf.output(path)
    return path

def parse_ai_response(text):
    """Parse AI response into structured sections"""
    sections = {
        'executive_summary': '',
        'market_timing': '',
        'pain_points': [],
        'competitor_analysis': '',
        'feasibility': '',
        'manufacturing': '',
        'pricing': '',
        'key_factors': '',
        'expansion': '',
        'raw_materials': ''
    }
    
    current_section = None
    lines = text.split('\n')
    
    for line in lines:
        line_clean = line.strip()
        line_lower = line.lower()
        
        # Section detection logic
        if line_clean.startswith('##'):
             clean_header = line_clean.replace('#', '').strip().lower()
             if 'executive' in clean_header: current_section = 'executive_summary'
             elif 'timing' in clean_header: current_section = 'market_timing'
             elif 'pain' in clean_header: current_section = 'pain_points'
             elif 'competitor' in clean_header: current_section = 'competitor_analysis'
             elif 'feasibility' in clean_header: current_section = 'feasibility'
             elif 'manufacturing' in clean_header: current_section = 'manufacturing'
             elif 'pric' in clean_header: current_section = 'pricing'
             elif 'success' in clean_header or 'factors' in clean_header: current_section = 'key_factors'
             elif 'expansion' in clean_header: current_section = 'expansion'
             elif 'raw' in clean_header: current_section = 'raw_materials'
        
        elif current_section and line_clean:
            if current_section == 'pain_points' and line_clean.startswith(('-', '•', '*')):
                sections[current_section].append(line_clean[1:].strip())
            elif current_section != 'pain_points':
                sections[current_section] += line + '\n'
    
    return sections

def generate_demo_data(product):
    """Generates dummy data for testing"""
    pain_points = [f"Battery life of {product} is too short", "Connecting is difficult", "Too expensive for the value", "Breaks easily after 2 months", "Customer support is non-existent"]
    competitors = [{"name": "Demo Competitor A", "url": "https://example.com", "domain": "example.com"}, {"name": "Demo Competitor B", "url": "https://test.com", "domain": "test.com"}]
    trends = {"multiTimeline": [{"time": "2024-01", "value": "50"}, {"time": "2024-02", "value": "75"}], "geoMap": [], "relatedEntities": [], "relatedQueries": []}
    
    ai_text = f"""
## Executive Summary
This is a DEMO REPORT for {product}. The market shows strong indicators for disruption. Key opportunities exist in improving battery longevity and reducing latency.

## Market Timing & Seasonality
Launch in Q3 to align with holiday shopping trends. Q1 is historically slow.

## User Pain Points & Feature Gaps
- Battery drains within 2 hours
- Uncomfortable fit for long usage
- Bluetooth pairing fails often

## Competitor Landscape
The market is saturated with low-end clones. High-end market is dominated by major tech giants, leaving a gap in the mid-range affordable luxury segment.

## Supply-Side Feasibility
Components are readily available. Sourcing lithium batteries requires certification.

## Manufacturing Recommendations
Start with a small batch of 1,000 units. Use injection molding for casings.

## Price Feasibility
Recommended retail price: $49.99 - $69.99. Competitors average at $89.00.

## Key Product Success Factors
1. Battery life > 8 hours
2. Water resistance (IPX4 minimum)
3. Fast charging case

## Regional Expansion Opportunities
Focus on urban centers first. Tier-2 cities show growing demand for budget alternatives.

## Raw Material Procurement
Secure copper and silicon contracts early. Plastic casing prices are volatile.
    """
    return pain_points, competitors, trends, ai_text

# ================== STATE MANAGEMENT ==================
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'generated_pdf_path' not in st.session_state:
    st.session_state.generated_pdf_path = None

# ================== UI ==================
st.markdown('<div class="main-header"><h1>SynopseeAI</h1><p>AI-driven market, demand & product feasibility analysis powered by multi-agent systems</p></div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    with st.expander("📂 Upload Trends Data (Optional)", expanded=True):
        st.caption("Upload CSVs from Google Trends")
        f_timeline = st.file_uploader("multiTimeline.csv", type=['csv'], key="u1")
        f_geomap = st.file_uploader("geoMap.csv", type=['csv'], key="u2")
        f_entities = st.file_uploader("relatedEntities.csv", type=['csv'], key="u3")
        f_queries = st.file_uploader("relatedQueries.csv", type=['csv'], key="u4")
        
        uploaded_files_dict = {
            "multiTimeline": f_timeline,
            "geoMap": f_geomap,
            "relatedEntities": f_entities,
            "relatedQueries": f_queries
        }

    st.markdown("---")
    analysis_depth = st.select_slider("Analysis Depth", options=["Quick", "Standard", "Deep"], value="Standard")
    include_competitors = st.checkbox("Competitor Analysis", value=True)
    include_pain_points = st.checkbox("Pain Point Research", value=True)
    
    st.markdown("---")
    st.subheader("🧪 Testing")
    btn_demo = st.button("🛠️ Load Demo Data (Test Mode)")

# Main form
with st.form("analysis_form"):
    col1, col2 = st.columns(2)
    with col1:
        product = st.text_input("📦 Product Name", placeholder="e.g., Wireless Earbuds")
        region = st.text_input("🌍 Target Region", placeholder="e.g., North America, India")
        max_price = st.number_input("💰 Max Unit Price (USD)", min_value=1, value=100)
    with col2:
        description = st.text_area("📝 Product Description", placeholder="Detailed description...", height=100)
        age_group = st.selectbox("👥 Target Age Group", ["All","18-25","26-35","36-50","50+"])
        product_category = st.selectbox("🏷️ Category", ["Electronics", "Fashion", "Home", "Sports", "Beauty", "Other"])
    
    submit_button = st.form_submit_button("🚀 Run Market Analysis")

# ================== LOGIC FLOW ==================

# 1. Handle Demo Mode
if btn_demo:
    product = "Demo Smart Watch" if not product else product
    region = "Demo Region" if not region else region
    
    with st.spinner("Generating demo data..."):
        d_pain, d_comp, d_trends, d_text = generate_demo_data(product)
        st.session_state.analysis_results = {
            "product": product,
            "region": region,
            "pain_points": d_pain,
            "competitors": d_comp,
            "trends": d_trends,
            "ai_response_text": d_text
        }
        # Generate PDF immediately for demo
        parsed_data = parse_ai_response(d_text)
        parsed_data['pain_points'] = d_pain
        st.session_state.generated_pdf_path = generate_enhanced_pdf(parsed_data, product, region)
    st.rerun()

# 2. Handle Real Analysis
if submit_button and product and region:
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with st.spinner("🔍 Initializing multi-agent analysis..."):
        # Pain Points
        pain_points = []
        if include_pain_points:
            status_text.text("🔎 Agent 1: Researching pain points...")
            progress_bar.progress(25)
            pain_points = fetch_pain_points(product)
        
        # Competitors
        competitors = []
        if include_competitors:
            status_text.text("🏢 Agent 2: Scouting competitors...")
            progress_bar.progress(50)
            competitors = scout_competitors(product, region)
        
        # Trends (From Uploads)
        status_text.text("📈 Agent 3: Processing trends data...")
        progress_bar.progress(75)
        trends = process_uploaded_trends(uploaded_files_dict)
        
        # Master Analysis
        status_text.text("🧠 Master Agent: Synthesizing insights...")
        progress_bar.progress(90)
        
        agent_input = {
            "product": product, "region": region, "price": max_price,
            "desc": description, "age": age_group, "cat": product_category,
            "pain_points": pain_points, "competitors": competitors,
            "trends_summary": "User provided CSV data included in analysis context" if any(uploaded_files_dict.values()) else "No trend data"
        }

        prompt = f"""
You are a senior market strategy analyst. Analyze this market intelligence.
DATA: {json.dumps(agent_input, indent=2)}

FORMAT RESPONSE STRICTLY WITH THESE HEADERS:
## Executive Summary
## Market Timing & Seasonality
## User Pain Points & Feature Gaps
## Competitor Landscape
## Supply-Side Feasibility
## Manufacturing Recommendations
## Price Feasibility
## Key Product Success Factors
## Regional Expansion Opportunities
## Raw Material Procurement

Write detailed paragraphs for each.
"""
        if client:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            ai_text = response.text
        else:
            ai_text = "Error: Gemini API Key not found. Please check .env file."

        # SAVE TO SESSION STATE
        st.session_state.analysis_results = {
            "product": product,
            "region": region,
            "pain_points": pain_points,
            "competitors": competitors,
            "trends": trends,
            "ai_response_text": ai_text
        }
        
        # Generate PDF
        parsed_data = parse_ai_response(ai_text)
        parsed_data['pain_points'] = pain_points
        st.session_state.generated_pdf_path = generate_enhanced_pdf(parsed_data, product, region)

        progress_bar.progress(100)
        status_text.text("✅ Analysis Complete!")

# 3. Display Results (from Session State)
if st.session_state.analysis_results:
    results = st.session_state.analysis_results
    
    st.success(f"🎉 Report Ready for {results['product']}")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Full Report", "🔍 Pain Points", "🏢 Competitors", "📈 Trends"])
    
    with tab1:
        st.markdown('<div class="section-header">Market Intelligence Report</div>', unsafe_allow_html=True)
        st.markdown(results['ai_response_text'])
    
    with tab2:
        st.markdown('<div class="section-header">Identified Pain Points</div>', unsafe_allow_html=True)
        if results['pain_points']:
            for i, point in enumerate(results['pain_points'], 1):
                st.markdown(f'<div class="pain-point"><strong>#{i}</strong> {point}</div>', unsafe_allow_html=True)
        else:
            st.info("No pain points data available")
    
    with tab3:
        st.markdown('<div class="section-header">Competitor Landscape</div>', unsafe_allow_html=True)
        if results['competitors']:
            for comp in results['competitors']:
                st.markdown(f'''
                <div class="competitor-card">
                    <strong>{comp["name"]}</strong><br>
                    <small>🌐 {comp["domain"]}</small><br>
                    <a href="{comp["url"]}" target="_blank">Visit Site →</a>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("No competitor data available")
    
    with tab4:
        st.markdown('<div class="section-header">Google Trends Data</div>', unsafe_allow_html=True)
        trends_data = results.get('trends', {})
        has_data = False
        for k, v in trends_data.items():
            if v:
                has_data = True
                st.subheader(k)
                st.dataframe(v[:10])
        if not has_data:
            st.info("No CSV data uploaded.")

    # PDF Download Section
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.generated_pdf_path and os.path.exists(st.session_state.generated_pdf_path):
            with open(st.session_state.generated_pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download Professional PDF Report",
                    data=f,
                    file_name=f"market_report_{results['product'].replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>Powered by Multi-Agent AI Systems | Gemini 2.0 Flash | DuckDuckGo | Jina AI</p>
    <p><small>© 2024 Agentic Market Intelligence Platform</small></p>
</div>
""", unsafe_allow_html=True)
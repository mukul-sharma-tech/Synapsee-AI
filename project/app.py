import streamlit as st
import pandas as pd
from agents import SynapseeAgents
from fpdf import FPDF
import json

# Page Config
st.set_page_config(page_title="Synapsee AI", page_icon="🧠", layout="wide")

# Custom CSS for "Hacker Mode"
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #0078D4;
        color: white;
        height: 3em;
        font-weight: bold;
    }
    .metric-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🧠 Synapsee AI")
st.markdown("**The Agentic Market Strategist for Startups**")
st.markdown("---")

# --- SIDEBAR: INPUTS ---
with st.sidebar:
    st.header("🚀 Project Parameters")
    product = st.text_input("Product Type", "Smart Heated Jacket")
    region = st.text_input("Target Region", "Manali, India")
    price = st.number_input("Target Unit Price (₹)", min_value=100, value=3000)
    desc = st.text_area("Description", "Battery operated, waterproof, 10hr life")
    
    analyze_btn = st.button("Initialize Agents")

# --- MAIN EXECUTION ---
if analyze_btn:
    # Check for secrets
    if "BING_SEARCH_KEY" not in st.secrets:
        st.error("⚠️ API Keys missing! Please configure .streamlit/secrets.toml")
        st.stop()

    # Initialize Agents
    agents = SynapseeAgents(st.secrets)
    
    # Create Layout Columns
    col1, col2 = st.columns([1, 1])
    
    with st.status("🤖 Orchestrating Agents...", expanded=True) as status:
        
        # 1. SCOUT AGENT
        st.write("🕵️ **Scout Agent:** Hunting competitors via Bing & Jina...")
        competitors = agents.scout_competitors(product, region)
        st.write(f"✅ Found {len(competitors)} competitors.")
        
        # 2. ANALYST AGENT
        st.write("📈 **Analyst Agent:** Fetching seasonality from Google Trends...")
        trends = agents.analyze_trends(product)
        st.write("✅ Trend data acquired.")
        
        # 3. REPORTER AGENT
        st.write("📰 **Reporter Agent:** Checking supply chain news...")
        news = agents.get_market_news(product)
        
        # 4. LISTENER AGENT
        st.write("👂 **Listener Agent:** Scanning Reddit for user pain points...")
        reddit = agents.listen_to_users(product)
        
        # 5. THE BRAIN
        st.write("🧠 **The Brain:** Synthesizing final strategy...")
        user_input = {"product": product, "region": region, "price": price}
        strategy = agents.generate_strategy(user_input, competitors, trends, news, reddit)
        
        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

    # --- RESULTS DASHBOARD ---
    st.divider()
    
    # ROW 1: METRICS
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Feasibility Score", f"{strategy.get('feasibility_score', 0)}/100")
    m2.metric("Safe Batch Size", f"{strategy.get('safe_batch_size', 0)} Units")
    m3.metric("Launch Date", strategy.get("marketing_start_date", "N/A"))
    m4.metric("Buy Material", strategy.get("raw_material_buy_date", "N/A"))
    
    st.divider()

    # ROW 2: TRENDS & INSIGHTS
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("📈 Market Demand Curve")
        if trends:
            df_trends = pd.DataFrame(trends)
            df_trends['date'] = pd.to_datetime(df_trends['date'])
            st.line_chart(df_trends, x='date', y='interest', color="#00FF00")
        else:
            st.warning("No sufficient trend data found.")
            
        st.subheader("💡 Executive Summary")
        st.info(strategy.get("executive_summary", "No summary generated."))
        
        st.subheader("🔑 Critical Features (User Demands)")
        for feature in strategy.get("key_features_to_add", []):
            st.success(f"✨ {feature}")

    with c2:
        st.subheader("⚔️ Top Competitors")
        for comp in competitors:
            with st.expander(comp['name']):
                st.write(f"**URL:** {comp['url']}")
                st.caption(comp.get('content_snippet', '')[:150] + "...")
                
        st.subheader("😡 User Pain Points (Reddit)")
        for post in reddit[:3]:
            if 'title' in post:
                st.warning(f"**{post['title']}** (Score: {post['score']})")

    # --- PDF GENERATION ---
    st.divider()
    
    def create_pdf(strat, input_data):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt=f"Synapsee AI Strategy Report: {input_data['product']}", ln=True, align='C')
        
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        pdf.multi_cell(0, 10, txt=f"Region: {input_data['region']} | Target Price: INR {input_data['price']}")
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="Executive Summary", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=strat.get("executive_summary", ""))
        pdf.ln(5)
        
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="Launch Strategy", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, txt=f"Marketing Start: {strat.get('marketing_start_date')}", ln=True)
        pdf.cell(0, 10, txt=f"Material Buy: {strat.get('raw_material_buy_date')}", ln=True)
        pdf.cell(0, 10, txt=f"Safe Batch Size: {strat.get('safe_batch_size')}", ln=True)
        
        return pdf.output(dest='S').encode('latin-1')

    pdf_bytes = create_pdf(strategy, user_input)
    
    st.download_button(
        label="📄 Download Official PDF Report",
        data=pdf_bytes,
        file_name=f"Synapsee_Report_{product.replace(' ', '_')}.pdf",
        mime='application/pdf'
    )
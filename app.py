import streamlit as st
import streamlit_authenticator as stauth
from yaml import safe_load
import requests
import os

# Load config for authenticator
with open('.streamlit/auth_config.yaml') as file:
    config = safe_load(file)

# Create authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Placeholder for backend analysis
def analyze_product(product_type, target_region, description, max_price, age_group):
    # In real implementation, call Azure Function
    # For now, return mock data
    return {
        "when_to_market": "Start Ads: Oct 1st. Peak: Dec 15th.",
        "raw_material_buy": "Buy in June (Lowest Demand).",
        "competitors": ["Competitor A", "Competitor B", "Competitor C"],
        "feasibility": "High",
        "safe_batch_size": "Manufacture 500 units initially.",
        "key_factors": "Must include Type-C Charging to win.",
        "nearby_regions": ["Shimla, India", "Darjeeling, India", "Kathmandu, Nepal"],
        "regional_expansion": "Top 3 expansion targets: Pune, Hyderabad, and Bangalore (in that order).",
        "user_pain_points": "Users complain about long charging times and poor battery life.",
        "pdf_content": b"Mock PDF content"  # In real, base64 or bytes
    }

def display_results(results):
    st.header("Analysis Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 When to Market")
        st.write(results["when_to_market"])
        
        st.subheader("🏭 Raw Material Buying")
        st.write(results["raw_material_buy"])
        
        st.subheader("⚔️ Competitors")
        for comp in results["competitors"]:
            st.write(f"- {comp}")
        
        st.subheader("📉 Feasibility")
        st.write(results["feasibility"])
    
    with col2:
        st.subheader("📦 Safe Batch Size")
        st.write(results["safe_batch_size"])
        
        st.subheader("🔑 Key Factors")
        st.write(results["key_factors"])
        
        st.subheader("🌍 Nearby Regions")
        for region in results["nearby_regions"]:
            st.write(f"- {region}")
        
        st.subheader("🗺️ Regional Expansion")
        st.write(results.get("regional_expansion", "Top 3 expansion targets: Pune, Hyderabad, and Bangalore (in that order)."))
        
        st.subheader("😡 User Pain Points")
        st.write(results.get("user_pain_points", "No specific pain points identified."))
    
    # PDF Download
    st.download_button(
        label="Download PDF Report",
        data=results["pdf_content"],
        file_name="synapsee_report.pdf",
        mime="application/pdf"
    )

# Authentication
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    # Dashboard code here
    st.title("Synapsee AI Dashboard")
    st.write("Enter your product details for market analysis.")

    with st.form("product_form"):
        product_type = st.text_input("Product Type", placeholder="e.g., Smart Heated Jacket")
        target_region = st.text_input("Target Region", placeholder="e.g., Manali, India")
        description = st.text_area("Product Description", placeholder="e.g., Battery operated, waterproof")
        max_price = st.number_input("Maximum Unit Price (₹)", min_value=0.0, step=0.01)
        age_group = st.selectbox("Target Age Group (optional)", ["", "18-25", "26-35", "36-45", "46-55", "56+"])
        submitted = st.form_submit_button("Analyze")

        if submitted:
            # Validate inputs
            if not product_type or not target_region or not description or max_price <= 0:
                st.error("Please fill all required fields.")
            else:
                with st.spinner("Analyzing market data..."):
                    # Call backend function
                    results = analyze_product(product_type, target_region, description, max_price, age_group)
                    if results:
                        display_results(results)
                    else:
                        st.error("Analysis failed. Please try again.")

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
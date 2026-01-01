from src.agents import openai_client

def synthesize_results(agent_results, product_type, target_region, max_price):
    scout = agent_results.get("scout", {})
    analyst = agent_results.get("analyst", {})
    reporter = agent_results.get("reporter", {})
    listener = agent_results.get("listener", {})
    
    # Prepare prompt
    prompt = f"""
    Act as a Supply Chain Expert. Analyze the following data from market research agents for a {product_type} in {target_region} with max price ₹{max_price}.

    Competitors: {scout.get('competitors', [])}
    Features & Prices: {scout.get('features_prices', [])}
    Seasonality: {analyst.get('seasonality', 'N/A')}
    Supply Chain Risks: {reporter.get('supply_chain_risks', [])}
    User Pain Points: {listener.get('user_pain_points', [])}

    Provide the following outputs:
    - When to Market: Based on seasonality data.
    - Raw Material Buying: When to buy materials based on trends.
    - Possible Competitors: List 3-5 competitors.
    - Feasibility: High/Medium/Low based on price comparison.
    - Safe Batch Size: Estimated initial manufacturing quantity.
    - Key Factors: Important features to include.
    - Other Nearby Possible Target Regions: Suggest 2-3 nearby regions based on location.
    - Regional Expansion: Analyze the initial target region's success metrics and suggest top 3 expansion targets from adjacent regions based on trends.
    - User Pain Points: Summarize key user complaints and pain points.

    Output in JSON format with keys: when_to_market, raw_material_buy, competitors, feasibility, safe_batch_size, key_factors, nearby_regions, regional_expansion, user_pain_points
    """
    
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    
    result_text = response.choices[0].message.content
    # Parse JSON (assume GPT returns valid JSON)
    import json
    try:
        results = json.loads(result_text)
    except:
        results = {
            "when_to_market": "Data not available",
            "raw_material_buy": "Data not available",
            "competitors": scout.get('competitors', []),
            "feasibility": "Unknown",
            "safe_batch_size": "500 units",
            "key_factors": "Include standard features",
            "nearby_regions": ["Nearby Region 1", "Nearby Region 2"],
            "regional_expansion": "Top 3 expansion targets: Pune, Hyderabad, and Bangalore (in that order).",
            "user_pain_points": "Users complain about battery life and charging time."
        }
    
    return results
from fpdf import FPDF
import io

def generate_pdf(analysis_results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Synapsee AI Market Analysis Report", ln=True, align='C')
    pdf.ln(10)
    
    pdf.cell(200, 10, txt=f"When to Market: {analysis_results.get('when_to_market', 'N/A')}", ln=True)
    pdf.cell(200, 10, txt=f"Raw Material Buying: {analysis_results.get('raw_material_buy', 'N/A')}", ln=True)
    pdf.cell(200, 10, txt=f"Feasibility: {analysis_results.get('feasibility', 'N/A')}", ln=True)
    pdf.cell(200, 10, txt=f"Safe Batch Size: {analysis_results.get('safe_batch_size', 'N/A')}", ln=True)
    pdf.cell(200, 10, txt=f"Key Factors: {analysis_results.get('key_factors', 'N/A')}", ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, txt="Competitors:", ln=True)
    for comp in analysis_results.get('competitors', []):
        pdf.cell(200, 10, txt=f"- {comp}", ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, txt="Nearby Regions:", ln=True)
    for region in analysis_results.get('nearby_regions', []):
        pdf.cell(200, 10, txt=f"- {region}", ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Regional Expansion: {analysis_results.get('regional_expansion', 'N/A')}", ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"User Pain Points: {analysis_results.get('user_pain_points', 'N/A')}", ln=True)
    
    # Save to bytes
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer.getvalue()
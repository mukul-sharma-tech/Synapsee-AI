from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(product, region, insights):
    path = "report.pdf"
    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(
        f"<b>Market Intelligence Report – {product}</b>", styles["Title"]
    ))
    story.append(Paragraph(f"Region: {region}", styles["Normal"]))
    story.append(Paragraph(f"Feasibility Score: {insights['feasibility']}/100", styles["Normal"]))
    story.append(Paragraph(f"Safe Batch Size: {insights['batch']} units", styles["Normal"]))
    story.append(Paragraph(f"Market Timing: {insights['market_timing']}", styles["Normal"]))
    story.append(Paragraph(f"Raw Material Window: {insights['raw_material']}", styles["Normal"]))

    doc.build(story)
    return path

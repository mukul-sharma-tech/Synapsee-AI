import logging
import azure.functions as func
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from src.agents import run_agents
from src.synthesis import synthesize_results
from src.pdf_generator import generate_pdf

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Synapsee AI function triggered.')

    try:
        req_body = req.get_json()
        product_type = req_body.get('product_type')
        target_region = req_body.get('target_region')
        description = req_body.get('description')
        max_price = req_body.get('max_price')
        age_group = req_body.get('age_group')
        user_id = req_body.get('user_id')

        if not all([product_type, target_region, description, max_price]):
            return func.HttpResponse("Missing required parameters", status_code=400)

        # Run agents in parallel
        agent_results = run_agents(product_type, target_region, description, max_price, age_group)

        # Synthesize results
        analysis_results = synthesize_results(agent_results, product_type, target_region, max_price)

        # Generate PDF
        pdf_content = generate_pdf(analysis_results)

        # Save to DB (optional, for history)
        # from src.db import save_report
        # save_report(user_id, req_body, analysis_results, pdf_url)

        return func.HttpResponse(
            json.dumps({
                "results": analysis_results,
                "pdf": pdf_content.decode('latin-1')  # or base64
            }),
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse("Internal server error", status_code=500)
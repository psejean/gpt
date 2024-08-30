import logging
import json
import azure.functions as func
from simple_salesforce import Salesforce

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Salesforce credentials (Consider using environment variables for security)
    sf = Salesforce(username='your_username', 
                    password='your_password', 
                    security_token='your_security_token')
    
    # Parse the HTTP request body for the SOQL query
    try:
        req_body = req.get_json()
        soql_query = req_body.get('query')
    except ValueError:
        return func.HttpResponse(
            "Please pass a valid SOQL query in the request body",
            status_code=400
        )
    
    # Query Salesforce
    try:
        result = sf.query(soql_query)
        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error querying Salesforce: {e}")
        return func.HttpResponse(
            f"Error querying Salesforce: {e}",
            status_code=500
        )

import logging
import azure.functions as func  # Import the Azure Functions module

logging.basicConfig(level=logging.INFO)

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info("Function executed successfully.")
        
        # Return a simple JSON response using HttpResponse
        return func.HttpResponse(
            body='{"status": "success", "message": "Hello, your function is working!"}',
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error in main function: {e}")
        return func.HttpResponse(
            body=f'{{"status": "error", "message": "{str(e)}"}}',
            mimetype="application/json",
            status_code=500
        )

import logging

logging.basicConfig(level=logging.INFO)

def main(req):
    try:
        logging.info("Function executed successfully.")
        
        # Return a simple JSON response
        return {
            "status": "success",
            "message": "Hello, your function is working!"
        }
    except Exception as e:
        logging.error(f"Error in main function: {e}")
        return {"status": "error", "message": str(e)}

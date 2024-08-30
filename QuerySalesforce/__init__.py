import sys
import os

# Add the path to the locally installed packages
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'python_packages')))

import logging
import requests
import openai  # or whichever package you are using

logging.basicConfig(level=logging.INFO)

def main(req):
    logging.info("Starting main function...")
    try:
        # Simplified logic for testing
        return {"message": "Function is running"}
    except Exception as e:
        logging.error(f"Error in main function: {e}")
        return {"error": str(e)}

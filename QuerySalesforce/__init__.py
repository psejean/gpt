import os
import sys
import logging

# Add the local python_packages directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'python_packages'))

import requests
import openai  # Replaced azure.ai.openai with openai

logging.basicConfig(level=logging.INFO)

def get_salesforce_token():
    try:
        url = "https://test.salesforce.com/services/oauth2/token"
        payload = {
            'grant_type': 'password',
            'client_id': os.getenv('SALESFORCE_CLIENT_ID'),
            'client_secret': os.getenv('SALESFORCE_CLIENT_SECRET'),
            'username': os.getenv('SALESFORCE_USERNAME'),
            'password': os.getenv('SALESFORCE_PASSWORD')
        }
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx
        return response.json()['access_token']
    except requests.exceptions.RequestException as e:
        logging.error(f"Error obtaining Salesforce token: {e}")
        raise

def query_salesforce(query):
    logging.info("Querying Salesforce...")
    try:
        token = get_salesforce_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        query_url = f"https://collegelacite--devphil.sandbox.lightning.force.com/services/data/v60.0/query/?q={query}"
        response = requests.get(query_url, headers=headers)
        response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error querying Salesforce: {e}")
        raise

def generate_openai_response(data):
    logging.info("Generating response using OpenAI...")
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")  # Set the OpenAI API key from environment variable
        prompt = f"Based on the following Salesforce data, answer the user's query: {data}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"Error generating OpenAI response: {e}")
        raise

def main(req):
    try:
        # Example query to Salesforce
        query = req.get_json().get('query')
        salesforce_data = query_salesforce(query)
        
        # Generate response using OpenAI
        openai_response = generate_openai_response(salesforce_data)
        
        logging.info("Function executed successfully.")
        return {
            "status": "success",
            "data": openai_response
        }
    except Exception as e:
        logging.error(f"Error in main function: {e}")
        return {"status": "error", "message": str(e)}

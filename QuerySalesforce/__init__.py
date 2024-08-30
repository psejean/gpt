import requests
from azure.ai.openai import OpenAIClient
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)

def get_salesforce_token():
    logging.info("Getting Salesforce token...")
    try:
        url = "https://test.salesforce.com/services/oauth2/token"
        payload = {
        'grant_type': 'password',
        'client_id': '3MVG9gtjsZa8aaSWsgYzPGD_8xUOflPh1ID5zH5CdE7tgRVK4MPHfW4PVIRJUh6n_POyEqsKinAWqabYOI0wy',
        'client_secret': '9838FBEB2E38D964AD1726AF41712A5A7EE46DE9111E8ACD0957D7A8417D8E69',
        'username': 'integrationuser@lacitec.on.ca.devphil',
        'password': 'Chatgptrules99'
        }
        response = requests.post(url, data=payload)
        response.raise_for_status()
        logging.info("Salesforce token obtained successfully.")
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
        response.raise_for_status()
        logging.info("Salesforce query executed successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error querying Salesforce: {e}")
        raise

def generate_openai_response(data):
    logging.info("Generating OpenAI response...")
    try:
        client = OpenAIClient("https://openai-poc-psej-us.openai.azure.com/", "02c7e86bcfdd4d46a0743819fdcb1d80")
        prompt = f"Based on the following Salesforce data, answer the user's query: {data}"
        response = client.completions.create(engine="text-davinci-003", prompt=prompt)
        logging.info("OpenAI response generated successfully.")
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"Error generating OpenAI response: {e}")
        raise

def main(query):
    logging.info("Starting main function...")
    try:
        # Step 1: Query Salesforce
        salesforce_data = query_salesforce(query)
        
        # Step 2: Generate response using Azure OpenAI
        openai_response = generate_openai_response(salesforce_data)
        
        logging.info("Function executed successfully.")
        return openai_response
    except Exception as e:
        logging.error(f"Error in main function: {e}")
        return {"error": str(e)}

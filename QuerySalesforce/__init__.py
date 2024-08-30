import requests
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)

def get_salesforce_token():
    logging.info("Starting Salesforce token retrieval...")
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
        response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx
        token = response.json().get('access_token')
        logging.info("Salesforce token retrieved successfully.")
        return token
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
        logging.info("Headers created successfully.")
        query_url = f"https://collegelacite--devphil.sandbox.lightning.force.com/services/data/v60.0/query/?q={query}"
        response = requests.get(query_url, headers=headers)
        response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx
        logging.info("Salesforce query executed successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error querying Salesforce: {e}")
        raise

def main(query):
    logging.info("Starting main function...")
    try:
        # Step 1: Query Salesforce
        salesforce_data = query_salesforce(query)
        
        logging.info("Function executed successfully.")
        return {"data": salesforce_data}
    except Exception as e:
        logging.error(f"Error in main function: {e}")
        return {"error": str(e)}

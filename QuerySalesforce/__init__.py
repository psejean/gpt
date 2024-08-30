import requests
from azure.ai.openai import OpenAIClient

def get_salesforce_token():
    # Existing logic to get the Salesforce token
    url = "https://test.salesforce.com/services/oauth2/token"
    payload = {
        'grant_type': 'password',
        'client_id': '3MVG9gtjsZa8aaSWsgYzPGD_8xUOflPh1ID5zH5CdE7tgRVK4MPHfW4PVIRJUh6n_POyEqsKinAWqabYOI0wy',
        'client_secret': '9838FBEB2E38D964AD1726AF41712A5A7EE46DE9111E8ACD0957D7A8417D8E69',
        'username': 'integrationuser@lacitec.on.ca.devphil',
        'password': 'Chatgptrules99'
    }
    response = requests.post(url, data=payload)
    return response.json()['access_token']

def query_salesforce(query):
    # Existing logic to query Salesforce
    token = get_salesforce_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    query_url = f"https://collegelacite--devphil.sandbox.lightning.force.com/services/data/v60.0/query/?q={query}"
    response = requests.get(query_url, headers=headers)
    return response.json()

def generate_openai_response(data):
    # Logic to interact with Azure OpenAI
    client = OpenAIClient("https://openai-poc-psej-us.openai.azure.com/", "02c7e86bcfdd4d46a0743819fdcb1d80")
    prompt = f"Based on the following Salesforce data, answer the user's query: {data}"
    response = client.completions.create(engine="text-davinci-003", prompt=prompt)
    return response.choices[0].text.strip()

def main(query):
    # Step 1: Query Salesforce
    salesforce_data = query_salesforce(query)
    
    # Step 2: Generate response using Azure OpenAI
    openai_response = generate_openai_response(salesforce_data)
    
    return openai_response

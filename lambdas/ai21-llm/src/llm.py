import os
import json
import urllib3
import boto3
from botocore.exceptions import ClientError

# Defaults
API_KEY_SECRET_NAME = os.environ['API_KEY_SECRET_NAME']
DEFAULT_MODEL_TYPE = os.environ.get("DEFAULT_MODEL_TYPE","mid") 
ENDPOINT_URL = os.environ.get("ENDPOINT_URL", "https://api.ai21.com/studio/v1/j2-{MODEL_TYPE}/complete")
MAX_TOKENS = 256

def get_secret(secret_name):
    print("Getting API key from Secrets Manager")
    secrets_client = boto3.client('secretsmanager')
    try:
        response = secrets_client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    api_key = response['SecretString']
    return api_key

def call_llm(parameters, prompt):
    api_key = get_secret(API_KEY_SECRET_NAME)
    # Default parameters
    data = {
        "maxTokens": MAX_TOKENS
    }
    data.update(parameters)
    data["prompt"] = prompt
    headers = {
        "Authorization": f"Bearer {api_key}",
        "content-type": "application/json",
        "accept": "application/json"
    }
    # Endpoint URL is a template, so we need to replace the model type with the one specified in parameters
    endpoint_url = ENDPOINT_URL.format(MODEL_TYPE=parameters.get("model_type", DEFAULT_MODEL_TYPE))
    http = urllib3.PoolManager()
    try:
        response = http.request(
            "POST",
            endpoint_url,
            body=json.dumps(data),
            headers=headers
        )
        if response.status != 200:
            raise Exception(f"Error: {response.status} - {response.data}")
        generated_text = json.loads(response.data)["completions"][0]["data"]["text"].strip()
        return generated_text
    except Exception as err:
        print(err)
        raise

"""
Example Test Event:
{
  "prompt": "Why is the sky blue?\nAssistant:",
  "parameters": {
    "model_type": "mid",
    "temperature": 0
  }
}
For supported parameters, see the link to AI21 docs: https://docs.ai21.com/reference/j2-complete-ref
"""
def lambda_handler(event, context):
    print("Event: ", json.dumps(event))
    global secret
    prompt = event["prompt"]
    parameters = event["parameters"] 
    generated_text = call_llm(parameters, prompt)
    print("Result:", json.dumps(generated_text))
    return {
        'generated_text': generated_text
    }

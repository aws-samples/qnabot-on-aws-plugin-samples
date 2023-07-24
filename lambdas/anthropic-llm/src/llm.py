import os
import json
import urllib3
import boto3
from botocore.exceptions import ClientError

# Defaults
API_KEY_SECRET_NAME = os.environ['API_KEY_SECRET_NAME']
ENDPOINT_URL = os.environ.get("ENDPOINT_URL", "https://api.anthropic.com/v1/complete")
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL","claude-instant-1")
MAX_TOKENS_TO_SAMPLE = 256

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
    # default parameters.. see https://docs.anthropic.com/claude/reference/complete_post for additional
    # allowed parameters
    data = {
        "max_tokens_to_sample": MAX_TOKENS_TO_SAMPLE,
        "model": DEFAULT_MODEL
    }
    data.update(parameters)
    data["prompt"] = prompt
    headers = {
        "anthropic-version": "2023-06-01", 
        "x-api-key": api_key,
        "content-type": "application/json",
        "accept": "application/json"
    }
    http = urllib3.PoolManager()
    try:
        response = http.request(
            "POST",
            ENDPOINT_URL,
            body=json.dumps(data),
            headers=headers
        )
        if response.status != 200:
            raise Exception(f"Error: {response.status} - {response.data}")
        generated_text = json.loads(response.data)["completion"].strip()
        return generated_text
    except Exception as err:
        print(err)
        raise

"""
Example Test Event:
{
  "prompt": "\n\nHuman:Why is the sky blue?\n\nAssistant:",
  "parameters": {
    "temperature": 0,
    "model": "claude-instant-1"
  }
}
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

import boto3
import json
import os

# Defaults
DEFAULT_MODEL_ID = os.environ.get("DEFAULT_MODEL_ID","amazon.titan-embed-text-v1")
AWS_REGION = os.environ["AWS_REGION_OVERRIDE"] if "AWS_REGION_OVERRIDE" in os.environ else os.environ["AWS_REGION"]
ENDPOINT_URL = os.environ.get("ENDPOINT_URL", f'https://bedrock-runtime.{AWS_REGION}.amazonaws.com')
EMBEDDING_MAX_WORDS = os.environ.get("EMBEDDING_MAX_WORDS") or 6000  # limit 8k token ~ 6k words

# global variables - avoid creating a new client for every request
client = None

# limit number of words to avoid exceeding model token limit
def truncate_text(text, n=500):
    words = text.split()
    if (len(words) > n):
        print(f"Truncating input text from {len(words)} to {n} words")
        truncated_words = words[:n]
        truncated_text = " ".join(truncated_words)
        return truncated_text
    else:
        return text

def get_client():
    print("Connecting to Bedrock Service: ", ENDPOINT_URL)
    client = boto3.client(service_name='bedrock-runtime', region_name=AWS_REGION, endpoint_url=ENDPOINT_URL)
    return client

"""
Example Test Event:
{
  "inputText": "Why is the sky blue?"
}
"""
def lambda_handler(event, context):
    print("Event:", json.dumps(event))
    global client
    modelId = DEFAULT_MODEL_ID
    max_words = EMBEDDING_MAX_WORDS
    text = truncate_text(event["inputText"].strip(), int(max_words))
    body = json.dumps({"inputText": text})
    if (client is None):
        client = get_client()
    response = client.invoke_model(body=body, modelId=modelId, accept='application/json', contentType='application/json')
    response_body = json.loads(response.get('body').read())
    print("Embeddings length:", len(response_body["embedding"]))
    return response_body

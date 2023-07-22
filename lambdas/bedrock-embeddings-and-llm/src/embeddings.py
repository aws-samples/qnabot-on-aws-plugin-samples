import boto3
import json
import os

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
    print("Connecting to Bedrock Service")
    region = os.environ['AWS_REGION']
    client = boto3.client(service_name='bedrock', region_name=region, endpoint_url=f'https://bedrock.{region}.amazonaws.com')
    return client

def lambda_handler(event, context):
    print("Event:", json.dumps(event))
    global client
    modelId = os.environ.get("BEDROCK_MODEL_IDENTIFIER") or 'amazon.titan-e1t-medium'
    max_tokens = os.environ.get("EMBEDDING_MAX_WORDS") or 300
    text = truncate_text(event["inputText"], int(max_tokens))
    body = json.dumps({"inputText": text})
    if (client is None):
        client = get_client()
    response = client.invoke_model(body=body, modelId=modelId, accept='application/json', contentType='application/json')
    response_body = json.loads(response.get('body').read())
    print("Embeddings length:", len(response_body["embedding"]))
    return response_body

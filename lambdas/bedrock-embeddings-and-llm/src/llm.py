import boto3
import json
import os

# Defaults
DEFAULT_MODEL_ID = os.environ.get("DEFAULT_MODEL_ID","anthropic.claude-instant-v1")
AWS_REGION = os.environ["AWS_REGION_OVERRIDE"] if "AWS_REGION_OVERRIDE" in os.environ else os.environ["AWS_REGION"]
ENDPOINT_URL = os.environ.get("ENDPOINT_URL", f'https://bedrock-runtime.{AWS_REGION}.amazonaws.com')
DEFAULT_MAX_TOKENS = 256

# global variables - avoid creating a new client for every request
client = None

def get_client():
    print("Connecting to Bedrock Service: ", ENDPOINT_URL)
    client = boto3.client(service_name='bedrock-runtime', region_name=AWS_REGION, endpoint_url=ENDPOINT_URL)
    return client

def get_request_body(modelId, parameters, prompt):
    provider = modelId.split(".")[0]
    request_body = None
    if provider == "anthropic":
        # claude-3 models use new messages format
        if modelId.startswith("anthropic.claude-3"):
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "messages": [{"role": "user", "content": [{'type':'text','text': prompt}]}],
                "max_tokens": DEFAULT_MAX_TOKENS
            }
            request_body.update(parameters)
        else:
            request_body = {
                "prompt": prompt,
                "max_tokens_to_sample": DEFAULT_MAX_TOKENS
            } 
            request_body.update(parameters)
    elif provider == "ai21":
        request_body = {
            "prompt": prompt,
            "maxTokens": DEFAULT_MAX_TOKENS
        }
        request_body.update(parameters)
    elif provider == "amazon":
        textGenerationConfig = {
            "maxTokenCount": DEFAULT_MAX_TOKENS
        }
        textGenerationConfig.update(parameters)
        request_body = {
            "inputText": prompt,
            "textGenerationConfig": textGenerationConfig
        }
    elif provider == "cohere":
        request_body = {
            "prompt": prompt,
            "max_tokens": DEFAULT_MAX_TOKENS
        }
        request_body.update(parameters)
    elif provider == "meta":
        request_body = {
            "prompt": prompt,
            "max_gen_len": DEFAULT_MAX_TOKENS
        }
        request_body.update(parameters)
    else:
        raise Exception("Unsupported provider: ", provider)
    return request_body

def get_generate_text(modelId, response):
    provider = modelId.split(".")[0]
    generated_text = None
    response_body = json.loads(response.get("body").read())
    print("Response body: ", json.dumps(response_body))
    if provider == "anthropic":
        # claude-3 models use new messages format
        if modelId.startswith("anthropic.claude-3"):
            generated_text = response_body.get("content")[0].get("text")
        else:
            generated_text = response_body.get("completion")
    elif provider == "ai21":
        generated_text = response_body.get("completions")[0].get("data").get("text")
    elif provider == "amazon":
        generated_text = response_body.get("results")[0].get("outputText")
    elif provider == "cohere":
        generated_text = response_body.get("generations")[0].get("text")
    elif provider == "meta":
        generated_text = response_body.get("generation")
    else:
        raise Exception("Unsupported provider: ", provider)
    return generated_text

def call_llm(parameters, prompt):
    global client
    modelId = parameters.pop("modelId", DEFAULT_MODEL_ID)
    body = get_request_body(modelId, parameters, prompt)
    print("ModelId", modelId, "-  Body: ", body)
    if (client is None):
        client = get_client()
    response = client.invoke_model(body=json.dumps(body), modelId=modelId, accept='application/json', contentType='application/json')
    generated_text = get_generate_text(modelId, response)
    return generated_text


"""
Example Test Event:
{
  "prompt": "\n\nHuman:Why is the sky blue?\n\nAssistant:",
  "parameters": {
    "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
    "temperature": 0,
    "system": "You are an AI assistant that always answers in ryhming couplets"
  }
}
For supported parameters for each provider model, see Bedrock docs: https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/providers
"""
def lambda_handler(event, context):
    print("Event: ", json.dumps(event))
    prompt = event["prompt"]
    parameters = event["parameters"] 
    generated_text = call_llm(parameters, prompt)
    print("Result:", json.dumps(generated_text))
    return {
        'generated_text': generated_text
    }
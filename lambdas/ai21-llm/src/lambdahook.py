import os
import json
import urllib3
import boto3
from botocore.exceptions import ClientError

# Defaults
API_KEY_SECRET_NAME = os.environ['API_KEY_SECRET_NAME']
DEFAULT_MODEL_TYPE = os.environ.get("DEFAULT_MODEL_TYPE","j2-mid") 
ENDPOINT_URL = os.environ.get("ENDPOINT_URL", "https://api.ai21.com/studio/v1/{MODEL_TYPE}/complete")
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

def get_llm_response(parameters, prompt):
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

def get_args_from_lambdahook_args(event):
    parameters = {}
    lambdahook_args_list = event["res"]["result"].get("args",[])
    print("LambdaHook args: ", lambdahook_args_list)
    if len(lambdahook_args_list):
        try:
            parameters = json.loads(lambdahook_args_list[0])
        except Exception as e:
            print(f"Failed to parse JSON:", lambdahook_args_list[0], e)
            print("..continuing")
    return parameters

def format_response(event, llm_response, prefix):
    # set plaintext, markdown, & ssml response
    if prefix in ["None", "N/A", "Empty"]:
        prefix = None
    plainttext = llm_response
    markdown = llm_response
    ssml = llm_response
    if prefix:
        plainttext = f"{prefix}\n\n{plainttext}"
        markdown = f"**{prefix}**\n\n{markdown}"
    # add plaintext, markdown, and ssml fields to event.res
    event["res"]["message"] = plainttext
    event["res"]["session"]["appContext"] = {
        "altMessages": {
            "markdown": markdown,
            "ssml": ssml
        }
    }
    #TODO - can we determine when LLM has a good answer or not?
    #For now, always assume it's a good answer.
    #QnAbot sets session attribute qnabot_gotanswer True when got_hits > 0
    event["res"]["got_hits"] = 1   
    return event

def lambda_handler(event, context):
    print("Received event: %s" % json.dumps(event))
    # args = {"Prefix:"<Prefix|None>", "Model_params":{"max_tokens":256}, "Prompt":"<prompt>"}
    args = get_args_from_lambdahook_args(event)
    # prompt set from args, or from req.question if not specified in args.
    prompt = args.get("Prompt", event["req"]["question"])
    model_params = args.get("Model_params",{})
    llm_response = get_llm_response(model_params, prompt)
    prefix = args.get("Prefix","LLM Answer:")
    event = format_response(event, llm_response, prefix)
    print("Returning response: %s" % json.dumps(event))
    return event

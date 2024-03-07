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

def replace_template_placeholders(prompt, event):
    # history
    history_array = json.loads(event["req"]["_userInfo"].get("chatMessageHistory","[]"))
    history_str = '\n'.join(f"{key}: {value}" for item in history_array for key, value in item.items())
    prompt = prompt.replace("{history}", history_str)
    # TODO - replace additional prompt template placeholders - eg query, input, session attributes, user info
    return prompt

def format_prompt(modelId, prompt):  
    provider = modelId.split(".")[0]
    if provider == "anthropic":
        # Claude models prior to v3 required 'Human/Assistant' formatting
        if not modelId.startswith("anthropic.claude-3"):
            print("Model provider is Anthropic v2. Checking prompt format.")
            if not prompt.startswith("\n\nHuman:") or not prompt.startswith("\n\nSystem:"):
                prompt = "\n\nHuman: " + prompt
                print("Prepended '\\n\\nHuman:'")
            if not prompt.endswith("\n\nAssistant:"):
                prompt = prompt + "\n\nAssistant:"
                print("Appended '\\n\\nHuman:'")
    print(f"Prompt: {json.dumps(prompt)}")
    return prompt

def get_llm_response(modelId, parameters, prompt):
    global client
    body = get_request_body(modelId, parameters, prompt)
    print("ModelId", modelId, "-  Body: ", body)
    if (client is None):
        client = get_client()
    response = client.invoke_model(body=json.dumps(body), modelId=modelId, accept='application/json', contentType='application/json')
    generated_text = get_generate_text(modelId, response)
    return generated_text

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
    # args = {"Prefix:"<Prefix|None>", "Model_params":{"modelId":"anthropic.claude-instant-v1", "max_tokens":256}, "Prompt":"<prompt>"}
    args = get_args_from_lambdahook_args(event)
    model_params = args.get("Model_params",{})
    modelId = model_params.pop("modelId", DEFAULT_MODEL_ID)
    # prompt set from args, or from req.question if not specified in args.
    prompt = args.get("Prompt", event["req"]["question"])
    prompt = format_prompt(modelId, prompt)
    prompt = replace_template_placeholders(prompt, event)
    llm_response = get_llm_response(modelId, model_params, prompt)
    prefix = args.get("Prefix","LLM Answer:")
    event = format_response(event, llm_response, prefix)
    print("Returning response: %s" % json.dumps(event))
    return event

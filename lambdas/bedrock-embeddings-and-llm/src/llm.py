import json
from langchain.llms import Bedrock

# global variables - avoid creating a new model for every request
llm = None

def get_llm(model_params):
    print("Getting Bedrock model from LangChain")
    # model_id is required.. use default if not provided
    if not model_params.get("model_id"):
        model_params["model_id"] = "amazon.titan-tg1-large"
    model = Bedrock(**model_params)
    return model

def lambda_handler(event, context):
    print("Event: ", json.dumps(event))
    global llm
    prompt = event["prompt"]
    model_params = event["parameters"] or {}
    if (llm is None):
        llm = get_llm(model_params)
    generated_text = llm(prompt)
    print("Result:", json.dumps(generated_text))
    return {
        'generated_text': generated_text
    }
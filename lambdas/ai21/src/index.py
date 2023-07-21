import boto3, os
from botocore.exceptions import ClientError
from langchain.llms import AI21

# global variables - avoid creating a new model for every request
llm = None

def get_secret(secret_name):
    secrets_client = boto3.client('secretsmanager')
    try:
        response = secrets_client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    api_key = response['SecretString']
    return api_key

def get_llm(params):
    print("Getting API key from Secrets Manager")
    secret_name = os.environ['API_KEY_SECRET_NAME']
    api_key = get_secret(secret_name)
    os.environ['AI21_API_KEY'] = api_key
    print("Getting LLM model from LangChain")
    model = AI21(**params)
    return model

def lambda_handler(event, context):
    print("Event: ", event)
    global llm
    prompt = event["prompt"]
    model_params = event["parameters"] 
    if (llm is None):
        llm = get_llm(model_params)
    generated_text = llm(prompt)
    print("Result:", generated_text)
    return {
        'generated_text': generated_text
    }
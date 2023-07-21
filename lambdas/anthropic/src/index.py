import boto3, os
from botocore.exceptions import ClientError
from langchain.chat_models import ChatAnthropic
from langchain.schema import HumanMessage

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
    os.environ['ANTHROPIC_API_KEY'] = api_key
    print("Getting LLM model from LangChain")
    model = ChatAnthropic(**params)
    return model

def lambda_handler(event, context):
    print("Event: ", event)
    global llm
    prompt = event["prompt"]
    model_params = event["parameters"] 
    if (llm is None):
        llm = get_llm(model_params)
    messages = [
        HumanMessage(
            content=prompt
        )
    ]
    generated_text = llm(messages).content
    print("Result:", generated_text)
    return {
        'generated_text': generated_text
    }

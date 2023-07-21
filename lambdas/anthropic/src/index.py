import boto3, os
from botocore.exceptions import ClientError
from langchain.chat_models import ChatAnthropic
from langchain.schema import HumanMessage

secrets_client = boto3.client('secretsmanager')
anthropic_secret_name = os.environ['ANTHROPIC_API_KEY_SECRET_NAME']


def get_secret(secret_name):
    try:
        response = secrets_client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    api_key = response['SecretString']

    return api_key


def get_llm(params):
    
    api_key = get_secret(anthropic_secret_name)
    os.environ['ANTHROPIC_API_KEY'] = api_key
    model = ChatAnthropic(**params)

    return model


def lambda_handler(event, context):
    prompt = event["prompt"]
    model_params = event["parameters"]
 
    llm = get_llm(model_params)
    
    messages = [
        HumanMessage(
            content=prompt
        )
    ]
    generated_text = llm(messages).content
  
    return {
        'generated_text': generated_text
    }

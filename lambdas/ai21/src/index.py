import boto3, os
from botocore.exceptions import ClientError
from langchain.llms import AI21

secrets_client = boto3.client('secretsmanager')
ai21_secret_name = os.environ['AI21_API_KEY_SECRET_NAME']


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

    # get API key from Secrets Manager
    api_key = get_secret(ai21_secret_name)
    os.environ['AI21_API_KEY'] = api_key
    model = AI21(**params)

    return model


def lambda_handler(event, context):
    prompt = event["prompt"]
    model_params = event["parameters"]


    llm = get_llm(model_params)
    generated_text = llm(prompt)
        
    return {
        'generated_text': generated_text
    }
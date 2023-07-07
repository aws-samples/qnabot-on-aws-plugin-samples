import boto3
from botocore.exceptions import ClientError
import os
from langchain.llms import AI21, Anthropic
from langchain.llms.ai21 import AI21PenaltyData
# from langchain import PromptTemplate, LLMChain


secrets_client = boto3.client('secretsmanager')
ai21_secret_name = os.environ['AI21_API_KEY_SECRET_NAME']
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

def get_llm(llm_model, params):

    if llm_model == 'AI21':
        # get API key from Secrets Manager
        api_key = get_secret(ai21_secret_name)
        model = AI21(
            ai21_api_key=api_key,
            numResults=1,
            maxTokens=params['maxTokens'],
            minTokens=params['minTokens'],
            temperature=params['temperature'],
            topP=params['topP'],
            topKReturn=params['topKReturn'],
            frequencyPenalty=AI21PenaltyData(
                scale=1,
                applyToWhitespaces=True,
                applyToPunctuations=True,
                applyToNumbers=True,
                applyToStopwords=True,
                applyToEmojis=True
            ),
            presencePenalty=AI21PenaltyData(
                scale=1,
                applyToWhitespaces=True,
                applyToPunctuations=True,
                applyToNumbers=True,
                applyToStopwords=True,
                applyToEmojis=True
            ),
            countPenalty=AI21PenaltyData(
                scale=1,
                applyToWhitespaces=True,
                applyToPunctuations=True,
                applyToNumbers=True,
                applyToStopwords=True,
                applyToEmojis=True
            )
        )

    elif llm_model == 'ANTHROPIC':
        api_key = get_secret(anthropic_secret_name)
        model = Anthropic(model="<model_name>", anthropic_api_key=api_key)

    return model



def lambda_handler(event, context):
           
    prompt = event["prompt"]
    model_params = event["parameters"]
    # settings = event["settings"]
    # apiKey = settings['LLM_THIRD_PARTY_API_KEY']
    llm_model_name = model_params['LLM_THIRD_PARTY_MODEL']

    llm = get_llm(llm_model_name, model_params)

    generated_text = llm(prompt)

    # if 'contextualAnswers' in model_params and model_params['contextualAnswers'] == 'TRUE':
    #     generated_text = get_contextualAnswers(prompt,model_params,apiKey)
    # else:
    #     generated_text = get_jurrasic(prompt,model_params,apiKey)

    return {
        'generated_text': generated_text
    }
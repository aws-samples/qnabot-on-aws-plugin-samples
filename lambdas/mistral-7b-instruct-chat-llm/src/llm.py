import boto3
import json
import os
import io
from typing import Dict

# grab environment variables
SAGEMAKER_ENDPOINT_NAME = os.environ['SAGEMAKER_ENDPOINT_NAME']
runtime= boto3.client('runtime.sagemaker')

def transform_input(prompt: Dict, model_kwargs: Dict) -> bytes:
    input_str = json.dumps(
        {
            "inputs": prompt,
            "parameters": model_kwargs,
        }
    )
    return input_str.encode("utf-8")


def call_llm(parameters, prompt):
    data = transform_input(prompt, parameters)
    response = runtime.invoke_endpoint(EndpointName=SAGEMAKER_ENDPOINT_NAME,
                                       ContentType='application/json',
                                       Body=data)
    generated_text = json.loads(response['Body'].read().decode("utf-8"))
    return generated_text[0]["generated_text"]

    
def lambda_handler(event, context):
    print("Event: ", json.dumps(event))
    prompt = event["prompt"]
    parameters = event["parameters"] 
    generated_text = call_llm(parameters, prompt)
    print("Result:", json.dumps(generated_text))
    return {
        'generated_text': generated_text
    }

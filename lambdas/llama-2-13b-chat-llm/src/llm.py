import boto3
import json
import os
import io
from typing import Dict

# TEMPERATURE = os.environ.get("TEMPERATURE", 1e-10)
# MAX_NEW_TOKENS = os.environ.get("MAX_NEW_TOKENS", 1024)  # max number of tokens to generate in the output

# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime= boto3.client('runtime.sagemaker')

def transform_input(prompt: Dict, model_kwargs: Dict) -> bytes:
    input_str = json.dumps(
        {
            "inputs": [
                [
                    {"role": "user", "content": prompt},
                ]
            ],
            "parameters": model_kwargs,
        }
    )
    # print(f"input_str: {input_str}\n")
    return input_str.encode("utf-8")


def call_llm(parameters, prompt):
    
    # print(json.dumps(prompt))
    # model_kwargs={"max_new_tokens": MAX_NEW_TOKENS, "temperature": TEMPERATURE}
    
    # print(parameters)
    
    data = transform_input(prompt, parameters)

    # print(payload)

    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='application/json',
                                       CustomAttributes="accept_eula=true",
                                       Body=data)
    # print(response)

    generated_text = json.loads(response['Body'].read().decode())
    
    # print(generated_text)
    return generated_text[0]["generation"]["content"]

    
def lambda_handler(event, context):
    print("Event: ", json.dumps(event))
    prompt = event["prompt"]
    parameters = event["parameters"] 
    generated_text = call_llm(parameters, prompt)
    print("Result:", json.dumps(generated_text))
    return {
        'generated_text': generated_text
    }

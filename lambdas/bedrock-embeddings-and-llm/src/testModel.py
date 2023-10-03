import boto3
import json
import os
import cfnresponse
import llm

"""
Example Test Event:
{
  "RequestType": "Create",
  "ResourceProperties": {
    "EmbeddingsModelId": "amazon.titan-embed-text-v1",
    "TextModelId": "amazon.titan-text-express-v1"
  }
}
"""
def lambda_handler(event, context):
    print("Event: ", json.dumps(event))
    global client
    status = cfnresponse.SUCCESS
    responseData = {}
    reason = "Success"
    modelId = ""
    if event['RequestType'] != 'Delete':
        prompt = "\n\nHuman: Why is the sky blue?\n\nAssistant:"
        try:
            embeddingsModelId = event['ResourceProperties'].get('EmbeddingsModelId', '')
            llmModelId = event['ResourceProperties'].get('LLMModelId', '')
            client = llm.get_client()
            # Test EmbeddingsModel
            modelId = embeddingsModelId        
            body = json.dumps({"inputText": prompt})
            print(f"Testing {modelId} - {body}")
            client.invoke_model(body=body, modelId=modelId, accept='application/json', contentType='application/json')
            # Test LLMModel
            modelId = llmModelId
            parameters = {
                "modelId": modelId,
                "temperature": 0
            }
            print(f"Testing {modelId}")
            llm.call_llm(parameters, prompt)            
        except Exception as e:
            status = cfnresponse.FAILED
            reason = f"Exception thrown testing ModelId='{modelId}'. Check that Amazon Bedrock is available in your region, and that models ('{embeddingsModelId}' and '{llmModelId}') are activated in your Amazon Bedrock account - {e}"
    print(f"Status: {status}, Reason: {reason}")        
    cfnresponse.send(event, context, status, responseData, reason=reason) 
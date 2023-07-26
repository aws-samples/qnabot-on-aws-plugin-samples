import cfnresponse
import json

# Default prompt temnplates
AI21_GENERATE_QUERY_PROMPT_TEMPLATE = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.<br>Chat History: <br>{history}<br>Follow up question: {input}<br>Standalone question:"""
AI21_QA_PROMPT_TEMPLATE = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know. Documents: {context} Instruction: Based on the above documents, provide a detailed answer for {query} Answer "don't know" if not present in the document. Solution:"""

def getModelSettings(modelType):
    params = {
        "model_type": modelType,
        "temperature": 0,
        "maxTokens": 256,
        "minTokens": 0,
        "topP": 1
    }
    settings = {
        'LLM_GENERATE_QUERY_MODEL_PARAMS': json.dumps(params),
        'LLM_QA_MODEL_PARAMS': json.dumps(params),
        'LLM_GENERATE_QUERY_PROMPT_TEMPLATE': AI21_GENERATE_QUERY_PROMPT_TEMPLATE,
        'LLM_QA_PROMPT_TEMPLATE': AI21_QA_PROMPT_TEMPLATE
    }
    
    return settings

def lambda_handler(event, context): 
    print("Event: ", json.dumps(event))
    status = cfnresponse.SUCCESS
    responseData = {}
    reason = ""
    if event['RequestType'] != 'Delete':
        try:                   
            modelType = event['ResourceProperties'].get('ModelType', '')
            responseData = getModelSettings(modelType) 
        except Exception as e:
            print(e)
            status = cfnresponse.FAILED
            reason = f"Exception thrown: {e}"              
    cfnresponse.send(event, context, status, responseData, reason=reason) 
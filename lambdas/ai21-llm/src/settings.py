import cfnresponse
import json

# Default prompt temnplates
AI21_GENERATE_QUERY_PROMPT_TEMPATE = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.<br>Chat History: <br>{history}<br>Follow up question: {input}<br>Standalone question:"""
AI21_QA_PROMPT_TEMPLATE = """<br><br>Human: You are a friendly AI assistant. You provide answers only based on the provided reference passages. Here are reference passages in <references> tags:<br><references><br>{context}<br></references><br>If the references contain the information needed to respond, then write a confident response in under 50 words, quoting the relevant references. <br>Otherwise, if you can make an informed guess based on the reference passages, then write a less condident response in under 50 words, stating your assumptions.<br>Finally, if the references do not have any relevant information, then respond saying \\"Sorry, I don't know\\".<br><br>{query}<br><br>Assistant: According to the reference passages, in under 50 words:"""

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
        'LLM_GENERATE_QUERY_PROMPT_TEMPLATE': AI21_GENERATE_QUERY_PROMPT_TEMPATE,
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
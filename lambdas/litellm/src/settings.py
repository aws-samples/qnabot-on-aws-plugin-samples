import cfnresponse
import json

# Default prompt temnplates
ANTHROPIC_GENERATE_QUERY_PROMPT_TEMPLATE = """<br><br>Human: Here is a chat history in <chatHistory> tags:<br><chatHistory><br>{history}<br></chatHistory><br>Human: And here is a follow up question or statement from the human in <followUpMessage> tags:<br><followUpMessage><br>{input}<br></followUpMessage><br>Human: Rephrase the follow up question or statement as a standalone question or statement that makes sense without reading the chat history.<br><br>Assistant: Here is the rephrased follow up question or statement:"""
ANTHROPIC_QA_PROMPT_TEMPLATE = """<br><br>Human: You are a friendly AI assistant. You provide answers only based on the provided reference passages. Here are reference passages in <references> tags:<br><references><br>{context}<br></references><br>If the references contain the information needed to respond, then write a confident response in under 50 words, quoting the relevant references. <br>Otherwise, if you can make an informed guess based on the reference passages, then write a less condident response in under 50 words, stating your assumptions.<br>Finally, if the references do not have any relevant information, then respond saying \\"Sorry, I don't know\\".<br><br>{query}<br><br>Assistant: According to the reference passages, in under 50 words:"""

def getModelSettings(model):
    params = {
        "model": model,
        "temperature": 0,
        "maxTokens": 256,
        "minTokens": 0,
        "topP": 1
    }
    settings = {
        'LLM_GENERATE_QUERY_MODEL_PARAMS': json.dumps(params),
        'LLM_QA_MODEL_PARAMS': json.dumps(params),
        'LLM_GENERATE_QUERY_PROMPT_TEMPLATE': ANTHROPIC_GENERATE_QUERY_PROMPT_TEMPLATE,
        'LLM_QA_PROMPT_TEMPLATE': ANTHROPIC_QA_PROMPT_TEMPLATE
    }
    
    return settings

def lambda_handler(event, context): 
    print("Event: ", json.dumps(event))
    status = cfnresponse.SUCCESS
    responseData = {}
    reason = ""
    if event['RequestType'] != 'Delete':
        try:                   
            model = event['ResourceProperties'].get('Model', '')
            responseData = getModelSettings(model) 
        except Exception as e:
            print(e)
            status = cfnresponse.FAILED
            reason = f"Exception thrown: {e}"              
    cfnresponse.send(event, context, status, responseData, reason=reason) 
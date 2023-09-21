import cfnresponse
import json

# Default prompt temnplates
LLAMA2_GENERATE_QUERY_PROMPT_TEMPLATE = """<br><br>Human: Here is a chat history in <chatHistory> tags:<br><chatHistory><br>{history}<br></chatHistory><br>Human: And here is a follow up question or statement from the human in <followUpMessage> tags:<br><followUpMessage><br>{input}<br></followUpMessage><br>Human: Rephrase the follow up question or statement as a standalone question or statement that makes sense without reading the chat history.<br><br>Assistant: Here is the rephrased follow up question or statement:"""
LLAMA2_QA_PROMPT_TEMPLATE = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know. Documents: {context} Instruction: Based on the above documents, provide a detailed answer for {query} Answer "don't know" if not present in the document. Solution:"""

def getModelSettings(model):
    params = {
        "temperature":0.1,
        "max_new_tokens":256,
        "top_p":0.5
    }
    settings = {
        'LLM_GENERATE_QUERY_MODEL_PARAMS': json.dumps(params),
        'LLM_QA_MODEL_PARAMS': json.dumps(params),
        'LLM_GENERATE_QUERY_PROMPT_TEMPLATE': LLAMA2_GENERATE_QUERY_PROMPT_TEMPLATE,
        'LLM_QA_PROMPT_TEMPLATE': LLAMA2_QA_PROMPT_TEMPLATE
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
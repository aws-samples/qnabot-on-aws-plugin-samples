import cfnresponse
import json

# Default prompt temnplates
MISTRAL_GENERATE_QUERY_PROMPT_TEMPLATE = """<s>[INST] You are a helpful assistant. <br>Here is a chat history in <chatHistory> tags:<br><chatHistory><br>{history}<br></chatHistory><br><br>And here is a follow up question or statement from the human in <followUpMessage> tags:<br><followUpMessage><br>{input}<br></followUpMessage>[/INST]<br><br>[INST]Rephrase the follow up question or statement as a standalone question or statement that makes sense without reading the chat history.[/INST]"""
MISTRAL_QA_PROMPT_TEMPLATE = """<s>[INST]You are an AI chatbot. Carefully read the following context and conversation history and then provide a short answer to question at the end. If the answer cannot be determined from the history or the context, reply saying "Sorry, I don\'t know". <br><br>Context: {context}<br><br>History: <br>{history}<br><br>{input}[/INST]"""

def getModelSettings(model):
    params = {
        "model":model,
        "temperature":0.1,
        "max_new_tokens":512,
        "top_p":0.5,
        "top_k":50,
        "do_sample":True,
    }
    settings = {
        'LLM_GENERATE_QUERY_MODEL_PARAMS': json.dumps(params),
        'LLM_QA_MODEL_PARAMS': json.dumps(params),
        'LLM_GENERATE_QUERY_PROMPT_TEMPLATE': MISTRAL_GENERATE_QUERY_PROMPT_TEMPLATE,
        'LLM_QA_PROMPT_TEMPLATE': MISTRAL_QA_PROMPT_TEMPLATE
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
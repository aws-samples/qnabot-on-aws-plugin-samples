# qna-lambda-for-ai21



## Getting started

This is the add on Lambda script for QnABot that use Large Language Model to Query Disambiguation for Conversational Retrieval, and Generative Question Answering.

This Lambda script  make it easy for you to get started to integrate AI21 Public Endpoint. The function can call either make Jurrasic-2 or Task-Specific (Contextual Answers [BETA]) API call. 

## Pre-requisites

- Docker installed 
- AWS CLI installed
- QnABot stack deployed in the account

## Deploy the CloudFormation Script (Installation)

- Run deploy.sh to package the CloudFormation template and build necessary Lambda layers:
    ```
        ./deploy.sh <cfn_bucket> <cfn_prefix> [public]
    ```
    <cfn_bucket> - name of the S3 bucket to store build artifacts (will be created if not existing)
    <cfn_prefix> - S3 prefix to store build artifacts in the bucket
    [public] - optional, include to make the S3 bucket and artifacts publicly accessible
- Copy the Template URL made available in the script outputs.
- Go to [AWS CloudFormation](https://console.aws.amazon.com/cloudformation/) console.
- Create Stack > With new resources (standard) > and input the Amazon S3 URL of the packaged template.
- Go to Designer Page of QnA Bot that was previously deployed, and go to Lambda Hooks on left menu
- Copy the Lambda Role

![Here is an example](./images/lambda_hook.png)

- Paste the Role into the functionIamRole parameter.
- Click Next, Next and Submit to initiate CloudFormation stack creation.

## Post-Deployment

### Store API Keys in Secrets Manager

- Register Account in the third-party LLMs that you want to use
- Copy the API Key
- In the CloudFormation stack Outputs, there will be outputs in the format of `secret<LLM Name>Console`, e.g. `secretAnthropicConsole`. Click on the link there and you will be brought to the Secrets Manager console.
- Scroll down to `Secret value` section and input the API Key there.

### Update QnABot CloudFormation Stack parameter

- In the CloudFormation stack Outputs, there will be outputs in the format of `lambdaFunction<LLM Name>Arn`, e.g. `lambdaFunctionAnthropicArn`. Copy the value of the LLM that you want to use.
- Go to the QnABot CloudFormation stack that was previously deployed, and click Update.
- Choose `Use current template` and click Next.
- Input the Lambda ARN of your choice in the `LLMLambdaArn` parameter.
- Click Next, Next and Submit to update the stack.

### Update QnABot Settings with model parameters
Follow the steps below to try the AI21 Foudation Model API in this QnA bot. This function call __j2-jumbo-instruct/complete__ by default.
- Update the __LLM_QA_MODEL_PARAMS__  to `{"temperature":0,"maxTokens":12,"minTokens":0,"topP":1,"topKReturn":1,"model_type":"j2-jumbo-instruct"}`

### Make Task-Specific (Contextual Answers [BETA]) API call
Follow the steps below to try the Contextual Answers API in this QnA bot

1. Backup your prompt text in __LLM_QA_PROMPT_TEMPLATE__
2. Update the __LLM_QA_PROMPT_TEMPLATE__ to `{context}||question:{query}`
3. Backup your parameter in __LLM_QA_MODEL_PARAMS__
4. Update the __LLM_QA_MODEL_PARAMS__  to `{"temperature":0,"maxTokens":64,"minTokens":12,"topP":1,"topKReturn":1,"contextualAnswers":"TRUE"}`


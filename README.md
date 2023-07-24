# QnABot Sample Plugins

This repository provides sample LLM Lambda functions for use with QnABot, installable using CloudFormation.
1. AI21 LLM: Uses AI21's Jurassic model API - requires an AI21 account with an API Key
2. Anthropic LLM: Uses Anthropic's Claude model API - requires an Anthropic account with an API Key
3. Amazon Bedrock Embeddings and LLM: Uses Amazon Bedrock service API (preview) - requires access to Amazon Bedrock service (current in private preview)


### (optional) Build and Publish LCA CloudFormation artifacts

_Note: Perform this step only if you want to create deployment artifacts in your own account. Otherwise, we have hosted a CloudFormation template for 1-click deployment in the [deploy](#deploy) section_.

*Pre-requisite*: You must already have the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) (version 1.49 or higher) installed and configured. You can use an AWS Cloud9 environment.

Use the [publish.sh](./publish.sh) bash script to build the project and deploy CloudFormation templates to your own deployment bucket.

Run the script with up to 3 parameters:
```
./publish.sh <cfn_bucket> <cfn_prefix> [public]

- <cfn_bucket>: name of S3 bucket to deploy CloudFormation templates and code artifacts. If bucket does not exist it will be created.
- <cfn_prefix>: artifacts will be copied to the path specified by this prefix (path/to/artifacts/)
- public: (optional) Adding the argument "public" will set public-read acl on all published artifacts, for sharing with any account.
```

To deploy to non-default region, set environment variable `AWS_DEFAULT_REGION` to a region supported by QnABot. See: [Supported AWS Regions](https://docs.aws.amazon.com/solutions/latest/qnabot-on-aws/supported-aws-regions.html) 
E.g. to deploy in Ireland run `export AWS_DEFAULT_REGION=eu-west-1` before running the publish script. 

It downloads package dependencies, builds code zipfiles, and copies templates and zip files to the cfn_bucket.
When complete, it displays the URLS for the CloudFormation templates, 1-click URLs for launching the stack create in CloudFormation, e.g.:
```
------------------------------------------------------------------------------
Outputs
------------------------------------------------------------------------------
QNABOT-AI21-LLM
==============
 - Template URL: https://s3.us-east-1.amazonaws.com/bobs-artifacts-bucket/qnabot-plugins/ai21-llm.yaml
 - Deploy URL:   https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://s3.us-east-1.amazonaws.com/bobs-artifacts-bucket/qnabot-plugins/ai21-llm.yaml&stackName=QNABOT-AI21-LLM

QNABOT-ANTHROPIC-LLM
==============
 - Template URL: https://s3.us-east-1.amazonaws.com/bobs-artifacts-bucket/qnabot-plugins/anthropic-llm.yaml
 - Deploy URL:   https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://s3.us-east-1.amazonaws.com/bobs-artifacts-bucket/qnabot-plugins/anthropic-llm.yaml&stackName=QNABOT-ANTHROPIC-LLM

QNABOT-BEDROCK-EMBEDDINGS-LLM
==============
 - Template URL: https://s3.us-east-1.amazonaws.com/bobs-artifacts-bucket/qnabot-plugins/bedrock-embeddings-llm.yaml
 - Deploy URL:   https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://s3.us-east-1.amazonaws.com/bobs-artifacts-bucket/qnabot-plugins/bedrock-embeddings-llm.yaml&stackName=QNABOT-BEDROCK-EMBEDDINGS-LLM
```

### Deploy a new stack

Use AWS CloudFormation to deploy one or more of the sample plug in Lambdas in your own AWS account (if you do not have an AWS account, please see [How do I create and activate a new Amazon Web Services account?](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)):

1. Log into the [AWS console](https://console.aws.amazon.com/) if you are not already.
*Note: If you are logged in as an IAM user, ensure your account has permissions to create and manage the necessary resources and components for this application.*
2. Choose one of the **Launch Stack** buttons below for your desired AWS region to open the AWS CloudFormation console and create a new stack. AWS Full-Stack Template is supported in the following regions:

Plugin | Region name | Region code | Launch
--- | --- | --- | ---
QNABOT-AI21-LLM | US East (N. Virginia) | us-east-1 | [![Launch Stack](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://s3.us-east-1.amazonaws.com/bobs-artifacts-bucket/qnabot-plugins/ai21-llm.yaml&stackName=QNABOT-AI21-LLM)
QNABOT-ANTHROPIC-LLM | US East (N. Virginia) | us-east-1 | [![Launch Stack](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://s3.us-east-1.amazonaws.com/bobs-artifacts-bucket/qnabot-plugins/anthropic-llm.yaml&stackName=QNABOT-ANTHROPIC-LLM)
QNABOT-BEDROCK-EMBEDDINGS-AND-LLM | US East (N. Virginia) | us-east-1 | [![Launch Stack](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://s3.us-east-1.amazonaws.com/bobs-artifacts-bucket/qnabot-plugins/bedrock-embeddings-and-llm.yaml&stackName=QNABOT-BEDROCK-EMBEDDINGS-AND-LLM)

3. On the CloudFormation `Create Stack` page, click `Next`
4. Enter the following parameters:
    1. `Stack Name`: Name your stack, e.g. QNABOT-LLM-AI21
    2. `APIKey`: Your Third Party vendor account API Key, if applicable. The API Key is securely stored in AWS Secrets Manager. 


## Post-Deployment

### (Optional) Modify Third Party API Keys in Secrets Manager

When your stack is CREATED, choose the **Outputs** tab. Use the link for `APIKeySecret` to open AWS Secrets Manager to inspect or edit your API Key in `Secret value`.


### Configure QnABot to use your new LLM function

When your stack is CREATED, choose the **Outputs** tab
- Copy the value for `LLMLambdaArn` 
- Deploy or update a QnABot stack, selecting **LLMApi** as `LAMBDA`, and for **LLMLambdaArn** enter the Lambda Arn copied above. 

For more information, see [QnABot LLM README - Lambda Function](https://github.com/aws-solutions/qnabot-on-aws/blob/feature/llm-summarize-bedrock-falcon40B-kendrarag-kendraindexandcrawler/docs/LLM_Retrieval_and_generative_question_answering/README.md#3-lambda-function)  **TODO: Update link**

**------------  Rework below ---------------**
  
### Update QnABot Settings with model parameters
Follow the steps below to try the AI21 Foudation Model API in this QnA bot. This function call __j2-jumbo-instruct/complete__ by default.
- Update the __LLM_QA_MODEL_PARAMS__  to `{"temperature":0,"maxTokens":12,"minTokens":0,"topP":1,"topKReturn":1,"model_type":"j2-jumbo-instruct"}`

### Make Task-Specific (Contextual Answers [BETA]) API call
Follow the steps below to try the Contextual Answers API in this QnA bot

1. Backup your prompt text in __LLM_QA_PROMPT_TEMPLATE__
2. Update the __LLM_QA_PROMPT_TEMPLATE__ to `{context}||question:{query}`
3. Backup your parameter in __LLM_QA_MODEL_PARAMS__
4. Update the __LLM_QA_MODEL_PARAMS__  to `{"temperature":0,"maxTokens":64,"minTokens":12,"topP":1,"topKReturn":1,"contextualAnswers":"TRUE"}`


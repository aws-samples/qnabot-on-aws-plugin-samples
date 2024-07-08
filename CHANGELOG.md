# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
## [0.1.17] - 2024-07-08
- Amazon Q Business Expert plugin now supports Identity Center authentication - PR #30

## [0.1.16] - 2024-07-02
### Added
- Amazon Bedrock LLM plugin now suports anthropic.claude-3-haiku model - PR #28.

## [0.1.15] - 2024-03-07
### Added
- Amazon Bedrock LLM plugin now suports anthropic.claude-3-sonnet model, and deprecates anthropic.claude-v1  - PR #26 & PR #27.

## [0.1.14] - 2023-12-22
### Added
- Amazon Q Business Expert plugin now suports optional file attachments via Lex Web UI (v0.20.4) attach option and the new userFileUpload session attribute - PR #23.


## [0.1.13] - 2023-12-06
### Added
- Bedrock plugin updates to support new text models - #22
  - amazon.titan-text-lite-v1
  - anthropic.claude-v2:1
  - cohere.command-text-v14
  - cohere.command-light-text-v14
  - meta.llama2-13b-chat-v1
  - meta.llama2-70b-chat-v1

## [0.1.12] - 2023-11-29
### Added
- Amazon Q, your business expert now integrates with QnABot as a fallback answer source, using QnAbot's using Lambda hooks with CustomNoMatches/no_hits. For more information see: [QnABot LambdaHook for Amazon Q, your business expert (preview)](./lambdas/qna_bot_qbusiness_lambdahook/README.md)

## [0.1.11] - 2023-11-07
### Fixed
- Error in Bedrock QnABotSettingQAPromptTemplate output - prompt does not terminate with '\n\nAssistant:` and generates error from Bedrock - #13

## [0.1.10] - 2023-10-27
### Fixed
- Prompt bug: question not denoted by an XML tag, so LLM gets confused about what it's answering - PR #13
- Upgrade issue in BedrockBoto3Layer due to bedrock boto3 zip - PR #16

## [0.1.9] - 2023-10-26
### Added
- Added Amazon Bedrock support for configuring LLM as a fallback source of answers, using Lambda hooks with CustomNoMatches/no_hits  - PR #11

## [0.1.8] - 2023-10-10
### Added
- Added Mistral 7b Instruct LLM - PR #10

## [0.1.7] - 2023-10-05
### Fixed
- Bedrock embeddings function now strips any leading or trailing whitespace from input strings before generating embeddings to avoid whitespace affecting accuracy.

## [0.1.6] - 2023-10-03
### Fixed
- Test that Bedrock service and selected models are available in account during stack create/update to avoid downstream failures.

## [0.1.5] - 2023-09-30
### Fixed
- Increased default EMBEDDINGS_SCORE_THRESHOLD to reduce poor quality QnA matches
- Fix typo in QA_PROMPT_TEMPLATE

## [0.1.4] - 2023-09-28
### Added
- Remove preview Bedrock sdk extensions
- Update to Bedrock GA model identifiers
- Update to `bedrock-runtime` endpoints/service name
- Use latest Titan embeddings model
- Add `EmbeddingsLambdaDimensions` to Bedrock plugin stack outputs
- Add new [Lambda Hook function](./README.md#optional-use-the-llm-as-a-fallback-source-of-answers-using-lambda-hooks-with-customnomatchesno_hits) to AI21 Plugin (others coming later)  

## [0.1.3] - 2023-09-21
### Added
- Added LLama-2-13b-Chat plugin - PR #5

## [0.1.2] - 2023-08-10
### Added
- Cfn nag fixes

## [0.1.1] - 2023-08-08
### Added
- Update default value for BedrockPreviewSdkUrl parameter in Amazon Bedrock plugin template

## [0.1.0] - 2023-07-27
### Added
- Initial release

[Unreleased]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/compare/main...develop
[0.1.17]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.17
[0.1.16]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.16
[0.1.15]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.15
[0.1.14]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.14
[0.1.13]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.13
[0.1.12]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.12
[0.1.11]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.11
[0.1.10]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.10
[0.1.9]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.9
[0.1.8]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.8
[0.1.7]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.7
[0.1.6]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.6
[0.1.5]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.5
[0.1.4]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.4
[0.1.3]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.3
[0.1.2]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.2
[0.1.1]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.1
[0.1.0]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.0

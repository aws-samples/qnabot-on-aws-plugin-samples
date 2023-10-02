# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/compare/v0.1.6...develop
[0.1.6]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.6
[0.1.5]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.5
[0.1.4]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.4
[0.1.3]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.3
[0.1.2]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.2
[0.1.1]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.1
[0.1.0]: https://github.com/aws-samples/qnabot-on-aws-plugin-samples/releases/tag/v0.1.0

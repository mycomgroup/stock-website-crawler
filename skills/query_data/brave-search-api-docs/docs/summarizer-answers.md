---
id: "url-73c1336c"
type: "api"
title: "Brave Search - API"
url: "https://api-dashboard.search.brave.com/api-reference/summarizer/answers"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T02:32:47.567Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/chat/completions"
  method: "GET"
  sections: []
  tables:
    - {"index":0,"headers":["Cookie Enabled","Cookie Key","Cookie Value"],"rows":[["","Key","Value"]]}
    - {"index":1,"headers":["Header Enabled","Header Key","Header Value"],"rows":[["","Accept","*/*"],["","Content-Type","application/json"],["","Key","Value"]]}
    - {"index":2,"headers":["Parameter Enabled","Parameter Key","Parameter Value"],"rows":[["","Key","Value"]]}
    - {"index":3,"headers":["JSON"],"rows":[]}
  examples:
    - {"type":"request","language":"bash","code":"curl -X POST -s --compressed \"https://api.search.brave.com/res/v1/chat/completions\" \\\n  -H \"Accept: application/json\" \\\n  -H \"Accept-Encoding: gzip\" \\\n  -H \"Content-Type: application/json\" \\\n  -d '{\"stream\": false, \"messages\": [{\"role\": \"user\", \"content\": \"What is the second highest mountain?\"}]}' \\\n  -H \"x-subscription-token: <YOUR_BRAVE_SEARCH_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl -X POST -s --compressed \"https://api.search.brave.com/res/v1/chat/completions\" \\\n  -H \"Accept: application/json\" \\\n  -H \"Accept-Encoding: gzip\" \\\n  -H \"Content-Type: application/json\" \\\n  -d '{\"stream\": false, \"messages\": [{\"role\": \"user\", \"content\": \"What is the second highest mountain?\"}]}' \\\n  -H \"x-subscription-token: <YOUR_BRAVE_SEARCH_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"model\": \"brave-pro\",\n  \"system_fingerprint\": \"string\",\n  \"choices\": [\n    {\n      \"delta\": {\n        \"role\": \"assistant\",\n        \"content\": \"string\"\n      },\n      \"finish_reason\": \"stop\"\n    }\n  ],\n  \"created\": 1,\n  \"id\": \"string\",\n  \"object\": \"chat.completion.chunk\",\n  \"usage\": {\n    \"completion_tokens\": 1,\n    \"prompt_tokens\": 1,\n    \"total_tokens\": 1,\n    \"completion_tokens_details\": {\n      \"reasoning_tokens\": 1\n    }\n  }\n}"}
    - {"type":"response","language":"json","code":"{\n  \"model\": \"brave-pro\",\n  \"system_fingerprint\": \"string\",\n  \"choices\": [\n    {\n      \"delta\": {\n        \"role\": \"assistant\",\n        \"content\": \"string\"\n      },\n      \"finish_reason\": \"stop\"\n    }\n  ],\n  \"created\": 1,\n  \"id\": \"string\",\n  \"object\": \"chat.completion.chunk\",\n  \"usage\": {\n    \"completion_tokens\": 1,\n    \"prompt_tokens\": 1,\n    \"total_tokens\": 1,\n    \"completion_tokens_details\": {\n      \"reasoning_tokens\": 1\n    }\n  }\n}"}
  rawContent: "Search GET\n\nSearch POST\n\nLocal POIs GET\n\nPOI Descriptions GET\n\nRich search GET\n\nLLM Context GET\n\nLLM Context POST\n\nPlace Search GET\n\nNews GET\n\nNews POST\n\nVideos GET\n\nVideos POST\n\nImages GET\n\nAnswers POST\n\nSuggest GET\n\nSpell check GET\n\nAnswers\n\nAPI for AI-generated answers backed by real-time web search and verifiable sources\n\npost/v1/chat/completions\n\nmessagesCopy link to messagesType: array Messages[] 1…1 required  Show UserMessagefor messages\n\ncountryCopy link to countryType: Countrydefault:  \"us\"\n\nenable_citationsCopy link to enable_citationsType: Enable Citationsdefault:  false\n\nenable_entitiesCopy link to enable_entitiesType: Enable Entitiesdefault:  false\n\nenable_researchCopy link to enable_researchType: Enable Researchdefault:  false\n\nlanguageCopy link to languageType: Languagedefault:  \"en\"\n\nmax_completion_tokensCopy link to max_completion_tokensType: Max Completion Tokens nullable \nInteger numbers.\n\nInteger numbers.\n\nmetadataCopy link to metadataType: Metadata nullable  Show Metadatafor metadata\n\nmodelCopy link to modelType: Modelenumdefault:  \"brave-pro\"brave-probrave\n\nbrave-pro\n\nresearch_allow_thinkingCopy link to research_allow_thinkingType: Research Allow Thinkingdefault:  true\n\nresearch_maximum_number_of_iterationsCopy link to research_maximum_number_of_iterationsType: Research Maximum Number Of Iterationsmin:    1max:    5default:  4\nInteger numbers.\n\nresearch_maximum_number_of_queriesCopy link to research_maximum_number_of_queriesType: Research Maximum Number Of Queriesmin:    1max:    50default:  20\nInteger numbers.\n\n200Copy link to 200Type: OpenAIChatResponsechoicesType: array Choices[] required  Show ChoiceChunkfor choicescreatedType: Created required \nInteger numbers.\nidType: Id required modelType: Modelenumdefault:  \"brave-pro\"brave-probraveobjectenumdefault:  \"chat.completion.chunk\"const:   chat.completion.chunkchat.completion.chunksystem_fingerprintType: System Fingerprint nullable usageType: OpenAIUsage nullable  Show OpenAIUsagefor usage\n\nchoicesType: array Choices[] required  Show ChoiceChunkfor choices\n\ncreatedType: Created required \nInteger numbers.\n\nidType: Id required\n\nmodelType: Modelenumdefault:  \"brave-pro\"brave-probrave\n\nobjectenumdefault:  \"chat.completion.chunk\"const:   chat.completion.chunkchat.completion.chunk\n\nchat.completion.chunk\n\nsystem_fingerprintType: System Fingerprint nullable\n\nusageType: OpenAIUsage nullable  Show OpenAIUsagefor usage\n\n400Copy link to 400Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"OPTION_NOT_IN_PLAN\",\n      \"detail\": \"The option is not subscribed in the plan.\",\n      \"status\": 400,\n      \"meta\": {\n        \"component\": \"authentication\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\nerrorType: APIErrorModel required  Show APIErrorModelfor error\n\ntimeType: Timedefault:  0\nInteger numbers.\n\ntypeType: Typedefault:  \"ErrorResponse\"\n\n402Copy link to 402Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"USAGE_LIMIT_EXCEEDED\",\n      \"detail\": \"Usage limit exceeded.\",\n      \"status\": 402,\n      \"meta\": {\n        \"component\": \"api\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\n403Copy link to 403Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"RESOURCE_NOT_ALLOWED\",\n      \"detail\": \"The user is not authorized to access this resource.\",\n      \"status\": 403,\n      \"meta\": {\n        \"component\": \"api\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\n404Copy link to 404Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"SUBSCRIPTION_NOT_FOUND\",\n      \"detail\": \"No subscription found.\",\n      \"status\": 404,\n      \"meta\": {\n        \"component\": \"subscriptions\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\n422Copy link to 422Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"SUBSCRIPTION_TOKEN_INVALID\",\n      \"detail\": \"The provided subscription token is invalid.\",\n      \"status\": 422,\n      \"meta\": {\n        \"component\": \"authentication\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\n429Copy link to 429Type: APIErrorResponseExamples{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"RATE_LIMITED\",\n      \"detail\": \"Request rate limit exceeded for plan.\",\n      \"status\": 429,\n      \"meta\": {\n        \"component\": \"rate_limiter\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"QUOTA_LIMITED\",\n      \"detail\": \"Request quota limit exceeded for plan.\",\n      \"status\": 429,\n      \"meta\": {\n        \"component\": \"rate_limiter\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\nSuccessful Response\n\nPath Parameters\n\nCookies\n\nHeaders\n\nQuery Parameters\n\nCode Snippet (Collapsed)\n\nServer Server:https://api.search.brave.com/res\n\nAnswers Operations post/v1/chat/completions\n\nShow additional properties for Request Body\n\nRequest Example for post/v1/chat/completionscURL curl -X POST -s --compressed \"https://api.search.brave.com/res/v1/chat/completions\" \\\n  -H \"Accept: application/json\" \\\n  -H \"Accept-Encoding: gzip\" \\\n  -H \"Content-Type: application/json\" \\\n  -d '{\"stream\": false, \"messages\": [{\"role\": \"user\", \"content\": \"What is the second highest mountain?\"}]}' \\\n  -H \"x-subscription-token: <YOUR_BRAVE_SEARCH_API_KEY>\" \nTest Request(post /v1/chat/completions)\n\nStatus: 200Status: 400Status: 402Status: 403Status: 404Status: 422Status: 429 Show Schema {\n  \"model\": \"brave-pro\",\n  \"system_fingerprint\": \"string\",\n  \"choices\": [\n    {\n      \"delta\": {\n        \"role\": \"assistant\",\n        \"content\": \"string\"\n      },\n      \"finish_reason\": \"stop\"\n    }\n  ],\n  \"created\": 1,\n  \"id\": \"string\",\n  \"object\": \"chat.completion.chunk\",\n  \"usage\": {\n    \"completion_tokens\": 1,\n    \"prompt_tokens\": 1,\n    \"total_tokens\": 1,\n    \"completion_tokens_details\": {\n      \"reasoning_tokens\": 1\n    }\n  }\n}\nSuccessful Response"
  suggestedFilename: "summarizer-answers"
---

# Brave Search - API

## 源URL

https://api-dashboard.search.brave.com/api-reference/summarizer/answers

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/chat/completions`

## 代码示例

### 示例 1 (bash)

```bash
curl -X POST -s --compressed "https://api.search.brave.com/res/v1/chat/completions" \
  -H "Accept: application/json" \
  -H "Accept-Encoding: gzip" \
  -H "Content-Type: application/json" \
  -d '{"stream": false, "messages": [{"role": "user", "content": "What is the second highest mountain?"}]}' \
  -H "x-subscription-token: <YOUR_BRAVE_SEARCH_API_KEY>"
```

### 示例 2 (json)

```json
{
  "model": "brave-pro",
  "system_fingerprint": "string",
  "choices": [
    {
      "delta": {
        "role": "assistant",
        "content": "string"
      },
      "finish_reason": "stop"
    }
  ],
  "created": 1,
  "id": "string",
  "object": "chat.completion.chunk",
  "usage": {
    "completion_tokens": 1,
    "prompt_tokens": 1,
    "total_tokens": 1,
    "completion_tokens_details": {
      "reasoning_tokens": 1
    }
  }
}
```

## 文档正文

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/chat/completions`

Search GET

Search POST

Local POIs GET

POI Descriptions GET

Rich search GET

LLM Context GET

LLM Context POST

Place Search GET

News GET

News POST

Videos GET

Videos POST

Images GET

Answers POST

Suggest GET

Spell check GET

Answers

API for AI-generated answers backed by real-time web search and verifiable sources

post/v1/chat/completions

messagesCopy link to messagesType: array Messages[] 1…1 required  Show UserMessagefor messages

countryCopy link to countryType: Countrydefault:  "us"

enable_citationsCopy link to enable_citationsType: Enable Citationsdefault:  false

enable_entitiesCopy link to enable_entitiesType: Enable Entitiesdefault:  false

enable_researchCopy link to enable_researchType: Enable Researchdefault:  false

languageCopy link to languageType: Languagedefault:  "en"

max_completion_tokensCopy link to max_completion_tokensType: Max Completion Tokens nullable 
Integer numbers.

Integer numbers.

metadataCopy link to metadataType: Metadata nullable  Show Metadatafor metadata

modelCopy link to modelType: Modelenumdefault:  "brave-pro"brave-probrave

brave-pro

research_allow_thinkingCopy link to research_allow_thinkingType: Research Allow Thinkingdefault:  true

research_maximum_number_of_iterationsCopy link to research_maximum_number_of_iterationsType: Research Maximum Number Of Iterationsmin:    1max:    5default:  4
Integer numbers.

research_maximum_number_of_queriesCopy link to research_maximum_number_of_queriesType: Research Maximum Number Of Queriesmin:    1max:    50default:  20
Integer numbers.

200Copy link to 200Type: OpenAIChatResponsechoicesType: array Choices[] required  Show ChoiceChunkfor choicescreatedType: Created required 
Integer numbers.
idType: Id required modelType: Modelenumdefault:  "brave-pro"brave-probraveobjectenumdefault:  "chat.completion.chunk"const:   chat.completion.chunkchat.completion.chunksystem_fingerprintType: System Fingerprint nullable usageType: OpenAIUsage nullable  Show OpenAIUsagefor usage

choicesType: array Choices[] required  Show ChoiceChunkfor choices

createdType: Created required 
Integer numbers.

idType: Id required

modelType: Modelenumdefault:  "brave-pro"brave-probrave

objectenumdefault:  "chat.completion.chunk"const:   chat.completion.chunkchat.completion.chunk

chat.completion.chunk

system_fingerprintType: System Fingerprint nullable

usageType: OpenAIUsage nullable  Show OpenAIUsagefor usage

400Copy link to 400Type: APIErrorResponseExample{
  "type": "ErrorResponse",
  "errors": [
    {
      "id": "5d832250-9396-4f6e-b84a-2a1fe524cd7d",
      "code": "OPTION_NOT_IN_PLAN",
      "detail": "The option is not subscribed in the plan.",
      "status": 400,
      "meta": {
        "component": "authentication"
      }
    }
  ],
  "time": 1663072993
}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0
Integer numbers.
typeType: Typedefault:  "ErrorResponse"

errorType: APIErrorModel required  Show APIErrorModelfor error

timeType: Timedefault:  0
Integer numbers.

typeType: Typedefault:  "ErrorResponse"

402Copy link to 402Type: APIErrorResponseExample{
  "type": "ErrorResponse",
  "errors": [
    {
      "id": "5d832250-9396-4f6e-b84a-2a1fe524cd7d",
      "code": "USAGE_LIMIT_EXCEEDED",
      "detail": "Usage limit exceeded.",
      "status": 402,
      "meta": {
        "component": "api"
      }
    }
  ],
  "time": 1663072993
}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0
Integer numbers.
typeType: Typedefault:  "ErrorResponse"

403Copy link to 403Type: APIErrorResponseExample{
  "type": "ErrorResponse",
  "errors": [
    {
      "id": "5d832250-9396-4f6e-b84a-2a1fe524cd7d",
      "code": "RESOURCE_NOT_ALLOWED",
      "detail": "The user is not authorized to access this resource.",
      "status": 403,
      "meta": {
        "component": "api"
      }
    }
  ],
  "time": 1663072993
}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0
Integer numbers.
typeType: Typedefault:  "ErrorResponse"

404Copy link to 404Type: APIErrorResponseExample{
  "type": "ErrorResponse",
  "errors": [
    {
      "id": "5d832250-9396-4f6e-b84a-2a1fe524cd7d",
      "code": "SUBSCRIPTION_NOT_FOUND",
      "detail": "No subscription found.",
      "status": 404,
      "meta": {
        "component": "subscriptions"
      }
    }
  ],
  "time": 1663072993
}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0
Integer numbers.
typeType: Typedefault:  "ErrorResponse"

422Copy link to 422Type: APIErrorResponseExample{
  "type": "ErrorResponse",
  "errors": [
    {
      "id": "5d832250-9396-4f6e-b84a-2a1fe524cd7d",
      "code": "SUBSCRIPTION_TOKEN_INVALID",
      "detail": "The provided subscription token is invalid.",
      "status": 422,
      "meta": {
        "component": "authentication"
      }
    }
  ],
  "time": 1663072993
}errorType: APIErrorModel required  Show APIErrorModelfor errortime

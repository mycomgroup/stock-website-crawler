---
id: "url-3f2b6f8d"
type: "api"
title: "Brave Search - API"
url: "https://api-dashboard.search.brave.com/api-reference/web/rich_search"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T02:31:41.808Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/web/rich?callback_key=1234567890"
  method: "GET"
  sections: []
  tables:
    - {"index":0,"headers":["Cookie Enabled","Cookie Key","Cookie Value"],"rows":[["","Key","Value"]]}
    - {"index":1,"headers":["Header Enabled","Header Key","Header Value"],"rows":[["","x-subscription-token Required","BSAkf-ialuaH0E5Fy0-xb-xCRk4_-K1"],["","api-version","Value"],["","accept","application/json"],["","cache-control","Value"],["","user-agent","Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36"],["","Key","Value"]]}
    - {"index":2,"headers":["Parameter Enabled","Parameter Key","Parameter Value"],"rows":[["","callback_key Required","Value"]]}
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/rich?callback_key=1234567890\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/rich?callback_key=1234567890\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"rich\",\n  \"results\": [],\n  \"response_callback_info\": {\n    \"vertical\": \"calculator\",\n    \"callback_key\": \"string\",\n    \"callback_status\": \"success\",\n    \"search_lang\": \"ar\"\n  }\n}"}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"rich\",\n  \"results\": [],\n  \"response_callback_info\": {\n    \"vertical\": \"calculator\",\n    \"callback_key\": \"string\",\n    \"callback_status\": \"success\",\n    \"search_lang\": \"ar\"\n  }\n}"}
  rawContent: "Search GET\n\nSearch POST\n\nLocal POIs GET\n\nPOI Descriptions GET\n\nRich search GET\n\nLLM Context GET\n\nLLM Context POST\n\nPlace Search GET\n\nNews GET\n\nNews POST\n\nVideos GET\n\nVideos POST\n\nImages GET\n\nAnswers POST\n\nSuggest GET\n\nSpell check GET\n\nRich search\n\nGets the rich realtime result for the requested resource, ie.\n  query like weather in london.\n\nThe rich result callback_key is obtained by performing first a\n  Web Search and including the enable_rich_callback=true\n  parameter in the request.\n\nRequires a Search subscription.\n\nget/v1/web/rich\n\ncallback_keyCopy link to callback_keyType: Callback Key required \nThe callback key to use for the rich header\n\nThe callback key to use for the rich header\n\nx-subscription-tokenCopy link to x-subscription-tokenType: Subscription token required ExamplesBSAkf-ialuaH0E5Fy0-xb-xCRk4_-K1BSAKfrEzjBnQc8Zs_0yCk7VvsJSO_C1BSASAwOd_FnWjNnAqRuRNCCli2yyt9UBSAaZabk4Lh4O6jq2kivx1SNqTk_uCt\nThe subscription token that was generated for the product.\n\nThe subscription token that was generated for the product.\n\napi-versionCopy link to api-versionType: API version nullable \nThe API version to use. This is denoted by the format YYYY-MM-DD. Default is the latest that is available. Read more about API versioning.\n\nThe API version to use. This is denoted by the format YYYY-MM-DD. Default is the latest that is available. Read more about API versioning.\n\nacceptCopy link to acceptType: Acceptenum\nThe default supported media type is application/json.\napplication/json*/*\n\nThe default supported media type is application/json.\n\napplication/json\n\ncache-controlCopy link to cache-controlenumconst:   no-cache\nBrave Search will return cached content by default. To prevent caching set the Cache-Control header to no-cache. This is currently done as best effort.\nno-cache\n\nBrave Search will return cached content by default. To prevent caching set the Cache-Control header to no-cache. This is currently done as best effort.\n\nno-cache\n\nuser-agentCopy link to user-agentType: User agent nullable ExamplesMozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/103.0.5060.63 Mobile/15E148 Safari/604.1Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36\nThe user agent originating the request. Brave search can utilize the user agent to provide a different experience depending on the device as described by the string. The user agent should follow the commonly used browser agent strings on each platform. For more information on curating user agents, see RFC 9110.\n\nThe user agent originating the request. Brave search can utilize the user agent to provide a different experience depending on the device as described by the string. The user agent should follow the commonly used browser agent strings on each platform. For more information on curating user agents, see RFC 9110.\n\n200Copy link to 200Type: RichHeaderResponseresponse_callback_infoType: ResponseCallbackInfo nullable  Show ResponseCallbackInfofor response_callback_inforesultsType: array Results[]default:  [] Show RichResultfor resultstypeenumdefault:  \"rich\"const:   richrich\n\nresponse_callback_infoType: ResponseCallbackInfo nullable  Show ResponseCallbackInfofor response_callback_info\n\nresultsType: array Results[]default:  [] Show RichResultfor results\n\ntypeenumdefault:  \"rich\"const:   richrich\n\n404Copy link to 404Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"SUBSCRIPTION_NOT_FOUND\",\n      \"detail\": \"No subscription found.\",\n      \"status\": 404,\n      \"meta\": {\n        \"component\": \"subscriptions\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\nerrorType: APIErrorModel required  Show APIErrorModelfor error\n\ntimeType: Timedefault:  0\nInteger numbers.\n\nInteger numbers.\n\ntypeType: Typedefault:  \"ErrorResponse\"\n\n422Copy link to 422Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"SUBSCRIPTION_TOKEN_INVALID\",\n      \"detail\": \"The provided subscription token is invalid.\",\n      \"status\": 422,\n      \"meta\": {\n        \"component\": \"authentication\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\n429Copy link to 429Type: APIErrorResponseExamples{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"RATE_LIMITED\",\n      \"detail\": \"Request rate limit exceeded for plan.\",\n      \"status\": 429,\n      \"meta\": {\n        \"component\": \"rate_limiter\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"QUOTA_LIMITED\",\n      \"detail\": \"Request quota limit exceeded for plan.\",\n      \"status\": 429,\n      \"meta\": {\n        \"component\": \"rate_limiter\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\nSuccessful Response\n\nPath Parameters\n\nCookies\n\nHeaders\n\nQuery Parameters\n\nCode Snippet (Collapsed)\n\nServer Server:https://api.search.brave.com/res\n\nRich search Operations get/v1/web/rich\n\nRequest Example for get/v1/web/richcURL curl \"https://api.search.brave.com/res/v1/web/rich?callback_key=1234567890\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\"\nTest Request(get /v1/web/rich)\n\nStatus: 200Status: 404Status: 422Status: 429 Show Schema {\n  \"type\": \"rich\",\n  \"results\": [],\n  \"response_callback_info\": {\n    \"vertical\": \"calculator\",\n    \"callback_key\": \"string\",\n    \"callback_status\": \"success\",\n    \"search_lang\": \"ar\"\n  }\n}\nSuccessful Response"
  suggestedFilename: "web-rich_search"
---

# Brave Search - API

## 源URL

https://api-dashboard.search.brave.com/api-reference/web/rich_search

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/web/rich?callback_key=1234567890`

## 代码示例

### 示例 1 (bash)

```bash
curl "https://api.search.brave.com/res/v1/web/rich?callback_key=1234567890" \
  -H "Accept: application/json" \ 
  -H "Accept-Encoding: gzip" \ 
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

### 示例 2 (json)

```json
{
  "type": "rich",
  "results": [],
  "response_callback_info": {
    "vertical": "calculator",
    "callback_key": "string",
    "callback_status": "success",
    "search_lang": "ar"
  }
}
```

## 文档正文

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/web/rich?callback_key=1234567890`

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

Rich search

Gets the rich realtime result for the requested resource, ie.
  query like weather in london.

The rich result callback_key is obtained by performing first a
  Web Search and including the enable_rich_callback=true
  parameter in the request.

Requires a Search subscription.

get/v1/web/rich

callback_keyCopy link to callback_keyType: Callback Key required 
The callback key to use for the rich header

The callback key to use for the rich header

x-subscription-tokenCopy link to x-subscription-tokenType: Subscription token required ExamplesBSAkf-ialuaH0E5Fy0-xb-xCRk4_-K1BSAKfrEzjBnQc8Zs_0yCk7VvsJSO_C1BSASAwOd_FnWjNnAqRuRNCCli2yyt9UBSAaZabk4Lh4O6jq2kivx1SNqTk_uCt
The subscription token that was generated for the product.

The subscription token that was generated for the product.

api-versionCopy link to api-versionType: API version nullable 
The API version to use. This is denoted by the format YYYY-MM-DD. Default is the latest that is available. Read more about API versioning.

The API version to use. This is denoted by the format YYYY-MM-DD. Default is the latest that is available. Read more about API versioning.

acceptCopy link to acceptType: Acceptenum
The default supported media type is application/json.
application/json*/*

The default supported media type is application/json.

application/json

cache-controlCopy link to cache-controlenumconst:   no-cache
Brave Search will return cached content by default. To prevent caching set the Cache-Control header to no-cache. This is currently done as best effort.
no-cache

Brave Search will return cached content by default. To prevent caching set the Cache-Control header to no-cache. This is currently done as best effort.

no-cache

user-agentCopy link to user-agentType: User agent nullable ExamplesMozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/103.0.5060.63 Mobile/15E148 Safari/604.1Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36
The user agent originating the request. Brave search can utilize the user agent to provide a different experience depending on the device as described by the string. The user agent should follow the commonly used browser agent strings on each platform. For more information on curating user agents, see RFC 9110.

The user agent originating the request. Brave search can utilize the user agent to provide a different experience depending on the device as described by the string. The user agent should follow the commonly used browser agent strings on each platform. For more information on curating user agents, see RFC 9110.

200Copy link to 200Type: RichHeaderResponseresponse_callback_infoType: ResponseCallbackInfo nullable  Show ResponseCallbackInfofor response_callback_inforesultsType: array Results[]default:  [] Show RichResultfor resultstypeenumdefault:  "rich"const:   richrich

response_callback_infoType: ResponseCallbackInfo nullable  Show ResponseCallbackInfofor response_callback_info

resultsType: array Results[]default:  [] Show RichResultfor results

typeenumdefault:  "rich"const:   richrich

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

errorType: APIErrorModel required  Show APIErrorModelfor error

timeType: Timedefault:  0
Integer numbers.

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
}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0
Integer numbers.
typeType: Typedefault:  "ErrorResponse"

429Copy link to 429Type: APIErrorResponseExamples{
  "type": "ErrorResponse",
  "errors": [
    {
      "id": "5d832250-9396-4f6e-b84a-2a1fe524cd7d",
      "code": "RATE_LIMITED",
      "detail": "Request

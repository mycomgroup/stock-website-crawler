---
id: "url-6d0939cb"
type: "api"
title: "Brave Search - API"
url: "https://api-dashboard.search.brave.com/api-reference/other/spell_check"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T02:32:31.206Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/spellcheck/search?q=artifial+inteligence"
  method: "GET"
  sections: []
  tables:
    - {"index":0,"headers":["Cookie Enabled","Cookie Key","Cookie Value"],"rows":[["","Key","Value"]]}
    - {"index":1,"headers":["Header Enabled","Header Key","Header Value"],"rows":[["","x-subscription-token Required","BSA_xlKz0a3BfIWOqxJdutqIwhtV2G6"],["","api-version","Value"],["","accept","application/json"],["","cache-control","Value"],["","user-agent","Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36"],["","Key","Value"]]}
    - {"index":2,"headers":["Parameter Enabled","Parameter Key","Parameter Value"],"rows":[["","q Required","Value"],["","lang","en"],["","country","US"],["","Key","Value"]]}
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/spellcheck/search?q=artifial+inteligence\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/spellcheck/search?q=artifial+inteligence\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"spellcheck\",\n  \"query\": {\n    \"original\": \"string\",\n    \"show_strict_warning\": true,\n    \"altered\": \"string\",\n    \"cleaned\": \"string\",\n    \"safesearch\": true,\n    \"is_navigational\": true,\n    \"is_geolocal\": true,\n    \"local_decision\": \"string\",\n    \"local_locations_idx\": 1,\n    \"is_trending\": true,\n    \"is_news_breaking\": true,\n    \"ask_for_location\": true,\n    \"language\": {\n      \"main\": \"string\"\n    },\n    \"spellcheck_off\": true,\n    \"country\": \"string\",\n    \"bad_results\": true,\n    \"should_fallback\": true,\n    \"lat\": \"string\",\n    \"long\": \"string\",\n    \"postal_code\": \"string\",\n    \"city\": \"string\",\n    \"header_country\": \"string\",\n    \"more_results_available\": true,\n    \"state\": \"string\",\n    \"custom_location_label\": \"string\",\n    \"reddit_cluster\": \"string\",\n    \"summary_key\": \"string\",\n    \"search_operators\": {\n      \"applied\": false,\n      \"cleaned_query\": \"string\",\n      \"sites\": [\n        \"string\"\n      ]\n    }\n  },\n  \"results\": []\n}"}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"spellcheck\",\n  \"query\": {\n    \"original\": \"string\",\n    \"show_strict_warning\": true,\n    \"altered\": \"string\",\n    \"cleaned\": \"string\",\n    \"safesearch\": true,\n    \"is_navigational\": true,\n    \"is_geolocal\": true,\n    \"local_decision\": \"string\",\n    \"local_locations_idx\": 1,\n    \"is_trending\": true,\n    \"is_news_breaking\": true,\n    \"ask_for_location\": true,\n    \"language\": {\n      \"main\": \"string\"\n    },\n    \"spellcheck_off\": true,\n    \"country\": \"string\",\n    \"bad_results\": true,\n    \"should_fallback\": true,\n    \"lat\": \"string\",\n    \"long\": \"string\",\n    \"postal_code\": \"string\",\n    \"city\": \"string\",\n    \"header_country\": \"string\",\n    \"more_results_available\": true,\n    \"state\": \"string\",\n    \"custom_location_label\": \"string\",\n    \"reddit_cluster\": \"string\",\n    \"summary_key\": \"string\",\n    \"search_operators\": {\n      \"applied\": false,\n      \"cleaned_query\": \"string\",\n      \"sites\": [\n        \"string\"\n      ]\n    }\n  },\n  \"results\": []\n}"}
  rawContent: "Search GET\n\nSearch POST\n\nLocal POIs GET\n\nPOI Descriptions GET\n\nRich search GET\n\nLLM Context GET\n\nLLM Context POST\n\nPlace Search GET\n\nNews GET\n\nNews POST\n\nVideos GET\n\nVideos POST\n\nImages GET\n\nAnswers POST\n\nSuggest GET\n\nSpell check GET\n\nSpell check\n\nIntelligent spell checking to improve query quality and help users find what they’re looking for.\n\nget/v1/spellcheck/search\n\nqCopy link to qType: Qmin length:    1max length:    400 required \nThe phrase to be spell checked. Query can not be empty. Maximum of 400 characters and 50 words in the query.\n\nThe phrase to be spell checked. Query can not be empty. Maximum of 400 characters and 50 words in the query.\n\nlangCopy link to langType: Languageenum\nThe spell check language preference, where potentially the results could come from. The 2 or more character language code for which the spell check search results are provided. This is a just a hint for calculating spell check responses.\nareubnbgca Show all values\n\nThe spell check language preference, where potentially the results could come from. The 2 or more character language code for which the spell check search results are provided. This is a just a hint for calculating spell check responses.\n\nShow all values\n\ncountryCopy link to countryType: SearchCountryenum\nThe spell check country, where potentially the results could come from. The country string is limited to 2 character country codes of supported countries. This is a just a hint for calculating spellcheck responses.\nARAUATBEBR Show all values\n\nThe spell check country, where potentially the results could come from. The country string is limited to 2 character country codes of supported countries. This is a just a hint for calculating spellcheck responses.\n\nx-subscription-tokenCopy link to x-subscription-tokenType: Subscription token required ExamplesBSA_xlKz0a3BfIWOqxJdutqIwhtV2G6BSAzr45IhgRrS8hCi8NJkhiRQ3pfOBeBSAd9YAVA1k_rJZw3PX81he9DploHaU\nThe subscription token that was generated for the product.\n\nThe subscription token that was generated for the product.\n\napi-versionCopy link to api-versionType: API version nullable \nThe API version to use. This is denoted by the format YYYY-MM-DD. Default is the latest that is available. Read more about API versioning.\n\nThe API version to use. This is denoted by the format YYYY-MM-DD. Default is the latest that is available. Read more about API versioning.\n\nacceptCopy link to acceptType: Acceptenum\nThe default supported media type is application/json.\napplication/json*/*\n\nThe default supported media type is application/json.\n\napplication/json\n\ncache-controlCopy link to cache-controlenumconst:   no-cache\nBrave Search will return cached content by default. To prevent caching set the Cache-Control header to no-cache. This is currently done as best effort.\nno-cache\n\nBrave Search will return cached content by default. To prevent caching set the Cache-Control header to no-cache. This is currently done as best effort.\n\nno-cache\n\nuser-agentCopy link to user-agentType: User agent nullable ExamplesMozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/103.0.5060.63 Mobile/15E148 Safari/604.1Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36\nThe user agent originating the request. Brave search can utilize the user agent to provide a different experience depending on the device as described by the string. The user agent should follow the commonly used browser agent strings on each platform. For more information on curating user agents, see RFC 9110.\n\nThe user agent originating the request. Brave search can utilize the user agent to provide a different experience depending on the device as described by the string. The user agent should follow the commonly used browser agent strings on each platform. For more information on curating user agents, see RFC 9110.\n\n200Copy link to 200Type: SpellCheckSearchApiResponsequeryType: Query required  Show Queryfor queryresultsType: array Results[]default:  []\nThe list of spell-checked results for given query.\n Show SpellCheckResultfor resultstypeenumdefault:  \"spellcheck\"const:   spellcheckspellcheck\n\nqueryType: Query required  Show Queryfor query\n\nresultsType: array Results[]default:  []\nThe list of spell-checked results for given query.\n Show SpellCheckResultfor results\n\nThe list of spell-checked results for given query.\n\ntypeenumdefault:  \"spellcheck\"const:   spellcheckspellcheck\n\nspellcheck\n\n404Copy link to 404Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"SUBSCRIPTION_NOT_FOUND\",\n      \"detail\": \"No subscription found.\",\n      \"status\": 404,\n      \"meta\": {\n        \"component\": \"subscriptions\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\nerrorType: APIErrorModel required  Show APIErrorModelfor error\n\ntimeType: Timedefault:  0\nInteger numbers.\n\nInteger numbers.\n\ntypeType: Typedefault:  \"ErrorResponse\"\n\n422Copy link to 422Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"SUBSCRIPTION_TOKEN_INVALID\",\n      \"detail\": \"The provided subscription token is invalid.\",\n      \"status\": 422,\n      \"meta\": {\n        \"component\": \"authentication\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\n429Copy link to 429Type: APIErrorResponseExamples{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"RATE_LIMITED\",\n      \"detail\": \"Request rate limit exceeded for plan.\",\n      \"status\": 429,\n      \"meta\": {\n        \"component\": \"rate_limiter\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"QUOTA_LIMITED\",\n      \"detail\": \"Request quota limit exceeded for plan.\",\n      \"status\": 429,\n      \"meta\": {\n        \"component\": \"rate_limiter\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\nSuccessful Response\n\nPath Parameters\n\nCookies\n\nHeaders\n\nQuery Parameters\n\nCode Snippet (Collapsed)\n\nServer Server:https://api.search.brave.com/res\n\nSpell check Operations get/v1/spellcheck/search\n\nRequest Example for get/v1/spellcheck/searchcURL curl \"https://api.search.brave.com/res/v1/spellcheck/search?q=artifial+inteligence\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\"\nTest Request(get /v1/spellcheck/search)\n\nStatus: 200Status: 404Status: 422Status: 429 Show Schema {\n  \"type\": \"spellcheck\",\n  \"query\": {\n    \"original\": \"string\",\n    \"show_strict_warning\": true,\n    \"altered\": \"string\",\n    \"cleaned\": \"string\",\n    \"safesearch\": true,\n    \"is_navigational\": true,\n    \"is_geolocal\": true,\n    \"local_decision\": \"string\",\n    \"local_locations_idx\": 1,\n    \"is_trending\": true,\n    \"is_news_breaking\": true,\n    \"ask_for_location\": true,\n    \"language\": {\n      \"main\": \"string\"\n    },\n    \"spellcheck_off\": true,\n    \"country\": \"string\",\n    \"bad_results\": true,\n    \"should_fallback\": true,\n    \"lat\": \"string\",\n    \"long\": \"string\",\n    \"postal_code\": \"string\",\n    \"city\": \"string\",\n    \"header_country\": \"string\",\n    \"more_results_available\": true,\n    \"state\": \"string\",\n    \"custom_location_label\": \"string\",\n    \"reddit_cluster\": \"string\",\n    \"summary_key\": \"string\",\n    \"search_operators\": {\n      \"applied\": false,\n      \"cleaned_query\": \"string\",\n      \"sites\": [\n        \"string\"\n      ]\n    }\n  },\n  \"results\": []\n}\nSuccessful Response"
  suggestedFilename: "other-spell_check"
---

# Brave Search - API

## 源URL

https://api-dashboard.search.brave.com/api-reference/other/spell_check

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/spellcheck/search?q=artifial+inteligence`

## 代码示例

### 示例 1 (bash)

```bash
curl "https://api.search.brave.com/res/v1/spellcheck/search?q=artifial+inteligence" \
  -H "Accept: application/json" \ 
  -H "Accept-Encoding: gzip" \ 
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

### 示例 2 (json)

```json
{
  "type": "spellcheck",
  "query": {
    "original": "string",
    "show_strict_warning": true,
    "altered": "string",
    "cleaned": "string",
    "safesearch": true,
    "is_navigational": true,
    "is_geolocal": true,
    "local_decision": "string",
    "local_locations_idx": 1,
    "is_trending": true,
    "is_news_breaking": true,
    "ask_for_location": true,
    "language": {
      "main": "string"
    },
    "spellcheck_off": true,
    "country": "string",
    "bad_results": true,
    "should_fallback": true,
    "lat": "string",
    "long": "string",
    "postal_code": "string",
    "city": "string",
    "header_country": "string",
    "more_results_available": true,
    "state": "string",
    "custom_location_label": "string",
    "reddit_cluster": "string",
    "summary_key": "string",
    "search_operators": {
      "applied": false,
      "cleaned_query": "string",
      "sites": [
        "string"
      ]
    }
  },
  "results": []
}
```

## 文档正文

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/spellcheck/search?q=artifial+inteligence`

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

Spell check

Intelligent spell checking to improve query quality and help users find what they’re looking for.

get/v1/spellcheck/search

qCopy link to qType: Qmin length:    1max length:    400 required 
The phrase to be spell checked. Query can not be empty. Maximum of 400 characters and 50 words in the query.

The phrase to be spell checked. Query can not be empty. Maximum of 400 characters and 50 words in the query.

langCopy link to langType: Languageenum
The spell check language preference, where potentially the results could come from. The 2 or more character language code for which the spell check search results are provided. This is a just a hint for calculating spell check responses.
areubnbgca Show all values

The spell check language preference, where potentially the results could come from. The 2 or more character language code for which the spell check search results are provided. This is a just a hint for calculating spell check responses.

Show all values

countryCopy link to countryType: SearchCountryenum
The spell check country, where potentially the results could come from. The country string is limited to 2 character country codes of supported countries. This is a just a hint for calculating spellcheck responses.
ARAUATBEBR Show all values

The spell check country, where potentially the results could come from. The country string is limited to 2 character country codes of supported countries. This is a just a hint for calculating spellcheck responses.

x-subscription-tokenCopy link to x-subscription-tokenType: Subscription token required ExamplesBSA_xlKz0a3BfIWOqxJdutqIwhtV2G6BSAzr45IhgRrS8hCi8NJkhiRQ3pfOBeBSAd9YAVA1k_rJZw3PX81he9DploHaU
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

200Copy link to 200Type: SpellCheckSearchApiResponsequeryType: Query required  Show Queryfor queryresultsType: array Results[]default:  []
The list of spell-checked results for given query.
 Show SpellCheckResultfor resultstypeenumdefault:  "spellcheck"const:   spellcheckspellcheck

queryType: Query required  Show Queryfor query

resultsType: array Results[]default:  []
The list of spell-checked results for given query.
 Show SpellCheckResultfor results

The list of spell-checked results for given query.

typeenumdefault:  "spellcheck"const:   spellcheckspellcheck

spellcheck

404Copy link to 404Type: APIErrorResponseExample{
  "type": "ErrorResponse",
  "errors": [
    {
      "id": "5d832250-9396-4f6e-b84a-2a1fe524cd7d",
      "code": "SUBSCRIPTION_NOT_FOUND",
      "detail": "No subscription found.",
      "status": 404,
      "meta": {
        "comp

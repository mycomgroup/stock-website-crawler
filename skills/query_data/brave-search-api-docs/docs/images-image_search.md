---
id: "url-23e89dfa"
type: "api"
title: "Brave Search - API"
url: "https://api-dashboard.search.brave.com/api-reference/images/image_search"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T02:33:09.423Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/images/search?q=mountain+landscape"
  method: "GET"
  sections: []
  tables:
    - {"index":0,"headers":["Cookie Enabled","Cookie Key","Cookie Value"],"rows":[["","Key","Value"]]}
    - {"index":1,"headers":["Header Enabled","Header Key","Header Value"],"rows":[["","x-subscription-token Required","Value"],["","api-version","Value"],["","accept","application/json"],["","cache-control","Value"],["","user-agent","Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36"],["","Key","Value"]]}
    - {"index":2,"headers":["Parameter Enabled","Parameter Key","Parameter Value"],"rows":[["","q Required","Value"],["","search_lang","en"],["","country","US"],["","safesearch","Select a value"],["","count","50"],["","spellcheck","true"],["","Key","Value"]]}
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/images/search?q=mountain+landscape\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/images/search?q=mountain+landscape\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"images\",\n  \"query\": {\n    \"original\": \"string\",\n    \"altered\": \"string\",\n    \"spellcheck_off\": true,\n    \"show_strict_warning\": true\n  },\n  \"results\": [\n    {\n      \"type\": \"image_result\",\n      \"title\": \"string\",\n      \"url\": \"string\",\n      \"source\": \"string\",\n      \"page_fetched\": \"string\",\n      \"thumbnail\": {\n        \"src\": \"string\",\n        \"width\": 1,\n        \"height\": 1\n      },\n      \"properties\": {\n        \"url\": \"string\",\n        \"placeholder\": \"string\",\n        \"width\": 1,\n        \"height\": 1\n      },\n      \"meta_url\": {\n        \"scheme\": \"string\",\n        \"netloc\": \"string\",\n        \"hostname\": \"string\",\n        \"favicon\": \"string\",\n        \"path\": \"string\"\n      },\n      \"confidence\": \"low\"\n    }\n  ],\n  \"extra\": {\n    \"might_be_offensive\": false\n  }\n}"}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"images\",\n  \"query\": {\n    \"original\": \"string\",\n    \"altered\": \"string\",\n    \"spellcheck_off\": true,\n    \"show_strict_warning\": true\n  },\n  \"results\": [\n    {\n      \"type\": \"image_result\",\n      \"title\": \"string\",\n      \"url\": \"string\",\n      \"source\": \"string\",\n      \"page_fetched\": \"string\",\n      \"thumbnail\": {\n        \"src\": \"string\",\n        \"width\": 1,\n        \"height\": 1\n      },\n      \"properties\": {\n        \"url\": \"string\",\n        \"placeholder\": \"string\",\n        \"width\": 1,\n        \"height\": 1\n      },\n      \"meta_url\": {\n        \"scheme\": \"string\",\n        \"netloc\": \"string\",\n        \"hostname\": \"string\",\n        \"favicon\": \"string\",\n        \"path\": \"string\"\n      },\n      \"confidence\": \"low\"\n    }\n  ],\n  \"extra\": {\n    \"might_be_offensive\": false\n  }\n}"}
  rawContent: "Search GET\n\nSearch POST\n\nLocal POIs GET\n\nPOI Descriptions GET\n\nRich search GET\n\nLLM Context GET\n\nLLM Context POST\n\nPlace Search GET\n\nNews GET\n\nNews POST\n\nVideos GET\n\nVideos POST\n\nImages GET\n\nAnswers POST\n\nSuggest GET\n\nSpell check GET\n\nImage search\n\nFind images from a large independent index of images.\n\nget/v1/images/search\n\nqCopy link to qType: Qmin length:    1max length:    400 required \nThe user’s search query term. Query can not be empty. Maximum of 400 characters and 50 words in the query.\n\nThe user’s search query term. Query can not be empty. Maximum of 400 characters and 50 words in the query.\n\nsearch_langCopy link to search_langType: Languageenum\nThe search language preference. The 2 or more character language code for which the search results are provided.\nareubnbgca Show all values\n\nThe search language preference. The 2 or more character language code for which the search results are provided.\n\nShow all values\n\ncountryCopy link to countryType: SearchCountryenum\nThe search query country, where the results come from. The country string is limited to 2 character country codes of supported countries and ALL for worldwide.\nARAUATBEBR Show all values\n\nThe search query country, where the results come from. The country string is limited to 2 character country codes of supported countries and ALL for worldwide.\n\nsafesearchCopy link to safesearchType: SafeSearchenum\nFilters search results for adult content. The following values are supported:\n\n\n  off - No content filtering (except for illegal content).\n  strict - Drops all adult content from search results.\n\nDefaults to strict.\noffstrict\n\nFilters search results for adult content. The following values are supported:\n\noff - No content filtering (except for illegal content).\n\nstrict - Drops all adult content from search results.\n\nDefaults to strict.\n\nstrict\n\ncountCopy link to countType: Countmin:    1max:    200default:  50\nThe number of search results returned in response. The maximum is 200. The actual number delivered may be less than requested. Defaults to 50.\n\nThe number of search results returned in response. The maximum is 200. The actual number delivered may be less than requested. Defaults to 50.\n\nspellcheckCopy link to spellcheckType: Spellcheckdefault:  trueExamplestruefalse\nWhether to spell check provided query. If the spell checker is enabled, the modified query is always used for search. The modified query can be found in altered key from the query response model.\n\nWhether to spell check provided query. If the spell checker is enabled, the modified query is always used for search. The modified query can be found in altered key from the query response model.\n\nx-subscription-tokenCopy link to x-subscription-tokenType: Subscription token required \nThe subscription token that was generated for the product.\n\nThe subscription token that was generated for the product.\n\napi-versionCopy link to api-versionType: API version nullable \nThe API version to use. This is denoted by the format YYYY-MM-DD. Default is the latest that is available. Read more about API versioning.\n\nThe API version to use. This is denoted by the format YYYY-MM-DD. Default is the latest that is available. Read more about API versioning.\n\nacceptCopy link to acceptType: Acceptenum\nThe default supported media type is application/json.\napplication/json*/*\n\nThe default supported media type is application/json.\n\napplication/json\n\ncache-controlCopy link to cache-controlenumconst:   no-cache\nBrave Search will return cached content by default. To prevent caching set the Cache-Control header to no-cache. This is currently done as best effort.\nno-cache\n\nBrave Search will return cached content by default. To prevent caching set the Cache-Control header to no-cache. This is currently done as best effort.\n\nno-cache\n\nuser-agentCopy link to user-agentType: User agent nullable ExamplesMozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/103.0.5060.63 Mobile/15E148 Safari/604.1Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36\nThe user agent originating the request. Brave search can utilize the user agent to provide a different experience depending on the device as described by the string. The user agent should follow the commonly used browser agent strings on each platform. For more information on curating user agents, see RFC 9110.\n\nThe user agent originating the request. Brave search can utilize the user agent to provide a different experience depending on the device as described by the string. The user agent should follow the commonly used browser agent strings on each platform. For more information on curating user agents, see RFC 9110.\n\n200Copy link to 200Type: ImageSearchApiResponseextraType: Extra required  Show Extrafor extraqueryType: Query required  Show Queryfor queryresultsType: array Results[] required \nThe list of image results for the given query.\n Show ImageResultfor resultstypeenumdefault:  \"images\"const:   imagesimages\n\nextraType: Extra required  Show Extrafor extra\n\nqueryType: Query required  Show Queryfor query\n\nresultsType: array Results[] required \nThe list of image results for the given query.\n Show ImageResultfor results\n\nThe list of image results for the given query.\n\ntypeenumdefault:  \"images\"const:   imagesimages\n\nimages\n\n404Copy link to 404Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"SUBSCRIPTION_NOT_FOUND\",\n      \"detail\": \"No subscription found.\",\n      \"status\": 404,\n      \"meta\": {\n        \"component\": \"subscriptions\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\nerrorType: APIErrorModel required  Show APIErrorModelfor error\n\ntimeType: Timedefault:  0\nInteger numbers.\n\nInteger numbers.\n\ntypeType: Typedefault:  \"ErrorResponse\"\n\n422Copy link to 422Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"SUBSCRIPTION_TOKEN_INVALID\",\n      \"detail\": \"The provided subscription token is invalid.\",\n      \"status\": 422,\n      \"meta\": {\n        \"component\": \"authentication\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\n429Copy link to 429Type: APIErrorResponseExamples{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"RATE_LIMITED\",\n      \"detail\": \"Request rate limit exceeded for plan.\",\n      \"status\": 429,\n      \"meta\": {\n        \"component\": \"rate_limiter\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"QUOTA_LIMITED\",\n      \"detail\": \"Request quota limit exceeded for plan.\",\n      \"status\": 429,\n      \"meta\": {\n        \"component\": \"rate_limiter\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\nSuccessful Response\n\nPath Parameters\n\nCookies\n\nHeaders\n\nQuery Parameters\n\nCode Snippet (Collapsed)\n\nServer Server:https://api.search.brave.com/res\n\nImage search Operations get/v1/images/search\n\nRequest Example for get/v1/images/searchcURL curl \"https://api.search.brave.com/res/v1/images/search?q=mountain+landscape\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\"\nTest Request(get /v1/images/search)\n\nStatus: 200Status: 404Status: 422Status: 429 Show Schema {\n  \"type\": \"images\",\n  \"query\": {\n    \"original\": \"string\",\n    \"altered\": \"string\",\n    \"spellcheck_off\": true,\n    \"show_strict_warning\": true\n  },\n  \"results\": [\n    {\n      \"type\": \"image_result\",\n      \"title\": \"string\",\n      \"url\": \"string\",\n      \"source\": \"string\",\n      \"page_fetched\": \"string\",\n      \"thumbnail\": {\n        \"src\": \"string\",\n        \"width\": 1,\n        \"height\": 1\n      },\n      \"properties\": {\n        \"url\": \"string\",\n        \"placeholder\": \"string\",\n        \"width\": 1,\n        \"height\": 1\n      },\n      \"meta_url\": {\n        \"scheme\": \"string\",\n        \"netloc\": \"string\",\n        \"hostname\": \"string\",\n        \"favicon\": \"string\",\n        \"path\": \"string\"\n      },\n      \"confidence\": \"low\"\n    }\n  ],\n  \"extra\": {\n    \"might_be_offensive\": false\n  }\n}\nSuccessful Response"
  suggestedFilename: "images-image_search"
---

# Brave Search - API

## 源URL

https://api-dashboard.search.brave.com/api-reference/images/image_search

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/images/search?q=mountain+landscape`

## 代码示例

### 示例 1 (bash)

```bash
curl "https://api.search.brave.com/res/v1/images/search?q=mountain+landscape" \
  -H "Accept: application/json" \ 
  -H "Accept-Encoding: gzip" \ 
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

### 示例 2 (json)

```json
{
  "type": "images",
  "query": {
    "original": "string",
    "altered": "string",
    "spellcheck_off": true,
    "show_strict_warning": true
  },
  "results": [
    {
      "type": "image_result",
      "title": "string",
      "url": "string",
      "source": "string",
      "page_fetched": "string",
      "thumbnail": {
        "src": "string",
        "width": 1,
        "height": 1
      },
      "properties": {
        "url": "string",
        "placeholder": "string",
        "width": 1,
        "height": 1
      },
      "meta_url": {
        "scheme": "string",
        "netloc": "string",
        "hostname": "string",
        "favicon": "string",
        "path": "string"
      },
      "confidence": "low"
    }
  ],
  "extra": {
    "might_be_offensive": false
  }
}
```

## 文档正文

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/images/search?q=mountain+landscape`

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

Image search

Find images from a large independent index of images.

get/v1/images/search

qCopy link to qType: Qmin length:    1max length:    400 required 
The user’s search query term. Query can not be empty. Maximum of 400 characters and 50 words in the query.

The user’s search query term. Query can not be empty. Maximum of 400 characters and 50 words in the query.

search_langCopy link to search_langType: Languageenum
The search language preference. The 2 or more character language code for which the search results are provided.
areubnbgca Show all values

The search language preference. The 2 or more character language code for which the search results are provided.

Show all values

countryCopy link to countryType: SearchCountryenum
The search query country, where the results come from. The country string is limited to 2 character country codes of supported countries and ALL for worldwide.
ARAUATBEBR Show all values

The search query country, where the results come from. The country string is limited to 2 character country codes of supported countries and ALL for worldwide.

safesearchCopy link to safesearchType: SafeSearchenum
Filters search results for adult content. The following values are supported:

  off - No content filtering (except for illegal content).
  strict - Drops all adult content from search results.

Defaults to strict.
offstrict

Filters search results for adult content. The following values are supported:

off - No content filtering (except for illegal content).

strict - Drops all adult content from search results.

Defaults to strict.

strict

countCopy link to countType: Countmin:    1max:    200default:  50
The number of search results returned in response. The maximum is 200. The actual number delivered may be less than requested. Defaults to 50.

The number of search results returned in response. The maximum is 200. The actual number delivered may be less than requested. Defaults to 50.

spellcheckCopy link to spellcheckType: Spellcheckdefault:  trueExamplestruefalse
Whether to spell check provided query. If the spell checker is enabled, the modified query is always used for search. The modified query can be found in altered key from the query response model.

Whether to spell check provided query. If the spell checker is enabled, the modified query is always used for search. The modified query can be found in altered key from the query response model.

x-subscription-tokenCopy link to x-subscription-tokenType: Subscription token required 
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

200Copy link to 200Type: ImageSe

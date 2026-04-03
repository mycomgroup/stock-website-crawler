---
id: "url-4f5c3dc3"
type: "api"
title: "Brave Search - API"
url: "https://api-dashboard.search.brave.com/api-reference/summarizer/llm_context/get"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T03:29:05.912Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/llm/context?q=how+deep+is+the+mediterranean+sea"
  method: "GET"
  sections: []
  tables:
    - {"index":0,"headers":["Cookie Enabled","Cookie Key","Cookie Value"],"rows":[["","Key","Value"]]}
    - {"index":1,"headers":["Header Enabled","Header Key","Header Value"],"rows":[["","x-loc-lat","Select a value"],["","x-loc-long","Select a value"],["","x-loc-city","Ann Arbor"],["","x-loc-state","MI"],["","x-loc-state-name","Michigan"],["","x-loc-country","US"],["","x-loc-postal-code","48105"],["","x-subscription-token Required","BSAzHZLCyKqYKXGrKIEESaFE9u5zQLe"],["","api-version","Value"],["","accept","application/json"],["","cache-control","Value"],["","user-agent","Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36"],["","Key","Value"]]}
    - {"index":2,"headers":["Parameter Enabled","Parameter Key","Parameter Value"],"rows":[["","q Required","Value"],["","country","US"],["","search_lang","en"],["","count","20"],["","maximum_number_of_urls","20"],["","maximum_number_of_tokens","8192"],["","maximum_number_of_snippets","50"],["","context_threshold_mode","balanced"],["","maximum_number_of_tokens_per_url","4096"],["","maximum_number_of_snippets_per_url","50"],["","goggles","https://raw.githubusercontent.com/brave/goggles-quickstart/main/goggles/hacker_news.goggle"],["","freshness","Select a value"],["","enable_local","Value"]]}
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/llm/context?q=how+deep+is+the+mediterranean+sea\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/llm/context?q=how+deep+is+the+mediterranean+sea\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"grounding\": {\n    \"generic\": [],\n    \"poi\": {\n      \"name\": \"string\",\n      \"url\": \"string\",\n      \"title\": \"string\",\n      \"snippets\": [\n        \"string\"\n      ]\n    },\n    \"map\": []\n  },\n  \"sources\": {}\n}"}
    - {"type":"response","language":"json","code":"{\n  \"grounding\": {\n    \"generic\": [],\n    \"poi\": {\n      \"name\": \"string\",\n      \"url\": \"string\",\n      \"title\": \"string\",\n      \"snippets\": [\n        \"string\"\n      ]\n    },\n    \"map\": []\n  },\n  \"sources\": {}\n}"}
  rawContent: "Search GET\n\nSearch POST\n\nLocal POIs GET\n\nPOI Descriptions GET\n\nRich search GET\n\nLLM Context GET\n\nLLM Context POST\n\nPlace Search GET\n\nNews GET\n\nNews POST\n\nVideos GET\n\nVideos POST\n\nImages GET\n\nAnswers POST\n\nSuggest GET\n\nSpell check GET\n\nLLM Context\n\nPre-extracted web content optimized for AI agents, LLM grounding, and RAG pipelines. Use this API to get the context for your LLM or AI agent.\n\nget/v1/llm/context\n\nqCopy link to qType: Qmin length:    1max length:    400 required \nThe user’s search query term. Query can not be empty. Maximum of 400 characters and 50 words in the query.\n\nThe user’s search query term. Query can not be empty. Maximum of 400 characters and 50 words in the query.\n\ncountryCopy link to countryType: SearchCountryenum\nThe search query country, where the results come from. The country string is limited to 2 character country codes of supported countries.\nARAUATBEBR Show all values\n\nThe search query country, where the results come from. The country string is limited to 2 character country codes of supported countries.\n\nShow all values\n\nsearch_langCopy link to search_langType: Languageenum\nThe search language preference. The 2 or more character language code for which the search results are provided.\nareubnbgca Show all values\n\nThe search language preference. The 2 or more character language code for which the search results are provided.\n\ncountCopy link to countType: Countmin:    1max:    50default:  20\nThe maximum number of search results considered to select the LLM context data. The default is 20 and the maximum is 50.\n\nThe maximum number of search results considered to select the LLM context data. The default is 20 and the maximum is 50.\n\nmaximum_number_of_urlsCopy link to maximum_number_of_urlsType: Maximum Number Of Urlsmin:    1max:    50default:  20\nMaximum number of different URLs to include in LLM context.\n\nMaximum number of different URLs to include in LLM context.\n\nmaximum_number_of_tokensCopy link to maximum_number_of_tokensType: Maximum Number Of Tokensmin:    1024max:    32768default:  8192\nApproximate maximum number of tokens to include in context. The default is 8192 and maximum is 32768.\n\nApproximate maximum number of tokens to include in context. The default is 8192 and maximum is 32768.\n\nmaximum_number_of_snippetsCopy link to maximum_number_of_snippetsType: Maximum Number Of Snippetsmin:    1max:    100default:  50\nMaximum number of different snippets (or chunks of text) to include in LLM context. The default is 50 and maximum is 100.\n\nMaximum number of different snippets (or chunks of text) to include in LLM context. The default is 50 and maximum is 100.\n\ncontext_threshold_modeCopy link to context_threshold_modeType: SummarizerContextThresholdModeenum\nThe mode to use to determine the threshold for including content in context. Default is balanced.\ndisabledstrictlenientbalanced\n\nThe mode to use to determine the threshold for including content in context. Default is balanced.\n\ndisabled\n\nstrict\n\nlenient\n\nbalanced\n\nmaximum_number_of_tokens_per_urlCopy link to maximum_number_of_tokens_per_urlType: Maximum Number Of Tokens Per Urlmin:    512max:    8192default:  4096\nMaximum number of tokens to include per URL. The default is 4096 and maximum is 8192.\n\nMaximum number of tokens to include per URL. The default is 4096 and maximum is 8192.\n\nmaximum_number_of_snippets_per_urlCopy link to maximum_number_of_snippets_per_urlType: Maximum Number Of Snippets Per Urlmin:    1max:    100default:  50\nMaximum number of snippets to include per URL. The default is 50 and maximum is 100.\n\nMaximum number of snippets to include per URL. The default is 50 and maximum is 100.\n\ngogglesCopy link to goggles nullable \nThe goggle url or definition to rerank search results.\nAny ofstringType: string\n\nThe goggle url or definition to rerank search results.\n\nType: string\n\nfreshnessCopy link to freshnessType: Freshnessdefault:  \"\"Examplespm2022-04-01to2022-07-30\nFilters search results by page age. The age of a page is determined by the most relevant date reported by the content, such as its published or last modified date. The following values are supported:\n\n  pd - Pages aged 24 hours or less.\n  pw - Pages aged 7 days or less.\n  pm - Pages aged 31 days or less.\n  py - Pages aged 365 days or less.\n  YYYY-MM-DDtoYYYY-MM-DD - A custom date range is also supported by specifying start and end dates e.g. 2022-04-01to2022-07-30.\n\nFilters search results by page age. The age of a page is determined by the most relevant date reported by the content, such as its published or last modified date. The following values are supported:\n\npd - Pages aged 24 hours or less.\n\npw - Pages aged 7 days or less.\n\npm - Pages aged 31 days or less.\n\npy - Pages aged 365 days or less.\n\nYYYY-MM-DDtoYYYY-MM-DD - A custom date range is also supported by specifying start and end dates e.g. 2022-04-01to2022-07-30.\n\nenable_localCopy link to enable_localType: Enable Local nullable \nWhether to enable local recall. Not setting this value means auto-detect and uses local recall if any of the localization headers are provided.\n\nWhether to enable local recall. Not setting this value means auto-detect and uses local recall if any of the localization headers are provided.\n\nx-loc-latCopy link to x-loc-latType: X-Loc-Latmin:    -90max:    90 nullable Example{}\nThe latitude of the client’s geographical location in degrees, to provide relevant local results. The latitude must be greater than or equal to -90.0 degrees and less than or equal to +90.0 degrees.\n\nThe latitude of the client’s geographical location in degrees, to provide relevant local results. The latitude must be greater than or equal to -90.0 degrees and less than or equal to +90.0 degrees.\n\nx-loc-longCopy link to x-loc-longType: X-Loc-Longmin:    -180max:    180 nullable Example{}\nThe longitude of the client’s geographical location in degrees, to provide relevant local results. The longitude must be greater than or equal to -180.0 and less than or equal to +180.0 degrees.\n\nThe longitude of the client’s geographical location in degrees, to provide relevant local results. The longitude must be greater than or equal to -180.0 and less than or equal to +180.0 degrees.\n\nx-loc-cityCopy link to x-loc-cityType: X-Loc-City nullable ExampleAnn Arbor\nThe generic name of the client city\n\nThe generic name of the client city\n\nx-loc-stateCopy link to x-loc-stateType: X-Loc-State nullable ExampleMI\nA code which could be up to three characters, that represent the client’s state/region. The region is the first-level subdivision (the broadest or least specific) of the ISO 3166-2 code.\n\nA code which could be up to three characters, that represent the client’s state/region. The region is the first-level subdivision (the broadest or least specific) of the ISO 3166-2 code.\n\nx-loc-state-nameCopy link to x-loc-state-nameType: X-Loc-State-Name nullable ExampleMichigan\nThe name of the client’s state/region. The region is the first-level subdivision (the broadest or least specific) of the ISO 3166-2 code.\n\nThe name of the client’s state/region. The region is the first-level subdivision (the broadest or least specific) of the ISO 3166-2 code.\n\nx-loc-countryCopy link to x-loc-countryType: Countryenum nullable ExampleUS\nThe two letter country code for the client’s country. For a list of country codes, see ISO 3166-1 alpha-2\nADAEAFAGAI Show all values\n\nThe two letter country code for the client’s country. For a list of country codes, see ISO 3166-1 alpha-2\n\nx-loc-postal-codeCopy link to x-loc-postal-codeType: X-Loc-Postal-Code nullable Example48105\nThe client’s postal code\n\nThe client’s postal code\n\nx-subscription-tokenCopy link to x-subscription-tokenType: Subscription token required ExampleBSAzHZLCyKqYKXGrKIEESaFE9u5zQLe\nThe subscription token that was generated for the product.\n\nThe subscription token that was generated for the product.\n\napi-versionCopy link to api-versionType: API version nullable \nThe API version to use. This is denoted by the format YYYY-MM-DD. Default is the latest that is available. Read more about API versioning.\n\nThe API version to use. This is denoted by the format YYYY-MM-DD. Default is the latest that is available. Read more about API versioning.\n\nacceptCopy link to acceptType: Acceptenum\nThe default supported media type is application/json.\napplication/json*/*\n\nThe default supported media type is application/json.\n\napplication/json\n\ncache-controlCopy link to cache-controlenumconst:   no-cache\nBrave Search will return cached content by default. To prevent caching set the Cache-Control header to no-cache. This is currently done as best effort.\nno-cache\n\nBrave Search will return cached content by default. To prevent caching set the Cache-Control header to no-cache. This is currently done as best effort.\n\nno-cache\n\nuser-agentCopy link to user-agentType: User agent nullable ExamplesMozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/103.0.5060.63 Mobile/15E148 Safari/604.1Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36\nThe user agent originating the request. Brave search can utilize the user agent to provide a different experience depending on the device as described by the string. The user agent should follow the commonly used browser agent strings on each platform. For more information on curating user agents, see RFC 9110.\n\nThe user agent originating the request. Brave search can utilize the user agent to provide a different experience depending on the device as described by the string. The user agent should follow the commonly used browser agent strings on each platform. For more information on curating user agents, see RFC 9110.\n\n200Copy link to 200Type: LLMContextAPIResponse\nResponse model for the LLM Context API (/v1/llm/context).\ngroundingType: LLMContext\nContainer for all LLM context content by type.\n Show LLMContextfor groundingsourcesType: Sourcesdefault:  {}\nMetadata for all referenced URLs, keyed by URL.\n Show Sourcesfor sources\n\nResponse model for the LLM Context API (/v1/llm/context).\n\ngroundingType: LLMContext\nContainer for all LLM context content by type.\n Show LLMContextfor grounding\n\nContainer for all LLM context content by type.\n\nsourcesType: Sourcesdefault:  {}\nMetadata for all referenced URLs, keyed by URL.\n Show Sourcesfor sources\n\nMetadata for all referenced URLs, keyed by URL.\n\n400Copy link to 400Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"OPTION_NOT_IN_PLAN\",\n      \"detail\": \"The option is not subscribed in the plan.\",\n      \"status\": 400,\n      \"meta\": {\n        \"component\": \"authentication\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\nerrorType: APIErrorModel required  Show APIErrorModelfor error\n\ntimeType: Timedefault:  0\nInteger numbers.\n\nInteger numbers.\n\ntypeType: Typedefault:  \"ErrorResponse\"\n\n403Copy link to 403Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"RESOURCE_NOT_ALLOWED\",\n      \"detail\": \"The user is not authorized to access this resource.\",\n      \"status\": 403,\n      \"meta\": {\n        \"component\": \"api\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\n404Copy link to 404Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"SUBSCRIPTION_NOT_FOUND\",\n      \"detail\": \"No subscription found.\",\n      \"status\": 404,\n      \"meta\": {\n        \"component\": \"subscriptions\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\n422Copy link to 422Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"SUBSCRIPTION_TOKEN_INVALID\",\n      \"detail\": \"The provided subscription token is invalid.\",\n      \"status\": 422,\n      \"meta\": {\n        \"component\": \"authentication\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\n429Copy link to 429Type: APIErrorResponseExamples{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"RATE_LIMITED\",\n      \"detail\": \"Request rate limit exceeded for plan.\",\n      \"status\": 429,\n      \"meta\": {\n        \"component\": \"rate_limiter\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"QUOTA_LIMITED\",\n      \"detail\": \"Request quota limit exceeded for plan.\",\n      \"status\": 429,\n      \"meta\": {\n        \"component\": \"rate_limiter\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\nSuccessful Response\n\nPath Parameters\n\nCookies\n\nHeaders\n\nQuery Parameters\n\nCode Snippet (Collapsed)\n\nServer Server:https://api.search.brave.com/res\n\nLLM Context Operations get/v1/llm/context\n\nRequest Example for get/v1/llm/contextcURL curl \"https://api.search.brave.com/res/v1/llm/context?q=how+deep+is+the+mediterranean+sea\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\"\nTest Request(get /v1/llm/context)\n\nStatus: 200Status: 400Status: 403Status: 404Status: 422Status: 429 Show Schema {\n  \"grounding\": {\n    \"generic\": [],\n    \"poi\": {\n      \"name\": \"string\",\n      \"url\": \"string\",\n      \"title\": \"string\",\n      \"snippets\": [\n        \"string\"\n      ]\n    },\n    \"map\": []\n  },\n  \"sources\": {}\n}\nSuccessful Response"
  suggestedFilename: "llm_context-get"
---

# Brave Search - API

## 源URL

https://api-dashboard.search.brave.com/api-reference/summarizer/llm_context/get

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/llm/context?q=how+deep+is+the+mediterranean+sea`

## 代码示例

### 示例 1 (bash)

```bash
curl "https://api.search.brave.com/res/v1/llm/context?q=how+deep+is+the+mediterranean+sea" \
  -H "Accept: application/json" \ 
  -H "Accept-Encoding: gzip" \ 
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

### 示例 2 (json)

```json
{
  "grounding": {
    "generic": [],
    "poi": {
      "name": "string",
      "url": "string",
      "title": "string",
      "snippets": [
        "string"
      ]
    },
    "map": []
  },
  "sources": {}
}
```

## 文档正文

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/llm/context?q=how+deep+is+the+mediterranean+sea`

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

LLM Context

Pre-extracted web content optimized for AI agents, LLM grounding, and RAG pipelines. Use this API to get the context for your LLM or AI agent.

get/v1/llm/context

qCopy link to qType: Qmin length:    1max length:    400 required 
The user’s search query term. Query can not be empty. Maximum of 400 characters and 50 words in the query.

The user’s search query term. Query can not be empty. Maximum of 400 characters and 50 words in the query.

countryCopy link to countryType: SearchCountryenum
The search query country, where the results come from. The country string is limited to 2 character country codes of supported countries.
ARAUATBEBR Show all values

The search query country, where the results come from. The country string is limited to 2 character country codes of supported countries.

Show all values

search_langCopy link to search_langType: Languageenum
The search language preference. The 2 or more character language code for which the search results are provided.
areubnbgca Show all values

The search language preference. The 2 or more character language code for which the search results are provided.

countCopy link to countType: Countmin:    1max:    50default:  20
The maximum number of search results considered to select the LLM context data. The default is 20 and the maximum is 50.

The maximum number of search results considered to select the LLM context data. The default is 20 and the maximum is 50.

maximum_number_of_urlsCopy link to maximum_number_of_urlsType: Maximum Number Of Urlsmin:    1max:    50default:  20
Maximum number of different URLs to include in LLM context.

Maximum number of different URLs to include in LLM context.

maximum_number_of_tokensCopy link to maximum_number_of_tokensType: Maximum Number Of Tokensmin:    1024max:    32768default:  8192
Approximate maximum number of tokens to include in context. The default is 8192 and maximum is 32768.

Approximate maximum number of tokens to include in context. The default is 8192 and maximum is 32768.

maximum_number_of_snippetsCopy link to maximum_number_of_snippetsType: Maximum Number Of Snippetsmin:    1max:    100default:  50
Maximum number of different snippets (or chunks of text) to include in LLM context. The default is 50 and maximum is 100.

Maximum number of different snippets (or chunks of text) to include in LLM context. The default is 50 and maximum is 100.

context_threshold_modeCopy link to context_threshold_modeType: SummarizerContextThresholdModeenum
The mode to use to determine the threshold for including content in context. Default is balanced.
disabledstrictlenientbalanced

The mode to use to determine the threshold for including content in context. Default is balanced.

disabled

strict

lenient

balanced

maximum_number_of_tokens_per_urlCopy link to maximum_number_of_tokens_per_urlType: Maximum Number Of Tokens Per Urlmin:    512max:    8192default:  4096
Maximum number of tokens to include per URL. The default is 4096 and maximum is 8192.

Maximum number of tokens to include per URL. The default is 4096 and maximum is 8192.

maximum_number_of_snippets_per_urlCopy link to maximum_number_of_snippets_per_urlType: Maximum Number Of Snippets Per Urlmin:    1max:    100default:  50
Maximum number of snippets to include per URL. The default is 50 and maximum is 100.

Maximum number of snippets to include per URL. The default is 50 and maximum is 100.

gogglesCopy link to goggles nullable 
The goggle url or definition to rerank search results.
Any ofstringType: string

The goggle url or definition to rerank search results.

Type: string

freshnessCopy link to freshnessType: Freshnessdefault:  ""Examplespm2022-04-01to2022-07-30
Filters search results by page age. The age of a page is determined by the most relevant date reported by the content, such as its published or last modified date. The following values are supported:

  pd - Pages aged 24 hours or less.
  pw - Pages aged 7 days or less.
  pm - Pages aged 31 days or less.
  py - Pages aged 365 days or less.
  YYYY-MM-DDtoYYYY-MM-DD - A custom date range is also supported by specifying start and end dates e.g. 2022-04-01to2022-07-30.

Filters search results by page age. The age of a page is determined by the most relevant date reported by the content, such as its published or last modified date. The following values are supported:

pd - Pages aged 24 hours or less.

pw - Pages aged 7 days or less.

pm - Pages aged 31 days or less.

py - Pages aged 365 days or less.

YYYY-MM-DDtoYYYY-MM-DD - A custom date range is also supported by specifying start and end dates e.g. 2022-04-01to2022-07-30.

enable_localCopy link to enable_localType: Enable Local nullable 
Whether to enable local recall. Not setting this value means au

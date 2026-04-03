---
id: "url-75e2e033"
type: "api"
title: "Brave Search - API"
url: "https://api-dashboard.search.brave.com/api-reference/videos/video_search/get"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T03:28:34.136Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/videos/search?q=machine+learning+tutorial"
  method: "GET"
  sections: []
  tables:
    - {"index":0,"headers":["Cookie Enabled","Cookie Key","Cookie Value"],"rows":[["","Key","Value"]]}
    - {"index":1,"headers":["Header Enabled","Header Key","Header Value"],"rows":[["","x-subscription-token Required","BSAf4jzyvMArBuKsqwq8mtlz6Q_IUCD"],["","api-version","Value"],["","accept","application/json"],["","cache-control","Value"],["","user-agent","Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36"],["","Key","Value"]]}
    - {"index":2,"headers":["Parameter Enabled","Parameter Key","Parameter Value"],"rows":[["","q Required","Value"],["","search_lang","en"],["","ui_lang","en-US"],["","country","US"],["","safesearch","Select a value"],["","count","20"],["","offset","0"],["","spellcheck","true"],["","freshness","Select a value"],["","include_fetch_metadata","false"],["","operators","true"],["","Key","Value"]]}
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/videos/search?q=machine+learning+tutorial\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/videos/search?q=machine+learning+tutorial\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"videos\",\n  \"query\": {\n    \"original\": \"string\",\n    \"altered\": \"string\",\n    \"cleaned\": \"string\",\n    \"spellcheck_off\": true,\n    \"show_strict_warning\": true,\n    \"search_operators\": {\n      \"applied\": false,\n      \"cleaned_query\": \"string\",\n      \"sites\": [\n        \"string\"\n      ]\n    }\n  },\n  \"results\": [],\n  \"extra\": {\n    \"might_be_offensive\": false\n  }\n}"}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"videos\",\n  \"query\": {\n    \"original\": \"string\",\n    \"altered\": \"string\",\n    \"cleaned\": \"string\",\n    \"spellcheck_off\": true,\n    \"show_strict_warning\": true,\n    \"search_operators\": {\n      \"applied\": false,\n      \"cleaned_query\": \"string\",\n      \"sites\": [\n        \"string\"\n      ]\n    }\n  },\n  \"results\": [],\n  \"extra\": {\n    \"might_be_offensive\": false\n  }\n}"}
  rawContent: "Search GET\n\nSearch POST\n\nLocal POIs GET\n\nPOI Descriptions GET\n\nRich search GET\n\nLLM Context GET\n\nLLM Context POST\n\nPlace Search GET\n\nNews GET\n\nNews POST\n\nVideos GET\n\nVideos POST\n\nImages GET\n\nAnswers POST\n\nSuggest GET\n\nSpell check GET\n\nVideo search\n\nSearch video content from a large independent index of web pages.\n\nget/v1/videos/search\n\nqCopy link to qType: Qmin length:    1max length:    400 required \nThe user’s search query term. Query can not be empty. Maximum of 400 characters and 50 words in the query.\n\nThe user’s search query term. Query can not be empty. Maximum of 400 characters and 50 words in the query.\n\nsearch_langCopy link to search_langType: Languageenum\nThe search language preference. The 2 or more character language code for which the search results are provided. Defaults to en.\nareubnbgca Show all values\n\nThe search language preference. The 2 or more character language code for which the search results are provided. Defaults to en.\n\nShow all values\n\nui_langCopy link to ui_langType: MarketCodesenum\nUser interface language preferred in response. Usually of the format <language_code>-<country_code>. For more, see RFC 9110. Defaults to en-US.\nes-ARen-AUde-ATnl-BEfr-BE Show all values\n\nUser interface language preferred in response. Usually of the format <language_code>-<country_code>. For more, see RFC 9110. Defaults to en-US.\n\ncountryCopy link to countryType: SearchCountryenum\nThe search query country, where the results come from. The country string is limited to 2 character country codes of supported countries or ALL for worldwide. Defaults to US.\nARAUATBEBR Show all values\n\nThe search query country, where the results come from. The country string is limited to 2 character country codes of supported countries or ALL for worldwide. Defaults to US.\n\nsafesearchCopy link to safesearchType: SafeSearchenum\nFilters search results for adult content. The following values are supported:\n\n\n  off - No filtering is done.\n  moderate - Filters explicit content, like images and videos, but allows adult domains in the search results.\n  strict - Drops all adult content from search results.\n\nDefaults to moderate.\noffmoderatestrict\n\nFilters search results for adult content. The following values are supported:\n\noff - No filtering is done.\n\nmoderate - Filters explicit content, like images and videos, but allows adult domains in the search results.\n\nstrict - Drops all adult content from search results.\n\nDefaults to moderate.\n\nmoderate\n\nstrict\n\ncountCopy link to countType: Countmin:    1max:    50default:  20\nThe number of search results returned in response. The maximum is 50. The actual number delivered may be less than requested. Combine this parameter with offset to paginate search results. Defaults to 20.\n\nThe number of search results returned in response. The maximum is 50. The actual number delivered may be less than requested. Combine this parameter with offset to paginate search results. Defaults to 20.\n\noffsetCopy link to offsetType: Offsetmin:    0max:    9default:  0\nThe zero based offset that indicates number of search results per page (count) to skip before returning the result. The maximum is 9. The actual number delivered may be less than requested based on the query. In order to paginate results use this parameter together with count. For example, if your user interface displays 20 search results per page, set count to 20 and offset to 0 to show the first page of results. To get subsequent pages, increment offset by 1 (e.g. 0, 1, 2). The results may overlap across multiple pages.\n\nThe zero based offset that indicates number of search results per page (count) to skip before returning the result. The maximum is 9. The actual number delivered may be less than requested based on the query. In order to paginate results use this parameter together with count. For example, if your user interface displays 20 search results per page, set count to 20 and offset to 0 to show the first page of results. To get subsequent pages, increment offset by 1 (e.g. 0, 1, 2). The results may overlap across multiple pages.\n\nspellcheckCopy link to spellcheckType: Spellcheckdefault:  trueExamplestruefalse\nWhether to spell check the provided query. If the spellchecker is enabled, the modified query is always used for search. The modified query can be found in altered key from the query response model. Defaults to true.\n\nWhether to spell check the provided query. If the spellchecker is enabled, the modified query is always used for search. The modified query can be found in altered key from the query response model. Defaults to true.\n\nfreshnessCopy link to freshnessType: Freshnessdefault:  \"\"Examplespm2022-04-01to2022-07-30\nFilters search results by page age. The age of a page is determined by the most relevant date reported by the content, such as its published or last modified date. The following values are supported:\n\n  pd - Pages aged 24 hours or less.\n  pw - Pages aged 7 days or less.\n  pm - Pages aged 31 days or less.\n  py - Pages aged 365 days or less.\n  YYYY-MM-DDtoYYYY-MM-DD - A custom date range is also supported by specifying start and end dates e.g. 2022-04-01to2022-07-30.\n\nFilters search results by page age. The age of a page is determined by the most relevant date reported by the content, such as its published or last modified date. The following values are supported:\n\npd - Pages aged 24 hours or less.\n\npw - Pages aged 7 days or less.\n\npm - Pages aged 31 days or less.\n\npy - Pages aged 365 days or less.\n\nYYYY-MM-DDtoYYYY-MM-DD - A custom date range is also supported by specifying start and end dates e.g. 2022-04-01to2022-07-30.\n\ninclude_fetch_metadataCopy link to include_fetch_metadataType: Include Fetch Metadatadefault:  falseExamplestruefalse\nInclude fetch metadata. Defaults to false.\n\nInclude fetch metadata. Defaults to false.\n\noperatorsCopy link to operatorsType: Operatorsdefault:  trueExamplestruefalse\nWhether to apply search operators. Defaults to true.\n\nWhether to apply search operators. Defaults to true.\n\nx-subscription-tokenCopy link to x-subscription-tokenType: Subscription token required ExampleBSAf4jzyvMArBuKsqwq8mtlz6Q_IUCD\nThe subscription token that was generated for the product.\n\nThe subscription token that was generated for the product.\n\napi-versionCopy link to api-versionType: API version nullable \nThe API version to use. This is denoted by the format YYYY-MM-DD. Default is the latest that is available. Read more about API versioning.\n\nThe API version to use. This is denoted by the format YYYY-MM-DD. Default is the latest that is available. Read more about API versioning.\n\nacceptCopy link to acceptType: Acceptenum\nThe default supported media type is application/json.\napplication/json*/*\n\nThe default supported media type is application/json.\n\napplication/json\n\ncache-controlCopy link to cache-controlenumconst:   no-cache\nBrave Search will return cached content by default. To prevent caching set the Cache-Control header to no-cache. This is currently done as best effort.\nno-cache\n\nBrave Search will return cached content by default. To prevent caching set the Cache-Control header to no-cache. This is currently done as best effort.\n\nno-cache\n\nuser-agentCopy link to user-agentType: User agent nullable ExamplesMozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/103.0.5060.63 Mobile/15E148 Safari/604.1Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36\nThe user agent originating the request. Brave search can utilize the user agent to provide a different experience depending on the device as described by the string. The user agent should follow the commonly used browser agent strings on each platform. For more information on curating user agents, see RFC 9110.\n\nThe user agent originating the request. Brave search can utilize the user agent to provide a different experience depending on the device as described by the string. The user agent should follow the commonly used browser agent strings on each platform. For more information on curating user agents, see RFC 9110.\n\n200Copy link to 200Type: VideoSearchApiResponseextraType: Extra required  Show Extrafor extraqueryType: Query required  Show Queryfor queryresultsType: array Results[]default:  []\nThe list of video results for the given query.\n Show VideoResultfor resultstypeenumdefault:  \"videos\"const:   videosvideos\n\nextraType: Extra required  Show Extrafor extra\n\nqueryType: Query required  Show Queryfor query\n\nresultsType: array Results[]default:  []\nThe list of video results for the given query.\n Show VideoResultfor results\n\nThe list of video results for the given query.\n\ntypeenumdefault:  \"videos\"const:   videosvideos\n\nvideos\n\n404Copy link to 404Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"SUBSCRIPTION_NOT_FOUND\",\n      \"detail\": \"No subscription found.\",\n      \"status\": 404,\n      \"meta\": {\n        \"component\": \"subscriptions\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\nerrorType: APIErrorModel required  Show APIErrorModelfor error\n\ntimeType: Timedefault:  0\nInteger numbers.\n\nInteger numbers.\n\ntypeType: Typedefault:  \"ErrorResponse\"\n\n422Copy link to 422Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"SUBSCRIPTION_TOKEN_INVALID\",\n      \"detail\": \"The provided subscription token is invalid.\",\n      \"status\": 422,\n      \"meta\": {\n        \"component\": \"authentication\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\n429Copy link to 429Type: APIErrorResponseExamples{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"RATE_LIMITED\",\n      \"detail\": \"Request rate limit exceeded for plan.\",\n      \"status\": 429,\n      \"meta\": {\n        \"component\": \"rate_limiter\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"QUOTA_LIMITED\",\n      \"detail\": \"Request quota limit exceeded for plan.\",\n      \"status\": 429,\n      \"meta\": {\n        \"component\": \"rate_limiter\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\nSuccessful Response\n\nPath Parameters\n\nCookies\n\nHeaders\n\nQuery Parameters\n\nCode Snippet (Collapsed)\n\nServer Server:https://api.search.brave.com/res\n\nVideo search Operations get/v1/videos/search\n\nRequest Example for get/v1/videos/searchcURL curl \"https://api.search.brave.com/res/v1/videos/search?q=machine+learning+tutorial\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\"\nTest Request(get /v1/videos/search)\n\nStatus: 200Status: 404Status: 422Status: 429 Show Schema {\n  \"type\": \"videos\",\n  \"query\": {\n    \"original\": \"string\",\n    \"altered\": \"string\",\n    \"cleaned\": \"string\",\n    \"spellcheck_off\": true,\n    \"show_strict_warning\": true,\n    \"search_operators\": {\n      \"applied\": false,\n      \"cleaned_query\": \"string\",\n      \"sites\": [\n        \"string\"\n      ]\n    }\n  },\n  \"results\": [],\n  \"extra\": {\n    \"might_be_offensive\": false\n  }\n}\nSuccessful Response"
  suggestedFilename: "video_search-get"
---

# Brave Search - API

## 源URL

https://api-dashboard.search.brave.com/api-reference/videos/video_search/get

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/videos/search?q=machine+learning+tutorial`

## 代码示例

### 示例 1 (bash)

```bash
curl "https://api.search.brave.com/res/v1/videos/search?q=machine+learning+tutorial" \
  -H "Accept: application/json" \ 
  -H "Accept-Encoding: gzip" \ 
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

### 示例 2 (json)

```json
{
  "type": "videos",
  "query": {
    "original": "string",
    "altered": "string",
    "cleaned": "string",
    "spellcheck_off": true,
    "show_strict_warning": true,
    "search_operators": {
      "applied": false,
      "cleaned_query": "string",
      "sites": [
        "string"
      ]
    }
  },
  "results": [],
  "extra": {
    "might_be_offensive": false
  }
}
```

## 文档正文

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/videos/search?q=machine+learning+tutorial`

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

Video search

Search video content from a large independent index of web pages.

get/v1/videos/search

qCopy link to qType: Qmin length:    1max length:    400 required 
The user’s search query term. Query can not be empty. Maximum of 400 characters and 50 words in the query.

The user’s search query term. Query can not be empty. Maximum of 400 characters and 50 words in the query.

search_langCopy link to search_langType: Languageenum
The search language preference. The 2 or more character language code for which the search results are provided. Defaults to en.
areubnbgca Show all values

The search language preference. The 2 or more character language code for which the search results are provided. Defaults to en.

Show all values

ui_langCopy link to ui_langType: MarketCodesenum
User interface language preferred in response. Usually of the format <language_code>-<country_code>. For more, see RFC 9110. Defaults to en-US.
es-ARen-AUde-ATnl-BEfr-BE Show all values

User interface language preferred in response. Usually of the format <language_code>-<country_code>. For more, see RFC 9110. Defaults to en-US.

countryCopy link to countryType: SearchCountryenum
The search query country, where the results come from. The country string is limited to 2 character country codes of supported countries or ALL for worldwide. Defaults to US.
ARAUATBEBR Show all values

The search query country, where the results come from. The country string is limited to 2 character country codes of supported countries or ALL for worldwide. Defaults to US.

safesearchCopy link to safesearchType: SafeSearchenum
Filters search results for adult content. The following values are supported:

  off - No filtering is done.
  moderate - Filters explicit content, like images and videos, but allows adult domains in the search results.
  strict - Drops all adult content from search results.

Defaults to moderate.
offmoderatestrict

Filters search results for adult content. The following values are supported:

off - No filtering is done.

moderate - Filters explicit content, like images and videos, but allows adult domains in the search results.

strict - Drops all adult content from search results.

Defaults to moderate.

moderate

strict

countCopy link to countType: Countmin:    1max:    50default:  20
The number of search results returned in response. The maximum is 50. The actual number delivered may be less than requested. Combine this parameter with offset to paginate search results. Defaults to 20.

The number of search results returned in response. The maximum is 50. The actual number delivered may be less than requested. Combine this parameter with offset to paginate search results. Defaults to 20.

offsetCopy link to offsetType: Offsetmin:    0max:    9default:  0
The zero based offset that indicates number of search results per page (count) to skip before returning the result. The maximum is 9. The actual number delivered may be less than requested based on the query. In order to paginate results use this parameter together with count. For example, if your user interface displays 20 search results per page, set count to 20 and offset to 0 to show the first page of results. To get subsequent pages, increment offset by 1 (e.g. 0, 1, 2). The results may overlap across multiple pages.

The zero based offset that indicates number of search results per page (count) to skip before returning the result. The maximum is 9. The actual number delivered may be less than requested based on the query. In order to paginate results use this parameter together with count. For example, if your user interface displays 20 search results per page, set count to 20 and offset to 0 to show the first page of results. To get subsequent pages, increment offset by 1 (e.g. 0, 1, 2). The results may overlap across multiple pages.

spellcheckCopy link to spellcheckType: Spellcheckdefault:  trueExamplestruefalse
Whether to spell check the provided query. If the spellchecker is enabled, the modified query is always used for search. The modified query can be found in altered key from the query response model. Defaults to true.

Whether to spell check the provided query. If the spellchecker is enabled, the modified query is always used for search. The modified query can be found in altered key from the query response model. Defaults to true.

freshnessCopy link to freshnessType: Freshnessdefault:  ""Examplespm2022-04-01to2022-07-30
Filters search results by page age. The age of a page is determined by the most relevant date reported by the content, such as its published or last modified date. The following values are supported:

  pd - Pages aged 24 hours or less.
  pw - Pages aged 7 days or less.
  pm - Pages aged 31 days or less.
  py -

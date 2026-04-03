---
id: "url-5f81a128"
type: "api"
title: "Brave Search - API"
url: "https://api-dashboard.search.brave.com/api-reference/web/place_search"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T02:32:09.305Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/local/place_search?q=coffee+shops&latitude=37.7749&longitude=-122.4194&radius=1000"
  method: "GET"
  sections: []
  tables:
    - {"index":0,"headers":["Cookie Enabled","Cookie Key","Cookie Value"],"rows":[["","Key","Value"]]}
    - {"index":1,"headers":["Header Enabled","Header Key","Header Value"],"rows":[["","x-subscription-token Required","BSAiLTtSPqyco-PVB42TvydabSM8FtQ"],["","api-version","Value"],["","accept","application/json"],["","cache-control","Value"],["","user-agent","Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36"],["","Key","Value"]]}
    - {"index":2,"headers":["Parameter Enabled","Parameter Key","Parameter Value"],"rows":[["","q","Value"],["","latitude","Value"],["","longitude","Value"],["","location","Value"],["","radius","Value"],["","count","20"],["","country","US"],["","search_lang","en"],["","ui_lang","en-US"],["","units","metric"],["","safesearch","strict"],["","spellcheck","true"],["","geoloc","Value"]]}
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/local/place_search?q=coffee+shops&latitude=37.7749&longitude=-122.4194&radius=1000\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/local/place_search?q=coffee+shops&latitude=37.7749&longitude=-122.4194&radius=1000\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"locations\",\n  \"query\": {\n    \"original\": \"string\",\n    \"altered\": \"string\",\n    \"spellcheck_off\": true,\n    \"show_strict_warning\": true\n  },\n  \"results\": [\n    {\n      \"title\": \"string\",\n      \"url\": \"string\",\n      \"is_source_local\": false,\n      \"is_source_both\": false,\n      \"description\": \"\",\n      \"page_age\": \"string\",\n      \"page_fetched\": \"string\",\n      \"fetched_content_timestamp\": 1,\n      \"profile\": {\n        \"name\": \"string\",\n        \"url\": \"string\",\n        \"long_name\": \"string\",\n        \"img\": \"string\"\n      },\n      \"language\": \"string\",\n      \"family_friendly\": true,\n      \"type\": \"location_result\",\n      \"provider_url\": \"string\",\n      \"coordinates\": [],\n      \"zoom_level\": 7,\n      \"thumbnail\": {\n        \"src\": \"string\",\n        \"alt\": \"string\",\n        \"height\": 1,\n        \"width\": 1,\n        \"bg_color\": \"string\",\n        \"original\": \"string\",\n        \"logo\": true,\n        \"duplicated\": true,\n        \"theme\": \"string\"\n      },\n      \"postal_address\": {\n        \"type\": \"PostalAddress\",\n        \"country\": \"string\",\n        \"postalCode\": \"string\",\n        \"streetAddress\": \"string\",\n        \"addressRegion\": \"string\",\n        \"addressLocality\": \"string\",\n        \"displayAddress\": \"string\"\n      },\n      \"opening_hours\": {\n        \"current_day\": [\n          {\n            \"abbr_name\": \"string\",\n            \"full_name\": \"string\",\n            \"opens\": \"string\",\n            \"closes\": \"string\"\n          }\n        ],\n        \"days\": [\n          [\n            {\n              \"abbr_name\": \"string\",\n              \"full_name\": \"string\",\n              \"opens\": \"string\",\n              \"closes\": \"string\"\n            }\n          ]\n        ]\n      },\n      \"contact\": {\n        \"email\": \"string\",\n        \"telephone\": \"string\"\n      },\n      \"price_range\": \"string\",\n      \"rating\": {\n        \"ratingValue\": 0,\n        \"bestRating\": 1,\n        \"reviewCount\": 1,\n        \"profile\": {\n          \"name\": \"string\",\n          \"url\": \"string\",\n          \"long_name\": \"string\",\n          \"img\": \"string\"\n        },\n        \"is_tripadvisor\": false\n      },\n      \"distance\": {\n        \"value\": 1,\n        \"units\": \"string\"\n      },\n      \"profiles\": [\n        {\n          \"type\": \"external\",\n          \"name\": \"string\",\n          \"url\": \"string\",\n          \"long_name\": \"string\",\n          \"img\": \"string\"\n        }\n      ],\n      \"reviews\": {\n        \"results\": [\n          {\n            \"title\": \"string\",\n            \"description\": \"string\",\n            \"date\": \"string\",\n            \"rating\": {\n              \"ratingValue\": 0,\n              \"bestRating\": 1,\n              \"reviewCount\": 1,\n              \"profile\": {\n                \"name\": \"string\",\n                \"url\": \"string\",\n                \"long_name\": \"string\",\n                \"img\": \"string\"\n              },\n              \"is_tripadvisor\": false\n            },\n            \"author\": {\n              \"type\": \"person\",\n              \"name\": \"string\",\n              \"url\": \"string\",\n              \"thumbnail\": {\n                \"src\": \"string\",\n                \"alt\": \"string\",\n                \"height\": 1,\n                \"width\": 1,\n                \"bg_color\": \"string\",\n                \"original\": \"string\",\n                \"logo\": true,\n                \"duplicated\": true,\n                \"theme\": \"string\"\n              },\n              \"email\": \"string\"\n            },\n            \"review_url\": \"string\",\n            \"language\": \"string\"\n          }\n        ],\n        \"viewMoreUrl\": \"string\",\n        \"reviews_in_foreign_language\": true\n      },\n      \"pictures\": {\n        \"viewMoreUrl\": \"string\",\n        \"results\": [\n          {\n            \"src\": \"string\",\n            \"alt\": \"string\",\n            \"height\": 1,\n            \"width\": 1,\n            \"bg_color\": \"string\",\n            \"original\": \"string\",\n            \"logo\": true,\n            \"duplicated\": true,\n            \"theme\": \"string\"\n          }\n        ]\n      },\n      \"action\": {\n        \"type\": \"string\",\n        \"url\": \"string\"\n      },\n      \"serves_cuisine\": [\n        \"string\"\n      ],\n      \"categories\": [],\n      \"icon_category\": \"string\",\n      \"timezone\": \"string\",\n      \"timezone_offset\": 1,\n      \"id\": \"string\",\n      \"results\": [\n        {\n          \"title\": \"string\",\n          \"url\": \"string\",\n          \"is_source_local\": false,\n          \"is_source_both\": false,\n          \"description\": \"\",\n          \"page_age\": \"string\",\n          \"page_fetched\": \"string\",\n          \"fetched_content_timestamp\": 1,\n          \"profile\": {\n            \"name\": \"string\",\n            \"url\": \"string\",\n            \"long_name\": \"string\",\n            \"img\": \"string\"\n          },\n          \"language\": \"string\",\n          \"...\": \"[Additional Properties Truncated]\"\n        }\n      ]\n    }\n  ],\n  \"location\": {\n    \"coordinates\": [],\n    \"name\": \"string\",\n    \"country\": \"string\"\n  }\n}"}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"locations\",\n  \"query\": {\n    \"original\": \"string\",\n    \"altered\": \"string\",\n    \"spellcheck_off\": true,\n    \"show_strict_warning\": true\n  },\n  \"results\": [\n    {\n      \"title\": \"string\",\n      \"url\": \"string\",\n      \"is_source_local\": false,\n      \"is_source_both\": false,\n      \"description\": \"\",\n      \"page_age\": \"string\",\n      \"page_fetched\": \"string\",\n      \"fetched_content_timestamp\": 1,\n      \"profile\": {\n        \"name\": \"string\",\n        \"url\": \"string\",\n        \"long_name\": \"string\",\n        \"img\": \"string\"\n      },\n      \"language\": \"string\",\n      \"family_friendly\": true,\n      \"type\": \"location_result\",\n      \"provider_url\": \"string\",\n      \"coordinates\": [],\n      \"zoom_level\": 7,\n      \"thumbnail\": {\n        \"src\": \"string\",\n        \"alt\": \"string\",\n        \"height\": 1,\n        \"width\": 1,\n        \"bg_color\": \"string\",\n        \"original\": \"string\",\n        \"logo\": true,\n        \"duplicated\": true,\n        \"theme\": \"string\"\n      },\n      \"postal_address\": {\n        \"type\": \"PostalAddress\",\n        \"country\": \"string\",\n        \"postalCode\": \"string\",\n        \"streetAddress\": \"string\",\n        \"addressRegion\": \"string\",\n        \"addressLocality\": \"string\",\n        \"displayAddress\": \"string\"\n      },\n      \"opening_hours\": {\n        \"current_day\": [\n          {\n            \"abbr_name\": \"string\",\n            \"full_name\": \"string\",\n            \"opens\": \"string\",\n            \"closes\": \"string\"\n          }\n        ],\n        \"days\": [\n          [\n            {\n              \"abbr_name\": \"string\",\n              \"full_name\": \"string\",\n              \"opens\": \"string\",\n              \"closes\": \"string\"\n            }\n          ]\n        ]\n      },\n      \"contact\": {\n        \"email\": \"string\",\n        \"telephone\": \"string\"\n      },\n      \"price_range\": \"string\",\n      \"rating\": {\n        \"ratingValue\": 0,\n        \"bestRating\": 1,\n        \"reviewCount\": 1,\n        \"profile\": {\n          \"name\": \"string\",\n          \"url\": \"string\",\n          \"long_name\": \"string\",\n          \"img\": \"string\"\n        },\n        \"is_tripadvisor\": false\n      },\n      \"distance\": {\n        \"value\": 1,\n        \"units\": \"string\"\n      },\n      \"profiles\": [\n        {\n          \"type\": \"external\",\n          \"name\": \"string\",\n          \"url\": \"string\",\n          \"long_name\": \"string\",\n          \"img\": \"string\"\n        }\n      ],\n      \"reviews\": {\n        \"results\": [\n          {\n            \"title\": \"string\",\n            \"description\": \"string\",\n            \"date\": \"string\",\n            \"rating\": {\n              \"ratingValue\": 0,\n              \"bestRating\": 1,\n              \"reviewCount\": 1,\n              \"profile\": {\n                \"name\": \"string\",\n                \"url\": \"string\",\n                \"long_name\": \"string\",\n                \"img\": \"string\"\n              },\n              \"is_tripadvisor\": false\n            },\n            \"author\": {\n              \"type\": \"person\",\n              \"name\": \"string\",\n              \"url\": \"string\",\n              \"thumbnail\": {\n                \"src\": \"string\",\n                \"alt\": \"string\",\n                \"height\": 1,\n                \"width\": 1,\n                \"bg_color\": \"string\",\n                \"original\": \"string\",\n                \"logo\": true,\n                \"duplicated\": true,\n                \"theme\": \"string\"\n              },\n              \"email\": \"string\"\n            },\n            \"review_url\": \"string\",\n            \"language\": \"string\"\n          }\n        ],\n        \"viewMoreUrl\": \"string\",\n        \"reviews_in_foreign_language\": true\n      },\n      \"pictures\": {\n        \"viewMoreUrl\": \"string\",\n        \"results\": [\n          {\n            \"src\": \"string\",\n            \"alt\": \"string\",\n            \"height\": 1,\n            \"width\": 1,\n            \"bg_color\": \"string\",\n            \"original\": \"string\",\n            \"logo\": true,\n            \"duplicated\": true,\n            \"theme\": \"string\"\n          }\n        ]\n      },\n      \"action\": {\n        \"type\": \"string\",\n        \"url\": \"string\"\n      },\n      \"serves_cuisine\": [\n        \"string\"\n      ],\n      \"categories\": [],\n      \"icon_category\": \"string\",\n      \"timezone\": \"string\",\n      \"timezone_offset\": 1,\n      \"id\": \"string\",\n      \"results\": [\n        {\n          \"title\": \"string\",\n          \"url\": \"string\",\n          \"is_source_local\": false,\n          \"is_source_both\": false,\n          \"description\": \"\",\n          \"page_age\": \"string\",\n          \"page_fetched\": \"string\",\n          \"fetched_content_timestamp\": 1,\n          \"profile\": {\n            \"name\": \"string\",\n            \"url\": \"string\",\n            \"long_name\": \"string\",\n            \"img\": \"string\"\n          },\n          \"language\": \"string\",\n          \"...\": \"[Additional Properties Truncated]\"\n        }\n      ]\n    }\n  ],\n  \"location\": {\n    \"coordinates\": [],\n    \"name\": \"string\",\n    \"country\": \"string\"\n  }\n}"}
  rawContent: "Search GET\n\nSearch POST\n\nLocal POIs GET\n\nPOI Descriptions GET\n\nRich search GET\n\nLLM Context GET\n\nLLM Context POST\n\nPlace Search GET\n\nNews GET\n\nNews POST\n\nVideos GET\n\nVideos POST\n\nImages GET\n\nAnswers POST\n\nSuggest GET\n\nSpell check GET\n\nPlace search\n\nSearch for points of interest in an area. If no q is provided, the endpoint will return general points of interest in the given area.\n\nget/v1/local/place_search\n\nqCopy link to qType: Qdefault:  \"\"\nQuery string to search for points of interest in an area. If no q is provided, the endpoint will return general points of interest in the given area.\n\nQuery string to search for points of interest in an area. If no q is provided, the endpoint will return general points of interest in the given area.\n\nlatitudeCopy link to latitudeType: Latitudemin:    -90max:    90 nullable \nLatitude of the geographical coordinates.\n\nLatitude of the geographical coordinates.\n\nlongitudeCopy link to longitudeType: Longitudemin:    -180max:    180 nullable \nLongitude of the geographical coordinates.\n\nLongitude of the geographical coordinates.\n\nlocationCopy link to locationType: Location nullable \n\n  Location string to search for points of interest in an area.\n  This is alternative to the latitude and longitude parameters.\n\n\n  For locations in US prefer the form <city> <state> <country name>, ie. san francisco ca united states\n  For non-US locations, use the form <city> <country name>, ie. tokyo japan\n  No need for commas or other special chars, capitalization does not matter\n  We cover multiple languages: nueva york instead of new york works, but using English or the most popular language on the target city should work the best\n\nLocation string to search for points of interest in an area.\n  This is alternative to the latitude and longitude parameters.\n\nFor locations in US prefer the form <city> <state> <country name>, ie. san francisco ca united states\n\nFor non-US locations, use the form <city> <country name>, ie. tokyo japan\n\nNo need for commas or other special chars, capitalization does not matter\n\nWe cover multiple languages: nueva york instead of new york works, but using English or the most popular language on the target city should work the best\n\nradiusCopy link to radiusType: Radiusmin:    0 nullable \nSearch radius around the given coordinates, in meters. Search is performed globally if no radius is provided.\n\nSearch radius around the given coordinates, in meters. Search is performed globally if no radius is provided.\n\ncountCopy link to countType: Countmin:    1max:    50default:  20\nNumber of results to return. The maximum is 50.\n\nNumber of results to return. The maximum is 50.\n\ncountryCopy link to countryType: SearchCountryenum\nTwo-letter country code (ISO 3166-1 alpha-2) to scope the search.\nARAUATBEBR Show all values\n\nTwo-letter country code (ISO 3166-1 alpha-2) to scope the search.\n\nShow all values\n\nsearch_langCopy link to search_langType: Languageenum\nLanguage for the search results.\nareubnbgca Show all values\n\nLanguage for the search results.\n\nui_langCopy link to ui_langType: MarketCodesenum\nUser interface language for the response. Usually <language>-<region>.\nes-ARen-AUde-ATnl-BEfr-BE Show all values\n\nUser interface language for the response. Usually <language>-<region>.\n\nunitsCopy link to unitsType: MeasurementUnitenum\nUnits of measurement for distance values.\nimperialmetric\n\nUnits of measurement for distance values.\n\nimperial\n\nmetric\n\nsafesearchCopy link to safesearchType: SafeSearchenum\nSafe search level for the query results.\noffmoderatestrict\n\nSafe search level for the query results.\n\nmoderate\n\nstrict\n\nspellcheckCopy link to spellcheckType: Spellcheckdefault:  true\nWhether to apply spellcheck before executing the search.\n\nWhether to apply spellcheck before executing the search.\n\ngeolocCopy link to geolocType: Geoloc nullable \nOptional geolocation token used to refine results.\n\nOptional geolocation token used to refine results.\n\nx-subscription-tokenCopy link to x-subscription-tokenType: Subscription token required ExamplesBSAiLTtSPqyco-PVB42TvydabSM8FtQBSACrXt_kYO67c13l-E0cZz1qkoz4Nh\nThe subscription token that was generated for the product.\n\nThe subscription token that was generated for the product.\n\napi-versionCopy link to api-versionType: API version nullable \nThe API version to use. This is denoted by the format YYYY-MM-DD. Default is the latest that is available. Read more about API versioning.\n\nThe API version to use. This is denoted by the format YYYY-MM-DD. Default is the latest that is available. Read more about API versioning.\n\nacceptCopy link to acceptType: Acceptenum\nThe default supported media type is application/json.\napplication/json*/*\n\nThe default supported media type is application/json.\n\napplication/json\n\ncache-controlCopy link to cache-controlenumconst:   no-cache\nBrave Search will return cached content by default. To prevent caching set the Cache-Control header to no-cache. This is currently done as best effort.\nno-cache\n\nBrave Search will return cached content by default. To prevent caching set the Cache-Control header to no-cache. This is currently done as best effort.\n\nno-cache\n\nuser-agentCopy link to user-agentType: User agent nullable ExamplesMozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/103.0.5060.63 Mobile/15E148 Safari/604.1Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36\nThe user agent originating the request. Brave search can utilize the user agent to provide a different experience depending on the device as described by the string. The user agent should follow the commonly used browser agent strings on each platform. For more information on curating user agents, see RFC 9110.\n\nThe user agent originating the request. Brave search can utilize the user agent to provide a different experience depending on the device as described by the string. The user agent should follow the commonly used browser agent strings on each platform. For more information on curating user agents, see RFC 9110.\n\n200Copy link to 200Type: LocalPlaceSearchApiResponselocationType: Location nullable \nA location\n Show Locationfor locationqueryType: Query nullable \nThe query object containing the original and potentially spell-corrected query.\n Show Queryfor queryresultsType: array Results[] nullable \nThe list of location results for the given query and area.\n\nA result that is location relevant.\n Show LocationResultfor resultstypeenumdefault:  \"locations\"const:   locationslocations\n\nlocationType: Location nullable \nA location\n Show Locationfor location\n\nA location\n\nqueryType: Query nullable \nThe query object containing the original and potentially spell-corrected query.\n Show Queryfor query\n\nThe query object containing the original and potentially spell-corrected query.\n\nresultsType: array Results[] nullable \nThe list of location results for the given query and area.\n\nA result that is location relevant.\n Show LocationResultfor results\n\nThe list of location results for the given query and area.\n\nA result that is location relevant.\n\ntypeenumdefault:  \"locations\"const:   locationslocations\n\nlocations\n\n400Copy link to 400Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"OPTION_NOT_IN_PLAN\",\n      \"detail\": \"The option is not subscribed in the plan.\",\n      \"status\": 400,\n      \"meta\": {\n        \"component\": \"authentication\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\nerrorType: APIErrorModel required  Show APIErrorModelfor error\n\ntimeType: Timedefault:  0\nInteger numbers.\n\nInteger numbers.\n\ntypeType: Typedefault:  \"ErrorResponse\"\n\n404Copy link to 404Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"SUBSCRIPTION_NOT_FOUND\",\n      \"detail\": \"No subscription found.\",\n      \"status\": 404,\n      \"meta\": {\n        \"component\": \"subscriptions\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\n422Copy link to 422Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"SUBSCRIPTION_TOKEN_INVALID\",\n      \"detail\": \"The provided subscription token is invalid.\",\n      \"status\": 422,\n      \"meta\": {\n        \"component\": \"authentication\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\n429Copy link to 429Type: APIErrorResponseExamples{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"RATE_LIMITED\",\n      \"detail\": \"Request rate limit exceeded for plan.\",\n      \"status\": 429,\n      \"meta\": {\n        \"component\": \"rate_limiter\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"QUOTA_LIMITED\",\n      \"detail\": \"Request quota limit exceeded for plan.\",\n      \"status\": 429,\n      \"meta\": {\n        \"component\": \"rate_limiter\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\nSuccessful Response\n\nPath Parameters\n\nCookies\n\nHeaders\n\nQuery Parameters\n\nCode Snippet (Collapsed)\n\nServer Server:https://api.search.brave.com/res\n\nPlace search Operations get/v1/local/place_search\n\nRequest Example for get/v1/local/place_searchcURL curl \"https://api.search.brave.com/res/v1/local/place_search?q=coffee+shops&latitude=37.7749&longitude=-122.4194&radius=1000\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\"\nTest Request(get /v1/local/place_search)\n\nStatus: 200Status: 400Status: 404Status: 422Status: 429 Show Schema"
  suggestedFilename: "web-place_search"
---

# Brave Search - API

## 源URL

https://api-dashboard.search.brave.com/api-reference/web/place_search

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/local/place_search?q=coffee+shops&latitude=37.7749&longitude=-122.4194&radius=1000`

## 代码示例

### 示例 1 (bash)

```bash
curl "https://api.search.brave.com/res/v1/local/place_search?q=coffee+shops&latitude=37.7749&longitude=-122.4194&radius=1000" \
  -H "Accept: application/json" \ 
  -H "Accept-Encoding: gzip" \ 
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

### 示例 2 (json)

```json
{
  "type": "locations",
  "query": {
    "original": "string",
    "altered": "string",
    "spellcheck_off": true,
    "show_strict_warning": true
  },
  "results": [
    {
      "title": "string",
      "url": "string",
      "is_source_local": false,
      "is_source_both": false,
      "description": "",
      "page_age": "string",
      "page_fetched": "string",
      "fetched_content_timestamp": 1,
      "profile": {
        "name": "string",
        "url": "string",
        "long_name": "string",
        "img": "string"
      },
      "language": "string",
      "family_friendly": true,
      "type": "location_result",
      "provider_url": "string",
      "coordinates": [],
      "zoom_level": 7,
      "thumbnail": {
        "src": "string",
        "alt": "string",
        "height": 1,
        "width": 1,
        "bg_color": "string",
        "original": "string",
        "logo": true,
        "duplicated": true,
        "theme": "string"
      },
      "postal_address": {
        "type": "PostalAddress",
        "country": "string",
        "postalCode": "string",
        "streetAddress": "string",
        "addressRegion": "string",
        "addressLocality": "string",
        "displayAddress": "string"
      },
      "opening_hours": {
        "current_day": [
          {
            "abbr_name": "string",
            "full_name": "string",
            "opens": "string",
            "closes": "string"
          }
        ],
        "days": [
          [
            {
              "abbr_name": "string",
              "full_name": "string",
              "opens": "string",
              "closes": "string"
            }
          ]
        ]
      },
      "contact": {
        "email": "string",
        "telephone": "string"
      },
      "price_range": "string",
      "rating": {
        "ratingValue": 0,
        "bestRating": 1,
        "reviewCount": 1,
        "profile": {
          "name": "string",
          "url": "string",
          "long_name": "string",
          "img": "string"
        },
        "is_tripadvisor": false
      },
      "distance": {
        "value": 1,
        "units": "string"
      },
      "profiles": [
        {
          "type": "external",
          "name": "string",
          "url": "string",
          "long_name": "string",
          "img": "string"
        }
      ],
      "reviews": {
        "results": [
          {
            "title": "string",
            "description": "string",
            "date": "string",
            "rating": {
              "ratingValue": 0,
              "bestRating": 1,
              "reviewCount": 1,
              "profile": {
                "name": "string",
                "url": "string",
                "long_name": "string",
                "img": "string"
              },
              "is_tripadvisor": false
            },
            "author": {
              "type": "person",
              "name": "string",
              "url": "string",
              "thumbnail": {
                "src": "string",
                "alt": "string",
                "height": 1,
                "width": 1,
                "bg_color": "string",
                "original": "string",
                "logo": true,
                "duplicated": true,
                "theme": "string"
              },
              "email": "string"
            },
            "review_url": "string",
            "language": "string"
          }
        ],
        "viewMoreUrl": "string",
        "reviews_in_foreign_language": true
      },
      "pictures": {
        "viewMoreUrl": "string",
        "results": [
          {
            "src": "string",
            "alt": "string",
            "height": 1,
            "width": 1,
            "bg_color": "string",
            "original": "string",
            "logo": true,
            "duplicated": true,
            "theme": "string"
          }
        ]
      },
      "action": {
        "type": "string",
        "url": "string"
      },
      "serves_cuisine": [
        "string"
      ],
      "categories": [],
      "icon_category": "string",
      "timezone": "string",
      "timezone_offset": 1,
      "id": "string",
      "results": [
        {
          "title": "string",
          "url": "string",
          "is_source_local": false,
          "is_source_both": false,
          "description": "",
          "page_age": "string",
          "page_fetched": "string",
          "fetched_content_timestamp": 1,
          "profile": {
            "name": "string",
            "url": "string",
            "long_name": "string",
            "img": "string"
          },
          "language": "string",
          "...": "[Additional Properties Truncated]"
        }
      ]
    }
  ],
  "location": {
    "coordinates": [],
    "name": "string",
    "country": "string"
  }
}
```

## 文档正文

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/local/place_search?q=coffee+shops&latitude=37.7749&longitude=-122.4194&radius=1000`

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

Place search

Search for points of interest in an area. If no q is provided, the endpoint will return general points of interest in the given area.

get/v1/local/place_search

qCopy link to qType: Qdefault:  ""
Query string to search for points of interest in an area. If no q is provided, the endpoint will return general points of interest in the given area.

Query string to search for points of interest in an area. If no q is provided, the endpoint will return general points of interest in the given area.

latitudeCopy link to latitudeType: Latitudemin:    -90max:    90 nullable 
Latitude of the geographical coordinates.

Latitude of the geographical coordinates.

longitudeCopy link to longitudeType: Longitudemin:    -180max:    180 nullable 
Longitude of the geographical coordinates.

Longitude of the geographical coordinates.

locationCopy link to locationType: Location nullable 

  Location string to search for points of interest in an area.
  This is alternative to the latitude and longitude parameters.

  For locations in US prefer the form <city> <state> <country name>, ie. san francisco ca united states
  For non-US locations, use the form <city> <country name>, ie. tokyo japan
  No need for commas or other special chars, capitalization does not matter
  We cover multiple languages: nueva york instead of new york works, but using English or the most popular language on the target city should work the best

Location string to search for points of interest in an area.
  This is alternative to the latitude and longitude parameters.

For locations in US prefer the form <city> <state> <country name>, ie. san francisco ca united states

For non-US locations, use the form <city> <country name>, ie. tokyo japan

No need for commas or other special chars, capitalization does not matter

We cover multiple languages: nueva york instead of new york works, but using English or the most popular language on the target city should work the best

radiusCopy link to radiusType: Radiusmin:    0 nullable 
Search radius around the given coordinates, in meters. Search is performed globally if no radius is provided.

Search radius around the given coordinates, in meters. Search is performed globally if no radius is provided.

countCopy link to countType: Countmin:    1max:    50default:  20
Number of results to return. The maximum is 50.

Number of results to return. The maximum is 50.

countryCopy link to countryType: SearchCountryenum
Two-letter country code (ISO 3166-1 alpha-2) to scope the search.
ARAUATBEBR Show all values

Two-letter country code (ISO 3166-1 alpha-2) to scope the search.

Show all values

search_langCopy link to search_langType: Languageenum
Language for the search results.
areubnbgca Show all values

Language for the search results.

ui_langCopy link to ui_langType: MarketCodesenum
User interface language for the response. Usually <language>-<region>.
es-ARen-AUde-ATnl-BEfr-BE Show all values

User interface language for the response. Usually <language>-<region>.

unitsCopy link to unitsType: MeasurementUnitenum
Units of measurement for distance values.
imperialmetric

Units of measurement for distance values.

imperial

metric

safesearchCopy link to safesearchType: SafeSearchenum
Safe search level for the query results.
offmoderatestrict

Safe search level for the query results.

moderate

strict

spellcheckCopy link to spellcheckType: Spellcheckdefault:  true
Whether to apply spellcheck before executing the search.

Whether to apply spellcheck before executing the search.

geolocCopy link to geolocType: Geoloc nullable 
Optional geolocation token used to refine results.

Optional geolocation token used to refine results.

x-subscription-tokenCopy link to x-subscription-tokenType: Subscription token required ExamplesBSAiLTtSPqyco-PVB42TvydabSM8FtQBSACrXt_kYO67c13l-E0cZz1qkoz4Nh
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

Brave Search will return cach

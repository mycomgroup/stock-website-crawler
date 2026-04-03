---
id: "url-165474b5"
type: "api"
title: "Brave Search - API"
url: "https://api-dashboard.search.brave.com/api-reference/web/local_pois"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T02:31:36.258Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/local/pois?ids=loc4FNMQJNOOCVHEB7UBOLN354ZYIDIYJ3RPRETERRY%3D"
  method: "GET"
  sections: []
  tables:
    - {"index":0,"headers":["Cookie Enabled","Cookie Key","Cookie Value"],"rows":[["","Key","Value"]]}
    - {"index":1,"headers":["Header Enabled","Header Key","Header Value"],"rows":[["","x-loc-lat","Value"],["","x-loc-long","Value"],["","x-subscription-token Required","Value"],["","api-version","Value"],["","accept","application/json"],["","cache-control","Value"],["","user-agent","Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36"],["","Key","Value"]]}
    - {"index":2,"headers":["Parameter Enabled","Parameter Key","Parameter Value"],"rows":[["","ids Required","Value"],["","search_lang","en"],["","ui_lang","en-US"],["","units","metric"],["","Key","Value"]]}
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/local/pois?ids=loc4FNMQJNOOCVHEB7UBOLN354ZYIDIYJ3RPRETERRY%3D\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/local/pois?ids=loc4FNMQJNOOCVHEB7UBOLN354ZYIDIYJ3RPRETERRY%3D\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"local_pois\",\n  \"results\": [\n    {\n      \"title\": \"string\",\n      \"url\": \"string\",\n      \"is_source_local\": false,\n      \"is_source_both\": false,\n      \"description\": \"\",\n      \"page_age\": \"string\",\n      \"page_fetched\": \"string\",\n      \"fetched_content_timestamp\": 1,\n      \"profile\": {\n        \"name\": \"string\",\n        \"url\": \"string\",\n        \"long_name\": \"string\",\n        \"img\": \"string\"\n      },\n      \"language\": \"string\",\n      \"family_friendly\": true,\n      \"type\": \"location_result\",\n      \"provider_url\": \"string\",\n      \"coordinates\": [],\n      \"zoom_level\": 7,\n      \"thumbnail\": {\n        \"src\": \"string\",\n        \"alt\": \"string\",\n        \"height\": 1,\n        \"width\": 1,\n        \"bg_color\": \"string\",\n        \"original\": \"string\",\n        \"logo\": true,\n        \"duplicated\": true,\n        \"theme\": \"string\"\n      },\n      \"postal_address\": {\n        \"type\": \"PostalAddress\",\n        \"country\": \"string\",\n        \"postalCode\": \"string\",\n        \"streetAddress\": \"string\",\n        \"addressRegion\": \"string\",\n        \"addressLocality\": \"string\",\n        \"displayAddress\": \"string\"\n      },\n      \"opening_hours\": {\n        \"current_day\": [\n          {\n            \"abbr_name\": \"string\",\n            \"full_name\": \"string\",\n            \"opens\": \"string\",\n            \"closes\": \"string\"\n          }\n        ],\n        \"days\": [\n          [\n            {\n              \"abbr_name\": \"string\",\n              \"full_name\": \"string\",\n              \"opens\": \"string\",\n              \"closes\": \"string\"\n            }\n          ]\n        ]\n      },\n      \"contact\": {\n        \"email\": \"string\",\n        \"telephone\": \"string\"\n      },\n      \"price_range\": \"string\",\n      \"rating\": {\n        \"ratingValue\": 0,\n        \"bestRating\": 1,\n        \"reviewCount\": 1,\n        \"profile\": {\n          \"name\": \"string\",\n          \"url\": \"string\",\n          \"long_name\": \"string\",\n          \"img\": \"string\"\n        },\n        \"is_tripadvisor\": false\n      },\n      \"distance\": {\n        \"value\": 1,\n        \"units\": \"string\"\n      },\n      \"profiles\": [\n        {\n          \"type\": \"external\",\n          \"name\": \"string\",\n          \"url\": \"string\",\n          \"long_name\": \"string\",\n          \"img\": \"string\"\n        }\n      ],\n      \"reviews\": {\n        \"results\": [\n          {\n            \"title\": \"string\",\n            \"description\": \"string\",\n            \"date\": \"string\",\n            \"rating\": {\n              \"ratingValue\": 0,\n              \"bestRating\": 1,\n              \"reviewCount\": 1,\n              \"profile\": {\n                \"name\": \"string\",\n                \"url\": \"string\",\n                \"long_name\": \"string\",\n                \"img\": \"string\"\n              },\n              \"is_tripadvisor\": false\n            },\n            \"author\": {\n              \"type\": \"person\",\n              \"name\": \"string\",\n              \"url\": \"string\",\n              \"thumbnail\": {\n                \"src\": \"string\",\n                \"alt\": \"string\",\n                \"height\": 1,\n                \"width\": 1,\n                \"bg_color\": \"string\",\n                \"original\": \"string\",\n                \"logo\": true,\n                \"duplicated\": true,\n                \"theme\": \"string\"\n              },\n              \"email\": \"string\"\n            },\n            \"review_url\": \"string\",\n            \"language\": \"string\"\n          }\n        ],\n        \"viewMoreUrl\": \"string\",\n        \"reviews_in_foreign_language\": true\n      },\n      \"pictures\": {\n        \"viewMoreUrl\": \"string\",\n        \"results\": [\n          {\n            \"src\": \"string\",\n            \"alt\": \"string\",\n            \"height\": 1,\n            \"width\": 1,\n            \"bg_color\": \"string\",\n            \"original\": \"string\",\n            \"logo\": true,\n            \"duplicated\": true,\n            \"theme\": \"string\"\n          }\n        ]\n      },\n      \"action\": {\n        \"type\": \"string\",\n        \"url\": \"string\"\n      },\n      \"serves_cuisine\": [\n        \"string\"\n      ],\n      \"categories\": [],\n      \"icon_category\": \"string\",\n      \"timezone\": \"string\",\n      \"timezone_offset\": 1,\n      \"id\": \"string\",\n      \"results\": [\n        {\n          \"title\": \"string\",\n          \"url\": \"string\",\n          \"is_source_local\": false,\n          \"is_source_both\": false,\n          \"description\": \"\",\n          \"page_age\": \"string\",\n          \"page_fetched\": \"string\",\n          \"fetched_content_timestamp\": 1,\n          \"profile\": {\n            \"name\": \"string\",\n            \"url\": \"string\",\n            \"long_name\": \"string\",\n            \"img\": \"string\"\n          },\n          \"language\": \"string\",\n          \"...\": \"[Additional Properties Truncated]\"\n        }\n      ]\n    }\n  ]\n}"}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"local_pois\",\n  \"results\": [\n    {\n      \"title\": \"string\",\n      \"url\": \"string\",\n      \"is_source_local\": false,\n      \"is_source_both\": false,\n      \"description\": \"\",\n      \"page_age\": \"string\",\n      \"page_fetched\": \"string\",\n      \"fetched_content_timestamp\": 1,\n      \"profile\": {\n        \"name\": \"string\",\n        \"url\": \"string\",\n        \"long_name\": \"string\",\n        \"img\": \"string\"\n      },\n      \"language\": \"string\",\n      \"family_friendly\": true,\n      \"type\": \"location_result\",\n      \"provider_url\": \"string\",\n      \"coordinates\": [],\n      \"zoom_level\": 7,\n      \"thumbnail\": {\n        \"src\": \"string\",\n        \"alt\": \"string\",\n        \"height\": 1,\n        \"width\": 1,\n        \"bg_color\": \"string\",\n        \"original\": \"string\",\n        \"logo\": true,\n        \"duplicated\": true,\n        \"theme\": \"string\"\n      },\n      \"postal_address\": {\n        \"type\": \"PostalAddress\",\n        \"country\": \"string\",\n        \"postalCode\": \"string\",\n        \"streetAddress\": \"string\",\n        \"addressRegion\": \"string\",\n        \"addressLocality\": \"string\",\n        \"displayAddress\": \"string\"\n      },\n      \"opening_hours\": {\n        \"current_day\": [\n          {\n            \"abbr_name\": \"string\",\n            \"full_name\": \"string\",\n            \"opens\": \"string\",\n            \"closes\": \"string\"\n          }\n        ],\n        \"days\": [\n          [\n            {\n              \"abbr_name\": \"string\",\n              \"full_name\": \"string\",\n              \"opens\": \"string\",\n              \"closes\": \"string\"\n            }\n          ]\n        ]\n      },\n      \"contact\": {\n        \"email\": \"string\",\n        \"telephone\": \"string\"\n      },\n      \"price_range\": \"string\",\n      \"rating\": {\n        \"ratingValue\": 0,\n        \"bestRating\": 1,\n        \"reviewCount\": 1,\n        \"profile\": {\n          \"name\": \"string\",\n          \"url\": \"string\",\n          \"long_name\": \"string\",\n          \"img\": \"string\"\n        },\n        \"is_tripadvisor\": false\n      },\n      \"distance\": {\n        \"value\": 1,\n        \"units\": \"string\"\n      },\n      \"profiles\": [\n        {\n          \"type\": \"external\",\n          \"name\": \"string\",\n          \"url\": \"string\",\n          \"long_name\": \"string\",\n          \"img\": \"string\"\n        }\n      ],\n      \"reviews\": {\n        \"results\": [\n          {\n            \"title\": \"string\",\n            \"description\": \"string\",\n            \"date\": \"string\",\n            \"rating\": {\n              \"ratingValue\": 0,\n              \"bestRating\": 1,\n              \"reviewCount\": 1,\n              \"profile\": {\n                \"name\": \"string\",\n                \"url\": \"string\",\n                \"long_name\": \"string\",\n                \"img\": \"string\"\n              },\n              \"is_tripadvisor\": false\n            },\n            \"author\": {\n              \"type\": \"person\",\n              \"name\": \"string\",\n              \"url\": \"string\",\n              \"thumbnail\": {\n                \"src\": \"string\",\n                \"alt\": \"string\",\n                \"height\": 1,\n                \"width\": 1,\n                \"bg_color\": \"string\",\n                \"original\": \"string\",\n                \"logo\": true,\n                \"duplicated\": true,\n                \"theme\": \"string\"\n              },\n              \"email\": \"string\"\n            },\n            \"review_url\": \"string\",\n            \"language\": \"string\"\n          }\n        ],\n        \"viewMoreUrl\": \"string\",\n        \"reviews_in_foreign_language\": true\n      },\n      \"pictures\": {\n        \"viewMoreUrl\": \"string\",\n        \"results\": [\n          {\n            \"src\": \"string\",\n            \"alt\": \"string\",\n            \"height\": 1,\n            \"width\": 1,\n            \"bg_color\": \"string\",\n            \"original\": \"string\",\n            \"logo\": true,\n            \"duplicated\": true,\n            \"theme\": \"string\"\n          }\n        ]\n      },\n      \"action\": {\n        \"type\": \"string\",\n        \"url\": \"string\"\n      },\n      \"serves_cuisine\": [\n        \"string\"\n      ],\n      \"categories\": [],\n      \"icon_category\": \"string\",\n      \"timezone\": \"string\",\n      \"timezone_offset\": 1,\n      \"id\": \"string\",\n      \"results\": [\n        {\n          \"title\": \"string\",\n          \"url\": \"string\",\n          \"is_source_local\": false,\n          \"is_source_both\": false,\n          \"description\": \"\",\n          \"page_age\": \"string\",\n          \"page_fetched\": \"string\",\n          \"fetched_content_timestamp\": 1,\n          \"profile\": {\n            \"name\": \"string\",\n            \"url\": \"string\",\n            \"long_name\": \"string\",\n            \"img\": \"string\"\n          },\n          \"language\": \"string\",\n          \"...\": \"[Additional Properties Truncated]\"\n        }\n      ]\n    }\n  ]\n}"}
  rawContent: "Search GET\n\nSearch POST\n\nLocal POIs GET\n\nPOI Descriptions GET\n\nRich search GET\n\nLLM Context GET\n\nLLM Context POST\n\nPlace Search GET\n\nNews GET\n\nNews POST\n\nVideos GET\n\nVideos POST\n\nImages GET\n\nAnswers POST\n\nSuggest GET\n\nSpell check GET\n\nLocal POIs\n\nget/v1/local/pois\n\nidsCopy link to idsType: array Ids[] 1…20 required \nA list of unique identifiers for the location. The ids are valid only for 8 hours.\n\nA list of unique identifiers for the location. The ids are valid only for 8 hours.\n\nsearch_langCopy link to search_langType: Languageenum\nThe search language preference. The 2 or more character language code for which the search results are provided.\nareubnbgca Show all values\n\nThe search language preference. The 2 or more character language code for which the search results are provided.\n\nShow all values\n\nui_langCopy link to ui_langType: MarketCodesenum\nUser interface language preferred in response. Usually of the format <language_code>-<country_code>. For more, see RFC 9110.\nes-ARen-AUde-ATnl-BEfr-BE Show all values\n\nUser interface language preferred in response. Usually of the format <language_code>-<country_code>. For more, see RFC 9110.\n\nunitsCopy link to unitsType: MeasurementUnitenum nullable Examplesmetricimperial\nThe measurement units. The following values are supported:\n\n  metric - The standardized measurement system (km, celcius…)\n  imperial - The British Imperial system of units (mile, fahrenheit…)\n\nimperialmetric\n\nThe measurement units. The following values are supported:\n\nmetric - The standardized measurement system (km, celcius…)\n\nimperial - The British Imperial system of units (mile, fahrenheit…)\n\nimperial\n\nmetric\n\nx-loc-latCopy link to x-loc-latType: X-Loc-Latmin:    -90max:    90 nullable \nThe latitude of the client’s geographical location in degrees, to provide relevant local results. The latitude must be greater than or equal to -90.0 degrees and less than or equal to +90.0 degrees.\n\nThe latitude of the client’s geographical location in degrees, to provide relevant local results. The latitude must be greater than or equal to -90.0 degrees and less than or equal to +90.0 degrees.\n\nx-loc-longCopy link to x-loc-longType: X-Loc-Longmin:    -180max:    180 nullable \nThe longitude of the client’s geographical location in degrees, to provide relevant local results. The longitude must be greater than or equal to -180.0 and less than or equal to +180.0 degrees.\n\nThe longitude of the client’s geographical location in degrees, to provide relevant local results. The longitude must be greater than or equal to -180.0 and less than or equal to +180.0 degrees.\n\nx-subscription-tokenCopy link to x-subscription-tokenType: Subscription token required \nThe subscription token that was generated for the product.\n\nThe subscription token that was generated for the product.\n\napi-versionCopy link to api-versionType: API version nullable \nThe API version to use. This is denoted by the format YYYY-MM-DD. Default is the latest that is available. Read more about API versioning.\n\nThe API version to use. This is denoted by the format YYYY-MM-DD. Default is the latest that is available. Read more about API versioning.\n\nacceptCopy link to acceptType: Acceptenum\nThe default supported media type is application/json.\napplication/json*/*\n\nThe default supported media type is application/json.\n\napplication/json\n\ncache-controlCopy link to cache-controlenumconst:   no-cache\nBrave Search will return cached content by default. To prevent caching set the Cache-Control header to no-cache. This is currently done as best effort.\nno-cache\n\nBrave Search will return cached content by default. To prevent caching set the Cache-Control header to no-cache. This is currently done as best effort.\n\nno-cache\n\nuser-agentCopy link to user-agentType: User agent nullable ExamplesMozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/103.0.5060.63 Mobile/15E148 Safari/604.1Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36\nThe user agent originating the request. Brave search can utilize the user agent to provide a different experience depending on the device as described by the string. The user agent should follow the commonly used browser agent strings on each platform. For more information on curating user agents, see RFC 9110.\n\nThe user agent originating the request. Brave search can utilize the user agent to provide a different experience depending on the device as described by the string. The user agent should follow the commonly used browser agent strings on each platform. For more information on curating user agents, see RFC 9110.\n\n200Copy link to 200Type: LocalPoiSearchApiResponseresultsType: array Results[] nullable \nThe list of location results (POIs) for the given location identifiers.\n Show Child Attributesfor resultstypeenumdefault:  \"local_pois\"const:   local_poislocal_pois\n\nresultsType: array Results[] nullable \nThe list of location results (POIs) for the given location identifiers.\n Show Child Attributesfor results\n\nThe list of location results (POIs) for the given location identifiers.\n\ntypeenumdefault:  \"local_pois\"const:   local_poislocal_pois\n\nlocal_pois\n\n400Copy link to 400Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"OPTION_NOT_IN_PLAN\",\n      \"detail\": \"The option is not subscribed in the plan.\",\n      \"status\": 400,\n      \"meta\": {\n        \"component\": \"authentication\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\nerrorType: APIErrorModel required  Show APIErrorModelfor error\n\ntimeType: Timedefault:  0\nInteger numbers.\n\nInteger numbers.\n\ntypeType: Typedefault:  \"ErrorResponse\"\n\n404Copy link to 404Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"SUBSCRIPTION_NOT_FOUND\",\n      \"detail\": \"No subscription found.\",\n      \"status\": 404,\n      \"meta\": {\n        \"component\": \"subscriptions\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\n422Copy link to 422Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"SUBSCRIPTION_TOKEN_INVALID\",\n      \"detail\": \"The provided subscription token is invalid.\",\n      \"status\": 422,\n      \"meta\": {\n        \"component\": \"authentication\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\n429Copy link to 429Type: APIErrorResponseExamples{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"RATE_LIMITED\",\n      \"detail\": \"Request rate limit exceeded for plan.\",\n      \"status\": 429,\n      \"meta\": {\n        \"component\": \"rate_limiter\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"QUOTA_LIMITED\",\n      \"detail\": \"Request quota limit exceeded for plan.\",\n      \"status\": 429,\n      \"meta\": {\n        \"component\": \"rate_limiter\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\nSuccessful Response\n\nPath Parameters\n\nCookies\n\nHeaders\n\nQuery Parameters\n\nCode Snippet (Collapsed)\n\nServer Server:https://api.search.brave.com/res\n\nLocal POIs Operations get/v1/local/pois\n\nRequest Example for get/v1/local/poiscURL curl \"https://api.search.brave.com/res/v1/local/pois?ids=loc4FNMQJNOOCVHEB7UBOLN354ZYIDIYJ3RPRETERRY%3D\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\"\nTest Request(get /v1/local/pois)\n\nStatus: 200Status: 400Status: 404Status: 422Status: 429 Show Schema"
  suggestedFilename: "web-local_pois"
---

# Brave Search - API

## 源URL

https://api-dashboard.search.brave.com/api-reference/web/local_pois

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/local/pois?ids=loc4FNMQJNOOCVHEB7UBOLN354ZYIDIYJ3RPRETERRY%3D`

## 代码示例

### 示例 1 (bash)

```bash
curl "https://api.search.brave.com/res/v1/local/pois?ids=loc4FNMQJNOOCVHEB7UBOLN354ZYIDIYJ3RPRETERRY%3D" \
  -H "Accept: application/json" \ 
  -H "Accept-Encoding: gzip" \ 
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

### 示例 2 (json)

```json
{
  "type": "local_pois",
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
  ]
}
```

## 文档正文

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/local/pois?ids=loc4FNMQJNOOCVHEB7UBOLN354ZYIDIYJ3RPRETERRY%3D`

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

Local POIs

get/v1/local/pois

idsCopy link to idsType: array Ids[] 1…20 required 
A list of unique identifiers for the location. The ids are valid only for 8 hours.

A list of unique identifiers for the location. The ids are valid only for 8 hours.

search_langCopy link to search_langType: Languageenum
The search language preference. The 2 or more character language code for which the search results are provided.
areubnbgca Show all values

The search language preference. The 2 or more character language code for which the search results are provided.

Show all values

ui_langCopy link to ui_langType: MarketCodesenum
User interface language preferred in response. Usually of the format <language_code>-<country_code>. For more, see RFC 9110.
es-ARen-AUde-ATnl-BEfr-BE Show all values

User interface language preferred in response. Usually of the format <language_code>-<country_code>. For more, see RFC 9110.

unitsCopy link to unitsType: MeasurementUnitenum nullable Examplesmetricimperial
The measurement units. The following values are supported:

  metric - The standardized measurement system (km, celcius…)
  imperial - The British Imperial system of units (mile, fahrenheit…)

imperialmetric

The measurement units. The following values are supported:

metric - The standardized measurement system (km, celcius…)

imperial - The British Imperial system of units (mile, fahrenheit…)

imperial

metric

x-loc-latCopy link to x-loc-latType: X-Loc-Latmin:    -90max:    90 nullable 
The latitude of the client’s geographical location in degrees, to provide relevant local results. The latitude must be greater than or equal to -90.0 degrees and less than or equal to +90.0 degrees.

The latitude of the client’s geographical location in degrees, to provide relevant local results. The latitude must be greater than or equal to -90.0 degrees and less than or equal to +90.0 degrees.

x-loc-longCopy link to x-loc-longType: X-Loc-Longmin:    -180max:    180 nullable 
The longitude of the client’s geographical location in degrees, to provide relevant local results. The longitude must be greater than or equal to -180.0 and less than or equal to +180.0 degrees.

The longitude of the client’s geographical location in degrees, to provide relevant local results. The longitude must be greater than or equal to -180.0 and less than or equal to +180.0 degrees.

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

200Copy link to 200Type: LocalPoiSearchApiResponseresultsType: array Results[] nullable 
The

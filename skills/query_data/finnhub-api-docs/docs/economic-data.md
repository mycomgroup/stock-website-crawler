---
id: "url-283bbff7"
type: "api"
title: "Economic Data Premium"
url: "https://finnhub.io/docs/api/economic-data"
description: "Premium: Accessible with Fundamental data or All in One subscription."
source: ""
tags: []
crawl_time: "2026-03-18T06:28:18.675Z"
metadata:
  requestMethod: "GET"
  endpoint: "/economic?code=MA-USA-656880"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "Economic Data Premium\n\nGet economic data.\n\nMethod: GET\n\nPremium: Accessible with Fundamental data or All in One subscription.\n\nExamples:\n\n/economic?code=MA-USA-656880\n\nArguments:\n\ncodeREQUIRED\n\nEconomic code.\n\nResponse Attributes:\n\ncode\n\nFinnhub economic code\n\ndata\n\nArray of economic data for requested code.\n\ndate\n\nDate of the reading\n\nvalue\n\nValue\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.economic_data('MA-USA-656880'))\n\nSample response\n\n{\n  \"code\": \"MA-USA-656880\",\n  \"data\": [\n    {\n      \"date\": \"2020-05-31\",\n      \"value\": -2760\n    },\n    {\n      \"date\": \"2020-04-30\",\n      \"value\": -19557\n    }\n  ]\n}"
  suggestedFilename: "economic-data"
---

# Economic Data Premium

## 源URL

https://finnhub.io/docs/api/economic-data

## 描述

Premium: Accessible with Fundamental data or All in One subscription.

## API 端点

**Method**: `GET`
**Endpoint**: `/economic?code=MA-USA-656880`

## 文档正文

Premium: Accessible with Fundamental data or All in One subscription.

## API 端点

**Method:** `GET`
**Endpoint:** `/economic?code=MA-USA-656880`

Economic Data Premium

Get economic data.

Method: GET

Premium: Accessible with Fundamental data or All in One subscription.

Examples:

/economic?code=MA-USA-656880

Arguments:

codeREQUIRED

Economic code.

Response Attributes:

code

Finnhub economic code

data

Array of economic data for requested code.

date

Date of the reading

value

Value

Sample code
cURL
Python
Javascript
Go
Ruby
Kotlin
PHP

import finnhub
finnhub_client = finnhub.Client(api_key="")

print(finnhub_client.economic_data('MA-USA-656880'))

Sample response

{
  "code": "MA-USA-656880",
  "data": [
    {
      "date": "2020-05-31",
      "value": -2760
    },
    {
      "date": "2020-04-30",
      "value": -19557
    }
  ]
}

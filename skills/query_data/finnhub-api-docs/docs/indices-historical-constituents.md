---
id: "url-667fa01"
type: "api"
title: "Indices Historical Constituents Premium"
url: "https://finnhub.io/docs/api/indices-historical-constituents"
description: "Get full history of index's constituents including symbols and dates of joining and leaving the Index. A list of supported indices for this endpoint can be found here. Method: GET Premium: Premium required."
source: ""
tags: []
crawl_time: "2026-03-18T11:21:33.572Z"
metadata:
  requestMethod: "GET"
  endpoint: "/index/historical-constituents?symbol=^GSPC"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "Indices Historical Constituents Premium\n\nGet full history of index's constituents including symbols and dates of joining and leaving the Index. A list of supported indices for this endpoint can be found here.\n\nMethod: GET\n\nPremium: Premium required.\n\nExamples:\n\n/index/historical-constituents?symbol=^GSPC\n\nArguments:\n\nsymbolREQUIRED\n\nsymbol\n\nResponse Attributes:\n\nhistoricalConstituents\n\nArray of historical constituents.\n\naction\n\nadd or remove.\n\ndate\n\nDate of joining or leaving the index.\n\nsymbol\n\nSymbol\n\nsymbol\n\nIndex's symbol.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.indices_hist_const(symbol = \"^GSPC\"))\n\nSample response\n\n{\n  \"historicalConstituents\": [\n    {\n      \"action\": \"add\",\n      \"symbol\": \"TYL\",\n      \"date\": \"2020-06-22\"\n    },\n    {\n      \"action\": \"add\",\n      \"symbol\": \"TDY\",\n      \"date\": \"2020-06-22\"\n    },\n    {\n      \"action\": \"remove\",\n      \"symbol\": \"JWN\",\n      \"date\": \"2020-06-22\"\n    }\n  ],\n  \"symbol\": \"^GSPC\"\n}"
  suggestedFilename: "indices-historical-constituents"
---

# Indices Historical Constituents Premium

## 源URL

https://finnhub.io/docs/api/indices-historical-constituents

## 描述

Get full history of index's constituents including symbols and dates of joining and leaving the Index. A list of supported indices for this endpoint can be found here. Method: GET Premium: Premium required.

## API 端点

**Method**: `GET`
**Endpoint**: `/index/historical-constituents?symbol=^GSPC`

## 文档正文

Get full history of index's constituents including symbols and dates of joining and leaving the Index. A list of supported indices for this endpoint can be found here. Method: GET Premium: Premium required.

## API 端点

**Method:** `GET`
**Endpoint:** `/index/historical-constituents?symbol=^GSPC`

Indices Historical Constituents Premium

Get full history of index's constituents including symbols and dates of joining and leaving the Index. A list of supported indices for this endpoint can be found here.

Method: GET

Premium: Premium required.

Examples:

/index/historical-constituents?symbol=^GSPC

Arguments:

symbolREQUIRED

symbol

Response Attributes:

historicalConstituents

Array of historical constituents.

action

add or remove.

date

Date of joining or leaving the index.

symbol

Symbol

symbol

Index's symbol.

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

print(finnhub_client.indices_hist_const(symbol = "^GSPC"))

Sample response

{
  "historicalConstituents": [
    {
      "action": "add",
      "symbol": "TYL",
      "date": "2020-06-22"
    },
    {
      "action": "add",
      "symbol": "TDY",
      "date": "2020-06-22"
    },
    {
      "action": "remove",
      "symbol": "JWN",
      "date": "2020-06-22"
    }
  ],
  "symbol": "^GSPC"
}

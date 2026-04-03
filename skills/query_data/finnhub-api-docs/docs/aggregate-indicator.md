---
id: "url-5e75cd36"
type: "api"
title: "Aggregate Indicators Premium"
url: "https://finnhub.io/docs/api/aggregate-indicator"
description: "Get aggregate signal of multiple technical indicators such as MACD, RSI, Moving Average v.v. A full list of indicators can be found here. Method: GET Premium: Premium Access Required"
source: ""
tags: []
crawl_time: "2026-03-18T08:36:04.569Z"
metadata:
  requestMethod: "GET"
  endpoint: "/scan/technical-indicator?symbol=AAPL&resolution=D"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "Aggregate Indicators Premium\n\nGet aggregate signal of multiple technical indicators such as MACD, RSI, Moving Average v.v. A full list of indicators can be found here.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/scan/technical-indicator?symbol=AAPL&resolution=D\n\nArguments:\n\nsymbolREQUIRED\n\nsymbol\n\nresolutionREQUIRED\n\nSupported resolution includes 1, 5, 15, 30, 60, D, W, M .Some timeframes might not be available depending on the exchange.\n\nResponse Attributes:\n\ntechnicalAnalysis\n\nNumber of indicator signals strong buy, buy, neutral, sell, strong sell signals.\n\ncount\n\nNumber of indicators for each signal\n\nbuy\n\nNumber of buy signals\n\nneutral\n\nNumber of neutral signals\n\nsell\n\nNumber of sell signals\n\nsignal\n\nAggregate Signal\n\ntrend\n\nWhether the market is trending.\n\nadx\n\nADX reading\n\ntrending\n\nWhether market is trending or going sideway\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.aggregate_indicator('AAPL', 'D'))\n\nSample response\n\n{\n  \"technicalAnalysis\": {\n    \"count\": {\n      \"buy\": 6,\n      \"neutral\": 7,\n      \"sell\": 4\n    },\n    \"signal\": \"neutral\"\n  },\n  \"trend\": {\n    \"adx\": 24.46020733373421,\n    \"trending\": false\n  }\n}"
  suggestedFilename: "aggregate-indicator"
---

# Aggregate Indicators Premium

## 源URL

https://finnhub.io/docs/api/aggregate-indicator

## 描述

Get aggregate signal of multiple technical indicators such as MACD, RSI, Moving Average v.v. A full list of indicators can be found here. Method: GET Premium: Premium Access Required

## API 端点

**Method**: `GET`
**Endpoint**: `/scan/technical-indicator?symbol=AAPL&resolution=D`

## 文档正文

Get aggregate signal of multiple technical indicators such as MACD, RSI, Moving Average v.v. A full list of indicators can be found here. Method: GET Premium: Premium Access Required

## API 端点

**Method:** `GET`
**Endpoint:** `/scan/technical-indicator?symbol=AAPL&resolution=D`

Aggregate Indicators Premium

Get aggregate signal of multiple technical indicators such as MACD, RSI, Moving Average v.v. A full list of indicators can be found here.

Method: GET

Premium: Premium Access Required

Examples:

/scan/technical-indicator?symbol=AAPL&resolution=D

Arguments:

symbolREQUIRED

symbol

resolutionREQUIRED

Supported resolution includes 1, 5, 15, 30, 60, D, W, M .Some timeframes might not be available depending on the exchange.

Response Attributes:

technicalAnalysis

Number of indicator signals strong buy, buy, neutral, sell, strong sell signals.

count

Number of indicators for each signal

buy

Number of buy signals

neutral

Number of neutral signals

sell

Number of sell signals

signal

Aggregate Signal

trend

Whether the market is trending.

adx

ADX reading

trending

Whether market is trending or going sideway

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

print(finnhub_client.aggregate_indicator('AAPL', 'D'))

Sample response

{
  "technicalAnalysis": {
    "count": {
      "buy": 6,
      "neutral": 7,
      "sell": 4
    },
    "signal": "neutral"
  },
  "trend": {
    "adx": 24.46020733373421,
    "trending": false
  }
}

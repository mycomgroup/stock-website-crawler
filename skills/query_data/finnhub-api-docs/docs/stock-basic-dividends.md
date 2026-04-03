---
id: "url-2b11f8bd"
type: "api"
title: "Basic Financials"
url: "https://finnhub.io/docs/api/stock-basic-dividends"
description: "Get company basic financials such as margin, P/E ratio, 52-week high/low etc. Method: GET"
source: ""
tags: []
crawl_time: "2026-03-18T09:28:08.109Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/metric?symbol=AAPL&metric=all"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "Basic Financials\n\nGet company basic financials such as margin, P/E ratio, 52-week high/low etc.\n\nMethod: GET\n\nExamples:\n\n/stock/metric?symbol=AAPL&metric=all\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol of the company: AAPL.\n\nmetricREQUIRED\n\nMetric type. Can be 1 of the following values all\n\nResponse Attributes:\n\nmetric\n\nMap key-value pair of key ratios and metrics.\n\nmetricType\n\nMetric type.\n\nseries\n\nMap key-value pair of time-series ratios.\n\nsymbol\n\nSymbol of the company.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.company_basic_financials('AAPL', 'all'))\n\nSample response\n\n{\n   \"series\": {\n    \"annual\": {\n      \"currentRatio\": [\n        {\n          \"period\": \"2019-09-28\",\n          \"v\": 1.5401\n        },\n        {\n          \"period\": \"2018-09-29\",\n          \"v\": 1.1329\n        }\n      ],\n      \"salesPerShare\": [\n        {\n          \"period\": \"2019-09-28\",\n          \"v\": 55.9645\n        },\n        {\n          \"period\": \"2018-09-29\",\n          \"v\": 53.1178\n        }\n      ],\n      \"netMargin\": [\n        {\n          \"period\": \"2019-09-28\",\n          \"v\": 0.2124\n        },\n        {\n          \"period\": \"2018-09-29\",\n          \"v\": 0.2241\n        }\n      ]\n    }\n  },\n  \"metric\": {\n    \"10DayAverageTradingVolume\": 32.50147,\n    \"52WeekHigh\": 310.43,\n    \"52WeekLow\": 149.22,\n    \"52WeekLowDate\": \"2019-01-14\",\n    \"52WeekPriceReturnDaily\": 101.96334,\n    \"beta\": 1.2989,\n  },\n  \"metricType\": \"all\",\n  \"symbol\": \"AAPL\"\n}"
  suggestedFilename: "stock-basic-dividends"
---

# Basic Financials

## 源URL

https://finnhub.io/docs/api/stock-basic-dividends

## 描述

Get company basic financials such as margin, P/E ratio, 52-week high/low etc. Method: GET

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/metric?symbol=AAPL&metric=all`

## 文档正文

Get company basic financials such as margin, P/E ratio, 52-week high/low etc. Method: GET

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/metric?symbol=AAPL&metric=all`

Basic Financials

Get company basic financials such as margin, P/E ratio, 52-week high/low etc.

Method: GET

Examples:

/stock/metric?symbol=AAPL&metric=all

Arguments:

symbolREQUIRED

Symbol of the company: AAPL.

metricREQUIRED

Metric type. Can be 1 of the following values all

Response Attributes:

metric

Map key-value pair of key ratios and metrics.

metricType

Metric type.

series

Map key-value pair of time-series ratios.

symbol

Symbol of the company.

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

print(finnhub_client.company_basic_financials('AAPL', 'all'))

Sample response

{
   "series": {
    "annual": {
      "currentRatio": [
        {
          "period": "2019-09-28",
          "v": 1.5401
        },
        {
          "period": "2018-09-29",
          "v": 1.1329
        }
      ],
      "salesPerShare": [
        {
          "period": "2019-09-28",
          "v": 55.9645
        },
        {
          "period": "2018-09-29",
          "v": 53.1178
        }
      ],
      "netMargin": [
        {
          "period": "2019-09-28",
          "v": 0.2124
        },
        {
          "period": "2018-09-29",
          "v": 0.2241
        }
      ]
    }
  },
  "metric": {
    "10DayAverageTradingVolume": 32.50147,
    "52WeekHigh": 310.43,
    "52WeekLow": 149.22,
    "52WeekLowDate": "2019-01-14",
    "52WeekPriceReturnDaily": 101.96334,
    "beta": 1.2989,
  },
  "metricType": "all",
  "symbol": "AAPL"
}
